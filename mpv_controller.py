import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import json
import time
import urllib.parse
import uuid
import html
import yt_dlp
import mpv
import threading
import re
from config import Config as conf
from yt_dlp.networking import Request
from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.extractor.youtube import YoutubeBaseInfoExtractor
import importlib
import inspect

YOUTUBE_IES = filter(
    lambda member: issubclass(member[1], YoutubeBaseInfoExtractor),
    inspect.getmembers(importlib.import_module('yt_dlp.extractor.youtube'), inspect.isclass)
)

_CLIENT_ID = conf.YOUR_CLIENT_ID
_CLIENT_SECRET = conf.YOUR_CLIENT_SECRET
_SCOPES = 'http://gdata.youtube.com https://www.googleapis.com/auth/youtube'

class YouTubeOAuth2Handler(InfoExtractor):
    def store_token(self, token_data):
        self.cache.store('youtube-oauth2', 'token_data', token_data)
        self._TOKEN_DATA = token_data

    def get_token(self):
        if not getattr(self, '_TOKEN_DATA', None):
            self._TOKEN_DATA = self.cache.load('youtube-oauth2', 'token_data')
        return self._TOKEN_DATA

    def validate_token_data(self, token_data):
        return all(key in token_data for key in ('access_token', 'expires', 'refresh_token', 'token_type'))

    def initialize_oauth(self):
        token_data = self.get_token()

        if token_data and not self.validate_token_data(token_data):
            self.report_warning('Invalid cached OAuth2 token data')
            token_data = None

        if not token_data:
            token_data = self.authorize()
            self.store_token(token_data)

        if token_data['expires'] < datetime.datetime.now(datetime.timezone.utc).timestamp() + 60:
            self.to_screen('Access token expired, refreshing')
            token_data = self.refresh_token(token_data['refresh_token'])
            self.store_token(token_data)

        return token_data

    def handle_oauth(self, request: Request):
        if not urllib.parse.urlparse(request.url).netloc.endswith('youtube.com'):
            return

        token_data = self.initialize_oauth()
        request.headers.pop('X-Goog-PageId', None)
        request.headers.pop('X-Goog-AuthUser', None)
        if 'Authorization' in request.headers:
            self.report_warning(
                'Youtube cookies have been provided, but OAuth2 is being used.'
                ' If you encounter problems, stop providing Youtube cookies to yt-dlp.')
            request.headers.pop('Authorization', None)
            request.headers.pop('X-Origin', None)
        request.headers.pop('X-Youtube-Identity-Token', None)
        authorization_header = {'Authorization': f'{token_data["token_type"]} {token_data["access_token"]}'}
        request.headers.update(authorization_header)

    def refresh_token(self, refresh_token):
        token_response = self._download_json(
            'https://www.youtube.com/o/oauth2/token',
            video_id='oauth2',
            note='Refreshing OAuth2 Token',
            data=json.dumps({
                'client_id': _CLIENT_ID,
                'client_secret': _CLIENT_SECRET,
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token'
            }).encode(),
            headers={'Content-Type': 'application/json', '__youtube_oauth__': True})
        error = traverse_obj(token_response, 'error')
        if error:
            self.report_warning(f'Failed to refresh access token: {error}. Restarting authorization flow')
            return self.authorize()

        return {
            'access_token': token_response['access_token'],
            'expires': datetime.datetime.now(datetime.timezone.utc).timestamp() + token_response['expires_in'],
            'token_type': token_response['token_type'],
            'refresh_token': token_response.get('refresh_token', refresh_token)
        }

    def authorize(self):
        code_response = self._download_json(
            'https://www.youtube.com/o/oauth2/device/code',
            video_id='oauth2',
            note='Initializing OAuth2 Authorization Flow',
            data=json.dumps({
                'client_id': _CLIENT_ID,
                'scope': _SCOPES,
                'device_id': uuid.uuid4().hex,
                'device_model': 'ytlr::'
            }).encode(),
            headers={'Content-Type': 'application/json', '__youtube_oauth__': True})

        verification_url = code_response['verification_url']
        user_code = code_response['user_code']
        self.to_screen(f'To give yt-dlp access to your account, go to {verification_url} and enter code {user_code}')

        while True:
            token_response = self._download_json(
                'https://www.youtube.com/o/oauth2/token',
                video_id='oauth2',
                note=False,
                data=json.dumps({
                    'client_id': _CLIENT_ID,
                    'client_secret': _CLIENT_SECRET,
                    'code': code_response['device_code'],
                    'grant_type': 'http://oauth.net/grant_type/device/1.0'
                }).encode(),
                headers={'Content-Type': 'application/json', '__youtube_oauth__': True})

            error = traverse_obj(token_response, 'error')
            if error:
                if error == 'authorization_pending':
                    time.sleep(code_response['interval'])
                    continue
                elif error == 'expired_token':
                    self.report_warning('The device code has expired, restarting authorization flow')
                    return self.authorize()
                else:
                    raise ExtractorError(f'Unhandled OAuth2 Error: {error}')

            self.to_screen('Authorization successful')
            return {
                'access_token': token_response['access_token'],
                'expires': datetime.datetime.now(datetime.timezone.utc).timestamp() + token_response['expires_in'],
                'refresh_token': token_response['refresh_token'],
                'token_type': token_response['token_type']
            }

for _, ie in YOUTUBE_IES:
    class _YouTubeOAuth(ie, YouTubeOAuth2Handler, plugin_name='oauth2'):
        _NETRC_MACHINE = 'youtube'
        _use_oauth2 = False

        def _perform_login(self, username, password):
            if username == 'oauth2':
                self._use_oauth2 = True
                self.initialize_oauth()

        def _create_request(self, *args, **kwargs):
            request = super()._create_request(*args, **kwargs)
            if '__youtube_oauth__' in request.headers:
                request.headers.pop('__youtube_oauth__')
            elif self._use_oauth2:
                self.handle_oauth(request)
            return request

        @property
        def is_authenticated(self):
            if self._use_oauth2:
                token_data = self.get_token()
                return token_data and self.validate_token_data(token_data)
            return super().is_authenticated

# Define search_you_tube function
def search_you_tube(query):
    try:
        youtube = build('youtube', 'v3', developerKey=conf.youtubeAPIkey)
        request = youtube.search().list(
            part='id,snippet',
            q=query,
            maxResults=conf.max_search_number,
            type='video'
        )
        response = request.execute()
        search_results = []
        for video in response['items']:
            title = video["snippet"]["title"]
            video_id = video["id"]["videoId"]
            item = {
                'name': title,
                'value': f'https://www.youtube.com/watch?v={video_id}',
            }
            search_results.append(item)
        return search_results
    except HttpError as e:
        if e.resp.status == 403:
            error_message = e._get_reason()
            print(f"Warning: Encountered 403 Forbidden - {error_message}")
            return None
        else:
            raise

class MPV_Controller:
    def __init__(self):
        self.current_song_index = 0
        self.songs = []
        self.names = []
        self.playURL = False
        self.player = mpv.MPV(ytdl=True)
        self.is_playing = False
        self.player.volume = conf.max_volume
        self.current_position = 0

    def decode_song_name(self, string):
        decoded = html.unescape(string)
        return decoded[:255]

    def extract_video_id(self, url):
        video_id_match = re.match(r'.*v=([^&]+)', url)
        if video_id_match:
            return video_id_match.group(1)
        return None

    def write_search_results_to_file(self):
        search_results = [{"name": name, "url": url} for name, url in zip(self.names, self.songs)]
        with open('search_list.json', 'w') as f:
            json.dump(search_results, f, ensure_ascii=False, indent=4)

    def youtube_search_and_play(self, query):
        if self.is_valid_youtube_link(query):
            video_id = self.extract_video_id(query)
            if video_id:
                self.playURL = True
                self.songs = [f'https://www.youtube.com/watch?v={video_id}']
                self.names = [query]
        else:
            self.playURL = False
            search_results = search_you_tube(query)
            if search_results is None:
                print("Quota exceeded. Please try again later.")
                return None
            self.names = [item['name'] for item in search_results]
            self.songs = [item['value'] for item in search_results]

        self.current_song_index = 0
        if self.songs:
            song_name = self.decode_song_name(self.names[self.current_song_index])
            audio_url = self.download_audio_url(self.songs[self.current_song_index])
            threading.Thread(target=self.play_audio, args=(audio_url,)).start()
            song_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(self.names)])
            print(song_list)
            if not self.playURL:
                self.write_search_results_to_file()
            return song_name
        else:
            print("No songs found for your query or invalid link.")
            return None

    def play_audio(self, url):
        self.is_playing = True
        self.current_position = 0
        self.player.play(url)
        self.player.wait_for_playback()
        self.is_playing = False

    def play_next_song(self):
        if not self.songs:
            print("No songs in the playlist.")
            return None
        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
        if self.current_song_index == 0:
            song_name = "No more songs in the playlist."
            print(song_name)
            return song_name
        else:
            song_name = self.decode_song_name(self.names[self.current_song_index])
            audio_url = self.download_audio_url(self.songs[self.current_song_index])
            threading.Thread(target=self.play_audio, args=(audio_url,)).start()
            return song_name

    def play_previous_song(self):
        if not self.songs:
            print("No songs in the playlist.")
            return None
        self.current_song_index = (self.current_song_index - 1) % len(self.songs)
        if self.current_song_index < 0:
            self.current_song_index = len(self.songs) - 1
        song_name = self.decode_song_name(self.names[self.current_song_index])
        audio_url = self.download_audio_url(self.songs[self.current_song_index])
        threading.Thread(target=self.play_audio, args=(audio_url,)).start()
        return song_name

    def stop_playback(self):
        self.player.stop()
        self.is_playing = False

    def pause_resume_playback(self):
        self.player.pause = not self.player.pause

    def seek_forward(self, seconds, fromUserID, callback):
        try:
            new_position = self.current_position + seconds
            total_duration = int(round(self.player.duration))

            if new_position < total_duration:
                self.player.command('seek', seconds, 'relative')
                message = f"Перемотка вперед на {seconds} секунд"
                callback(message, fromUserID)
            else:
                error_message = "Cannot seek forward: exceeds total duration"
                print(error_message)
                callback(error_message, fromUserID)
        except Exception as e:
            error_message = f"Error seeking forward: {e}"
            print(error_message)
            callback(error_message, fromUserID)

    def seek_backward(self, seconds, fromUserID, callback):
        try:
            new_position = self.current_position - seconds
            if new_position >= 0:
                self.player.command('seek', -seconds, 'relative')
                message = f"Перемотка назад на {seconds} секунд"
                callback(message, fromUserID)
            else:
                error_message = "Cannot seek backward: exceeds start of the track"
                print(error_message)
                callback(error_message, fromUserID)
        except Exception as e:
            error_message = f"Error seeking backward: {e}"
            print(error_message)
            callback(error_message, fromUserID)

    def set_volume(self, volume):
        self.player.volume = volume

    def set_speed(self, speed):
        if 1 <= speed <= 5.0:
            self.player.speed = speed
        else:
            print("Invalid speed. Please set a value between 0.1 and 5.0.")

    def player_status(self):
        if self.player.pause:
            return "paused"
        elif self.player.playback_abort:
            return "stopped"
        elif self.player.playback_start:
            return "playing"
        return "unknown"

    def is_valid_youtube_link(self, link):
        pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
        return re.match(pattern, link) is not None

    def download_audio_url(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'ignoreerrors': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            return audio_url

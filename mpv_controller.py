from __future__ import print_function, unicode_literals
from youtube_api import search_you_tube
import html
import yt_dlp
import mpv
import threading
import re
import json
from config import Config as conf
import time

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
        # self.playback_thread = threading.Thread(target=self.check_playback_status, daemon=True)
        # self.playback_thread.start()

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

    # def check_playback_status(self):
    #     while True:
    #         if self.is_playing:
    #             total_duration = self.player.duration
    #             self.current_position = self.player.playback_time
    #             remaining_time = int(round(total_duration - self.current_position))
    #             print(f"song remaining time -> {remaining_time}")
    #             if remaining_time <= 2:
    #                 self.play_next_song()
    #         time.sleep(2)

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

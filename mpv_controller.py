from __future__ import print_function, unicode_literals
from youtube_api import search_you_tube
import html
import yt_dlp
import mpv_module
import threading
import re
import json
from config import Config as conf
import time
import random
from urllib.parse import parse_qs, urlparse

class MPV_Controller:
    playback_update_interval = 3
    playback_icon_sets = (
        ("♪", "♫", "♬", "♩"),
        ("▶", "▷"),
        ("◐", "◓", "◑", "◒"),
        (">", ">>", ">>>"),
    )

    def __init__(self, update_nickname_callback, update_song_name_callback):
        self.current_song_index = 0
        self.songs = []
        self.names = []
        self.songName = ""
        self.playURL = False
        self.player = mpv_module.MPV(
            ytdl=True,  
            cache=True,  
            cache_secs=30,  # Set minimal caching duration
            demuxer_max_bytes="50M", 
            demuxer_max_back_bytes="10M",  
        )
        self.is_playing = False
        self.player.volume = conf.max_volume
        self.current_position = 0
        self.current_remaining_label = None
        self.playback_icons = self.playback_icon_sets[0]
        self.playback_icon_index = 0
        self.lock = threading.RLock()
        self.update_nickname_callback = update_nickname_callback
        self.update_song_name_callback = update_song_name_callback
        self.playback_thread = threading.Thread(target=self.check_playback_status, daemon=True)
        self.playback_thread.start()
        #favorite vars init
        self.current_song_name = None
        self.current_song_url = None

    def decode_song_name(self, string):
        decoded = html.unescape(string)
        return decoded[:255]

    def song_status_label(self, index=None, name=None):
        with self.lock:
            playlist_size = len(self.names)
            song_index = self.current_song_index if index is None else index
            song_name = self.current_song_name if name is None else name
        if not song_name:
            return "stopped"
        width = max(2, len(str(playlist_size)))
        return f"{song_index + 1:0{width}d}.{song_name}"

    def select_random_icon_set(self):
        self.playback_icons = random.choice(self.playback_icon_sets)
        self.playback_icon_index = 0

    def playback_time_label(self, remaining_time=None):
        icon = self.playback_icons[self.playback_icon_index % len(self.playback_icons)]
        self.playback_icon_index += 1
        time_label = self.formatted_time(remaining_time) if remaining_time is not None else "--:--"
        self.current_remaining_label = time_label
        return f"{time_label} {icon}"

    def extract_video_id(self, url):
        parsed = urlparse(url if "://" in url else f"https://{url}")
        host = parsed.netloc.lower().removeprefix("www.")
        path_parts = [part for part in parsed.path.split("/") if part]

        if host == "youtu.be" and path_parts:
            return path_parts[0]

        if host in ("youtube.com", "m.youtube.com", "music.youtube.com"):
            query_video = parse_qs(parsed.query).get("v", [None])[0]
            if query_video:
                return query_video
            if len(path_parts) >= 2 and path_parts[0] in ("live", "shorts", "embed"):
                return path_parts[1]

        return None

    def write_search_results_to_file(self):
        search_results = [{"name": name, "url": url} for name, url in zip(self.names, self.songs)]
        with open('search_list.json', 'w', encoding='utf-8') as f:
            json.dump(search_results, f, ensure_ascii=False, indent=4)

    def clear_playlist(self):
        with self.lock:
            self.songs = []
            self.names = []
            self.songName = ""
            self.current_song_index = 0
            self.current_song_name = None
            self.current_song_url = None

    def youtube_search_and_play(self, query, display_name=None):
        with self.lock:
            self.is_playing = False
            try:
                self.player.stop()
            except Exception as e:
                print(f"Error stopping previous playback: {e}")

        if self.is_valid_youtube_link(query):
            print("URL validated")
            video_id = self.extract_video_id(query)
            if not video_id:
                self.clear_playlist()
                print("No video ID found in YouTube link.")
                return None
            with self.lock:
                self.playURL = True
                songs = [f'https://www.youtube.com/watch?v={video_id}']
                names = [display_name or query]
               
        else:
            search_results = search_you_tube(query)
            if search_results is None:
                print("Quota exceeded. Please try again later.")
                return None
            with self.lock:
                self.playURL = False
                names = [item['name'] for item in search_results]
                songs = [item['value'] for item in search_results]
            
        if songs:
            song_name = self.decode_song_name(names[0])
            audio_url = self.download_audio_url(songs[0])
            if not audio_url:
                self.clear_playlist()
                return None
            with self.lock:
                self.songs = songs
                self.names = names
                self.current_song_index = 0
       
            threading.Thread(target=self.play_audio, args=(audio_url,), daemon=True).start()
            song_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(names)])
            print(song_list)
            
            #self.update_nickname_callback(f"{conf.botName} playing")
            
            
            with self.lock:
                self.songName = song_name
                self.current_song_name = song_name
                self.current_song_url = songs[0]
                self.select_random_icon_set()
            self.update_song_name_callback(self.song_status_label(0, song_name))
            
            if not self.playURL:
                self.write_search_results_to_file()
            return song_name
        else:
            print("No songs found for your query or invalid link.")
            return None

    def play_saved_playlist(self, playlist, start_index=0):
        if not playlist or not 0 <= start_index < len(playlist):
            return None

        with self.lock:
            self.is_playing = False
            try:
                self.player.stop()
            except Exception as e:
                print(f"Error stopping previous playback: {e}")

        names = [item.get('name', item.get('url', '')) for item in playlist]
        songs = [item.get('url') for item in playlist]
        if not songs[start_index]:
            return None

        song_name = self.decode_song_name(names[start_index])
        audio_url = self.download_audio_url(songs[start_index])
        if not audio_url:
            self.clear_playlist()
            return None

        with self.lock:
            self.playURL = False
            self.songs = songs
            self.names = names
            self.current_song_index = start_index
            self.current_song_name = song_name
            self.current_song_url = songs[start_index]
            self.songName = song_name
            self.select_random_icon_set()

        threading.Thread(target=self.play_audio, args=(audio_url,), daemon=True).start()
        self.update_song_name_callback(self.song_status_label(start_index, song_name))
        return song_name

    def play_audio(self, url):
        # self.is_playing = True
        # self.current_position = 0
        # print(f"Playing audio: {url}")
        # self.player.play(url) 
        # ver 2.1
        
        if not url:
            print("Error: No valid audio URL provided. Skipping playback.")
            with self.lock:
                self.is_playing = False
            return

        with self.lock:
            self.is_playing = True
            self.current_position = 0
        print(f"Playing audio: {url}")
       
        #self.update_song_name_callback("stopped")  # ✅ Update status immediately
        if conf.showTime:
            self.update_nickname_callback(self.playback_time_label())
        else:
            self.update_nickname_callback("playing")

        try:
            with self.lock:
                self.player.play(url)
            time.sleep(1)  # Give MPV time to start playback
           
        except AttributeError as e:
            print(f"Error: Invalid audio URL. {e}")
            with self.lock:
                self.is_playing = False
        except Exception as e:
            print(f"Unexpected error while playing audio: {e}")
            with self.lock:
                self.is_playing = False

     
    def check_playback_status(self):
        while True:
            try:
                if not conf.showTime:
                    time.sleep(self.playback_update_interval)
                    continue
                with self.lock:
                    is_playing = self.is_playing
                    total_duration = self.player.duration if is_playing else None
                    current_position = self.player.playback_time if is_playing else None
                    self.current_position = current_position or 0
                if is_playing:
                    if total_duration is not None and self.current_position is not None:
                        remaining_time = int(round(total_duration - self.current_position))
                        #print(f"song remaining time -> {remaining_time}")
                        self.update_nickname_callback(self.playback_time_label(remaining_time))
                        if remaining_time <= 3:
                            self.play_next_song()
                    else:
                        self.update_nickname_callback(self.playback_time_label())
            except Exception as e:
                print(f"Playback status monitor error: {e}")
            time.sleep(self.playback_update_interval)
    

    def play_next_song(self):
        with self.lock:
            if not self.songs:
                print("No songs in the playlist.")
                return None
            next_index = self.current_song_index + 1
            if next_index >= len(self.songs):
                self.is_playing = False
                try:
                    self.player.stop()
                except Exception as e:
                    print(f"Error stopping at end of playlist: {e}")
                self.update_song_name_callback("stopped")
                self.update_nickname_callback("stopped")
                self.current_song_index = 0
                self.current_song_name = None
                self.current_song_url = None
                self.current_remaining_label = None
                self.songName = ""
                print("No more songs in the playlist.")
                return "No more songs in the playlist."
            self.current_song_index = next_index
            song_name = self.decode_song_name(self.names[self.current_song_index])
            song_url = self.songs[self.current_song_index]
            self.current_song_name = song_name
            self.current_song_url = song_url
            self.songName = song_name
            self.select_random_icon_set()
            self.is_playing = True

        audio_url = self.download_audio_url(song_url)
        if not audio_url:
            with self.lock:
                self.is_playing = False
            return None
        print(song_name)
        self.update_song_name_callback(self.song_status_label(None, song_name))
        threading.Thread(target=self.play_audio, args=(audio_url,), daemon=True).start()
        return song_name

    def play_previous_song(self):
        with self.lock:
            if not self.songs:
                print("No songs in the playlist.")
                return None
            self.current_song_index = (self.current_song_index - 1) % len(self.songs)
            song_name = self.decode_song_name(self.names[self.current_song_index])
            song_url = self.songs[self.current_song_index]
            self.current_song_name = song_name
            self.current_song_url = song_url
            self.songName = song_name
            self.select_random_icon_set()
            self.is_playing = True

        audio_url = self.download_audio_url(song_url)
        if not audio_url:
            with self.lock:
                self.is_playing = False
            return None
        threading.Thread(target=self.play_audio, args=(audio_url,), daemon=True).start()
        print(song_name)
        self.update_song_name_callback(self.song_status_label(None, song_name))
        return song_name

    def stop_playback(self):
        with self.lock:
            self.player.stop()
            self.is_playing = False
            self.current_song_name = None
            self.current_song_url = None
            self.current_remaining_label = None
            self.songName = ""
       
        if conf.showTime:
            self.update_nickname_callback("stopped")
        else:
            self.update_nickname_callback("stopped") 
        self.update_song_name_callback("stopped")
        

    def pause_resume_playback(self):
        with self.lock:
            self.player.pause = not self.player.pause
            play_status = "Paused" if self.player.pause else "Playing"
            if self.player.pause:
                self.is_playing = False
            elif self.current_song_name:
                self.is_playing = True
        
        self.update_nickname_callback(play_status.lower())

    def seek_forward(self, seconds, fromUserID, callback):
        try:
            with self.lock:
                self.player.command('seek', seconds, 'relative')
            message = f"Перемотка вперед на {seconds} секунд"
            callback(message, fromUserID)
        except Exception as e:
            error_message = f"Error seeking forward: {e}"
            print(error_message)
            callback(error_message, fromUserID)

    def seek_backward(self, seconds, fromUserID, callback):
        try:
            with self.lock:
                self.player.command('seek', -seconds, 'relative')
            message = f"Перемотка назад на {seconds} секунд"
            callback(message, fromUserID)
        except Exception as e:
            error_message = f"Error seeking backward: {e}"
            print(error_message)
            callback(error_message, fromUserID)

    def set_volume(self, volume):
        with self.lock:
            self.player.volume = volume
        
    def get_volume(self):
        with self.lock:
            return self.player.volume

    def set_speed(self, speed):
        if 1 <= speed <= 5.0:
            with self.lock:
                self.player.speed = speed
        else:
            print("Invalid speed. Please set a value between 0.1 and 5.0.")
  
    @property
    def player_status(self):
        with self.lock:
            if self.player.pause:
                return "paused"
            if self.is_playing:  
                return "playing" 
            return "stopped" if self.player.playback_time is None else "loading"

    def is_valid_youtube_link(self, link):
        parsed = urlparse(link if "://" in link else f"https://{link}")
        host = parsed.netloc.lower().removeprefix("www.")
        return host in ("youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be")

    def download_audio_url(self, url):
      
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'ignoreerrors': True,
            
        }
        if conf.oAuth:
            print("Using oAuth")
            ydl_opts.update({
                'username': 'oauth+MyProfile',
                'password': '',
            })
        
        if conf.cookies:
            print("Using cookies")
            ydl_opts['cookiefile'] = 'all_cookies.txt'

        #ver 2.1
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info or 'url' not in info:
                    print("Error: No valid audio URL found.")
                    return None
                return info['url']
        except yt_dlp.utils.DownloadError as e:
            print(f"Error: Failed to download audio. {e}")
            if conf.cookies:
                print("Check if the cookie file is valid and properly formatted.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    #fforrmatted time  
    def formatted_time(self, seconds):
        if seconds <= 0:
            return "00:00"
        if seconds >= 3600:
            return time.strftime("%H:%M:%S", time.gmtime(seconds))
        else:
            return time.strftime("%M:%S", time.gmtime(seconds))
    

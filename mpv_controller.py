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

class MPV_Controller:
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
        self.playback_thread = threading.Thread(target=self.check_playback_status, daemon=True)
        if conf.showTime:
            self.playback_thread.start()
        self.update_nickname_callback = update_nickname_callback
        self.update_song_name_callback = update_song_name_callback
        #favorite vars init
        self.current_song_name = None
        self.current_song_url = None

    def decode_song_name(self, string):
        decoded = html.unescape(string)
        return decoded[:255]

    def extract_video_id(self, url):
        video_id_match = re.match(r'.*v=([^&]+)', url)
        if video_id_match:
            return video_id_match.group(1)
        live_video_id_match = re.match(r'.*\/live\/([^?]+)', url)
        if live_video_id_match:
            return live_video_id_match.group(1)
        return None

    def write_search_results_to_file(self):
        search_results = [{"name": name, "url": url} for name, url in zip(self.names, self.songs)]
        with open('search_list.json', 'w', encoding='utf-8') as f:
            json.dump(search_results, f, ensure_ascii=False, indent=4)

    def youtube_search_and_play(self, query):
        if self.is_valid_youtube_link(query):
            print("URL validated")
            video_id = self.extract_video_id(query)
            if video_id:
                self.playURL = True
                self.songs = [f'https://www.youtube.com/watch?v={video_id}']
                self.names = [query]
                self.songName = query
               
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
       
            
            self.is_playing = True
            

            threading.Thread(target=self.play_audio, args=(audio_url,)).start()
            song_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(self.names)])
            print(song_list)
            
            #self.update_nickname_callback(f"{conf.botName} playing")
            
            
            self.songName = song_name
            self.update_song_name_callback(self.songName)
            
            #song name for favorite
            self.current_song_name = song_name
            #song url for favorite
            self.current_song_url = self.songs[self.current_song_index]
            
            if not self.playURL:
                self.write_search_results_to_file()
            return song_name
        else:
            print("No songs found for your query or invalid link.")
            return None

    def play_audio(self, url):
        # self.is_playing = True
        # self.current_position = 0
        # print(f"Playing audio: {url}")
        # self.player.play(url) 
        # ver 2.1
        
        if not url:
            print("Error: No valid audio URL provided. Skipping playback.")
            self.is_playing = False
            return

        self.is_playing = True
        self.current_position = 0
        print(f"Playing audio: {url}")
       
        #self.update_song_name_callback("stopped")  # ✅ Update status immediately
        if conf.showTime == False:
            self.update_nickname_callback(f"{conf.botName} playing")

        try:
            self.player.play(url)
            time.sleep(1)  # Give MPV time to start playback
           
        except AttributeError as e:
            print(f"Error: Invalid audio URL. {e}")
            self.is_playing = False
        except Exception as e:
            print(f"Unexpected error while playing audio: {e}")
            self.is_playing = False

     
    def check_playback_status(self):
        while True:
            if self.is_playing:
                total_duration = self.player.duration
                self.current_position = self.player.playback_time
                if total_duration is not None and self.current_position is not None:
                    remaining_time = int(round(total_duration - self.current_position))
                    #print(f"song remaining time -> {remaining_time}")
                    self.update_nickname_callback(self.formatted_time(remaining_time))
                    if remaining_time <= 3:
                        self.play_next_song()
            time.sleep(5)
    

    def play_next_song(self):
        if not self.songs:
            print("No songs in the playlist.")
            return None
        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
        if self.current_song_index == 0:
            song_name = "No more songs in the playlist."
        
            return song_name
        else:
            song_name = self.decode_song_name(self.names[self.current_song_index])
            audio_url = self.download_audio_url(self.songs[self.current_song_index])
            print(song_name)
            self.current_song_name = song_name
            self.current_song_url = self.songs[self.current_song_index]
            self.songName = song_name
            self.is_playing = True  # ✅ Update status immediately
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
        self.current_song_name = song_name
        self.current_song_url = self.songs[self.current_song_index]
        threading.Thread(target=self.play_audio, args=(audio_url,)).start()
        print(song_name)
        self.songName = song_name
        self.update_song_name_callback(self.songName)
        return song_name

    def stop_playback(self):
        self.player.stop()
        self.is_playing = False
       
        if conf.showTime:
            self.update_nickname_callback(self.formatted_time(0))
        else:
            self.update_nickname_callback("Stopped") 
        

    def pause_resume_playback(self):
        self.player.pause = not self.player.pause
        play_status = "Paused" if self.player.pause else "Playing"
        
        if self.current_song_name:
            self.update_nickname_callback(f"{play_status}")  # ✅ Update nickname
        else:
            self.update_nickname_callback(f"{play_status}")  # ✅ Fallback if no song name

    def seek_forward(self, seconds, fromUserID, callback):
        try:
            self.player.command('seek', seconds, 'relative')
            message = f"Перемотка вперед на {seconds} секунд"
            callback(message, fromUserID)
        except Exception as e:
            error_message = f"Error seeking forward: {e}"
            print(error_message)
            callback(error_message, fromUserID)

    def seek_backward(self, seconds, fromUserID, callback):
        try:
            self.player.command('seek', -seconds, 'relative')
            message = f"Перемотка назад на {seconds} секунд"
            callback(message, fromUserID)
        except Exception as e:
            error_message = f"Error seeking backward: {e}"
            print(error_message)
            callback(error_message, fromUserID)

    def set_volume(self, volume):
        self.player.volume = volume
        
    def get_volume(self):
        return self.player.volume

    def set_speed(self, speed):
        if 1 <= speed <= 5.0:
            self.player.speed = speed
        else:
            print("Invalid speed. Please set a value between 0.1 and 5.0.")
  
    @property
    def player_status(self):
        print(f"DEBUG: pause={self.player.pause}, playback_time={self.player.playback_time}, time_pos={self.player.time_pos}")

        if self.player.pause:
            return "paused"
        
        if self.is_playing:  
            return "playing" 
        
        return "stopped" if self.player.playback_time is None else "loading"

    
    
    def is_valid_youtube_link(self, link):
        pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
        return re.match(pattern, link) is not None

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

        # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        #     info = ydl.extract_info(url, download=False)
        #     audio_url = info['url']
        #     return audio_url
        
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
        if seconds == 0:
            return
        if seconds >= 3600:
            return time.strftime("%H:%M:%S", time.gmtime(seconds))
        else:
            return time.strftime("%M:%S", time.gmtime(seconds))
    

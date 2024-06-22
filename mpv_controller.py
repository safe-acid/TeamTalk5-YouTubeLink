from __future__ import print_function, unicode_literals
from youtube_api import search_you_tube
import html
import yt_dlp
import mpv
import threading
import re
import json
from config import Config as conf

class MPV_Controller:
    def __init__(self):
        # Global variables for song management
        self.current_song_index = 0
        self.songs = []
        self.names = []
        self.playURL = False

        # Create an MPV player instance
        self.player = mpv.MPV(ytdl=True)
        self.is_playing = False

        # Set initial volume to the maximum volume defined in the configuration
        self.player.volume = conf.max_volume

    # Decode song name
    def decode_song_name(self, string):
        decoded = html.unescape(string)
        return decoded[:255]

    # Extract video ID from a YouTube URL
    def extract_video_id(self, url):
        video_id_match = re.match(r'.*v=([^&]+)', url)
        if video_id_match:
            return video_id_match.group(1)
        return None
    def write_search_results_to_file(self):
        search_results = [{"name": name, "url": url} for name, url in zip(self.names, self.songs)]
        with open('search_list.json', 'w') as f:
            json.dump(search_results, f, ensure_ascii=False, indent=4)
            
    # Perform the search and start playing
    def youtube_search_and_play(self, query):
        # Check if query is a valid YouTube video link
        if self.is_valid_youtube_link(query):
            video_id = self.extract_video_id(query)
            if video_id:
                self.playURL = True
                self.songs = [f'https://www.youtube.com/watch?v={video_id}']  # Create a list with only the given link
                self.names = [query]  # For consistency, assume the name is the link itself
        else:
            # Perform a YouTube search
            self.playURL = False
            search_results = search_you_tube(query)

            if search_results is None:
                print("Quota exceeded. Please try again later.")
                return None  # Exit early if quota is exceeded

            self.names = [item['name'] for item in search_results]
            self.songs = [item['value'] for item in search_results]

        self.current_song_index = 0  # Reset index for the new playlist

        if self.songs:
            song_name = self.decode_song_name(self.names[self.current_song_index])
            audio_url = self.download_audio_url(self.songs[self.current_song_index])
            threading.Thread(target=self.play_audio, args=(audio_url,)).start()
            song_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(self.names)])
            print(song_list)
            if self.playURL == False:
                self.write_search_results_to_file()  # Write results to JSON file
            return song_name
        else:
            print("No songs found for your query or invalid link.")
            return None

    def play_audio(self, url):
        self.player.play(url)
        self.player.wait_for_playback()

    # Play the next song
    def play_next_song(self):
        if not self.songs:  # Check if songs list is empty
            print("No songs in the playlist.")
            return None
        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
        if self.current_song_index == 0:  # Reached the end of the list
            song_name = "No more songs in the playlist."
            return song_name
        else:
            song_name = self.decode_song_name(self.names[self.current_song_index])
            audio_url = self.download_audio_url(self.songs[self.current_song_index])
            threading.Thread(target=self.play_audio, args=(audio_url,)).start()
            return song_name

    # Play the previous song
    def play_previous_song(self):
        if not self.songs:  # Check if songs list is empty
            print("No songs in the playlist.")
            return None
        self.current_song_index = (self.current_song_index - 1) % len(self.songs)
        if self.current_song_index < 0:
            self.current_song_index = len(self.songs) - 1
        song_name = self.decode_song_name(self.names[self.current_song_index])
        audio_url = self.download_audio_url(self.songs[self.current_song_index])
        threading.Thread(target=self.play_audio, args=(audio_url,)).start()
        return song_name

    # Stop playback
    def stop_playback(self):
        self.player.stop()

    # Pause/Resume playback
    def pause_resume_playback(self):
        self.player.pause = not self.player.pause

    # Seek forward
    def seek_forward(self, seconds):
        self.player.command('seek', seconds, 'relative')

    # Seek backward
    def seek_backward(self, seconds):
        self.player.command('seek', -seconds, 'relative')

    # Set volume
    def set_volume(self, volume):
        self.player.volume = volume
     # Set playback speed
    def set_speed(self, speed):
        if 1 <= speed <= 5.0:
            self.player.speed = speed
        else:
            print("Invalid speed. Please set a value between 0.1 and 5.0.")

    # Check player status
    def player_status(self):
        
        if self.player.pause:
            return "paused"
        elif self.player.playback_abort:
            return "stopped"
        elif self.player.playback_start:
            return "playing"
        return "unknown"

    # Function to check if a string is a valid YouTube video link
    def is_valid_youtube_link(self, link):
        pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
        return re.match(pattern, link) is not None

    # Download audio URL
    def download_audio_url(self, url):
        # Specify format options to get the best audio
        ydl_opts = {
            'format': 'bestaudio/best',  # Selects the best audio quality
            'noplaylist': True,  # If you want to download a single song not a playlist
            'ignoreerrors': True,  # Ignore errors to handle live streams
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract information without downloading
            info = ydl.extract_info(url, download=False)

            if 'is_live' in info and info['is_live']:
                print(f"{info['title']} is a live stream.")
                audio_url = info['url']
            else:
                # Direct URL to the best audio stream
                audio_url = info['url']

            # Extract additional metadata
            title = info.get('title', 'Unknown Title')
            uploader = info.get('uploader', 'Unknown Uploader')
            upload_date = info.get('upload_date', 'Unknown Date')
            duration = info.get('duration', 0)  # Duration in seconds

            # debug Print extracted information 
            # print(f"Audio URL: {audio_url}")
            # print(f"Title: {title}")
            # print(f"Uploader: {uploader}")
            # print(f"Upload Date: {upload_date}")
            # print(f"Duration: {duration} seconds")
        return audio_url

# ##debug
# if __name__ == "__main__":
#     mpv_controller = MPV_Controller()
#     url = "iron maiden"
#     mpv_controller.youtube_search_and_play(url)

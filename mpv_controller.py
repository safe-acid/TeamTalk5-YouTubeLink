from __future__ import print_function, unicode_literals
from youtube_api import search_you_tube
import html
import yt_dlp
import mpv
import threading
import re
from config import Config as conf


# Global variables for song management
current_song_index = 0
songs = []
names = []

# Create an MPV player instance
player = mpv.MPV(ytdl=True)

# Decode song name
def decode_song_name(string):
    decoded = html.unescape(string)
    return decoded[:255]

# Extract video ID from a YouTube URL
def extract_video_id(url):
    video_id_match = re.match(r'.*v=([^&]+)', url)
    if video_id_match:
        return video_id_match.group(1)
    return None

# Perform the search and start playing
def youtube_search_and_play(query):
    global songs, names, current_song_index
    
    #youtube_main.ttClient.send_message("Quota exceeded. Please try again later.", None , 2)
    # Check if query is a valid YouTube video link
    if is_valid_youtube_link(query):
        video_id = extract_video_id(query)
        if video_id:
            songs = [f'https://www.youtube.com/watch?v={video_id}']  # Create a list with only the given link
            names = [query]  # For consistency, assume the name is the link itself
    else:
        # Perform a YouTube search
        search_results = search_you_tube(query)

        if search_results is None:
            #tt.send_message("Quota exceeded. Please try again later.", None , 2)
            print("Quota exceeded. Please try again later.")
            return None  # Exit early if quota is exceeded

        names = [item['name'] for item in search_results]
        songs = [item['value'] for item in search_results]

    current_song_index = 0  # Reset index for the new playlist

    if songs:
        song_name = decode_song_name(names[current_song_index])
        
        audio_url = download_audio_url(songs[current_song_index])
        threading.Thread(target=play_audio, args=(audio_url,)).start()
        song_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(names)])
        print(song_list)
        return song_name
    else:
        print("No songs found for your query or invalid link.")
        return None

def play_audio(url):
    player.play(url)
    player.wait_for_playback()

# Play the next song
def play_next_song():
    global current_song_index
    if not songs:  # Check if songs list is empty
        print("No songs in the playlist.")
        return None
    current_song_index = (current_song_index + 1) % len(songs)
    if current_song_index == 0:  # Reached the end of the list
        song_name = "No more songs in the playlist."
        return song_name
    else:
        song_name = decode_song_name(names[current_song_index])
        audio_url = download_audio_url(songs[current_song_index])
        threading.Thread(target=play_audio, args=(audio_url,)).start()
        return song_name

# Play the previous song
def play_previous_song():
    global current_song_index
    if not songs:  # Check if songs list is empty
        print("No songs in the playlist.")
        return None
    current_song_index = (current_song_index - 1) % len(songs)
    if current_song_index < 0:
        current_song_index = len(songs) - 1
    song_name = decode_song_name(names[current_song_index])
    audio_url = download_audio_url(songs[current_song_index])
    threading.Thread(target=play_audio, args=(audio_url,)).start()
    return song_name

# Stop playback
def stop_playback():
    player.stop()

# Pause/Resume playback
def pause_resume_playback():
    player.pause = not player.pause
    
# Seek forward
def seek_forward(seconds):
    player.command('seek', seconds, 'relative')

# Seek backward
def seek_backward(seconds):
    player.command('seek', -seconds, 'relative')

# Function to check if a string is a valid YouTube video link
def is_valid_youtube_link(link):
    pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    return re.match(pattern, link) is not None

# Set volume
def set_volume(volume):
    player.volume = volume
# Download audio URL
def download_audio_url(url):
    # Specify format options to get the best audio
    ydl_opts = {
        'format': 'bestaudio/best',  # Selects the best audio quality
        'noplaylist': True,  # If you want to download a single song not a playlist
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract information without downloading
        info = ydl.extract_info(url, download=False)
        
        # Direct URL to the best audio stream
        audio_url = info['url']
        # Extract additional metadata
        title = info.get('title', 'Unknown Title')
        uploader = info.get('uploader', 'Unknown Uploader')
        upload_date = info.get('upload_date', 'Unknown Date')
        duration = info.get('duration', 0)  # Duration in seconds

        # Print extracted information
        print(f"Audio URL: {audio_url}")
        print(f"Title: {title}")
        print(f"Uploader: {uploader}")
        print(f"Upload Date: {upload_date}")
        print(f"Duration: {duration} seconds")
    return audio_url

# if __name__ == "__main__":
#     url = "iron maiden"
#     youtube_search_and_play(url)

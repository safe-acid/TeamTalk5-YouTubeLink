# TeamTalk5-YouTubeLink
This is a simple YouTube Player for TeamTalk5. YouTube Data API v3 is used for best search. The bot will reconnect automatically if the server is rebooted.

### Minimum requirements:
* Windows 10/11       x64
* Mac OS X (10.9)     x86_64
* Linux (Ubuntu 22)   x86_64
* Python 3.11 or later

# Installation 

## 1. Install Requirements
Install python requirements from requirements.txt
```shell script
pip install -r requirements.txt
```
Download essentiial TeamTalk5 SDK using the command
```shell script
python setup.py
```
Linux:
```shell script
sudo apt install -y pulseaudio libmpv-dev
```
Mac:
```shell script
brew install pulseaudio
brew install mpv
```
## 2. Set Up Audio Device ID
Define Audio Device ID by running the command
```shell script
python devices.py
```

## 3. Configure Settings
Update your Audio ID and server's settings in config.py file and API Key.
API key could be created for free in <a href = "https://console.cloud.google.com/"> Google Cloud Console</a>
Menu -> APIs & Servces -> Creditants

Check if YouTube Data API v3 is enabled, go to:


Menu -> APIs & Servces -> Enabled APIs & Services
and search for YouTube Data API v3

## 4. Run the Bot
Run the RadioLink by command
```shell script
python youtube_main.py
```

The default langauge is English, if you want to run on Russian use command
```shell script
python youtube_main.py --language ru
```
### OAuth
OAuth login is no longer supported. Use a YouTube Data API v3 key for search, and cookies only when your server IP is blocked by YouTube.

## Commands
1. [s] - searching and playing the song from YouTube, you could drop youtube links and live links as well
    - example: s Metallica 
    - example: s https://www.youtube.com/watch?v=X4bgXH3sJ2Q

2. [p] - play\pause
3. [d] - download the current song as `yt_song name.mp3` and upload it to the current channel's files
4. [+] - play next song
5. [-] - play previous song
6. [+X] - seeking forward
    - example or seeking forward for 30 seconds: +30
7. [-X] - seeking backward
    - example or seeking backward for 30 seconds: -30
8. [pl] - showing last searched results
9. [plX] - play song from search result bu ID
    - example of playing song no 10: pl10
10. [sp] - change of speed from 1 to 4
    - example of playing 2 times faster: sp2  
11. [vX] - set the volume
    - example of 50%: v50    
12. [?] - check current volume
13. [f+] - add song to favorite list
14. [fl] - check favorite list
15. [fpX] - play song by id from favorite list
    - example fp10
16. [f-X] - remove song from favorite list
    - example f-10
17. [v] - version
18. [q] - quit the bot

### Notes:

Telegram - <a href="https://t.me/TT5Link"> TT5Link</a>

Good Luck:
Котяра 🐾

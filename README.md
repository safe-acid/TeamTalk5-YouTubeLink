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
Windows:

mpv - Download the installer or portable version from <a href="https://mpv.io/installation/"> mpv.io</a>

libmpv - Download the installer or portable version from <a href="https://mpv.io/installation/"> libmpv </a>


Linux:
```shell script
sudo apt install -y pulseaudio mpv libmpv-dev
```
Mac:
```shell script
brew install pulseaudio mpv libmpv
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
## Commands
1. [s] - searching and playing the song from YouTube
    - example: s Metallica

2. [p] - play\pause
3. [+] - play next song
4. [-] - play previous song
5. [+X] - seeking forward 
    - example or seeking forward for 30 seconds: +30
6. [-X] - seeking backward
    - example or seeking backward for 30 seconds: -30
7. [pl] - showing last searched results
8. [plX] - play song from search result bu ID
    - example of playing song no 10: pl10
9. [sp] - change of speed from 1 to 4
    - example of playing 2 times faster: sp2  
10. [vX] - set the volume
    - example of 50%: v50    
11. [v] - version
12. [q] - quit the bot     

### Notes:

Telegram - <a href="https://t.me/TT5Link"> TT5Link</a>

Good Luck:
Котяра 🐾


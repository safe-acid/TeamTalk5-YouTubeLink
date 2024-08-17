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
### Initiate OAuth
When you run the bot first time you need authorize your device where bot is installed.
Run the bot and perform your first search, send the message
```shell script
s metallica
```
You will get an otput in your terminal:
```shell script
[youtube+oauth2] oauth2: Initializing OAuth2 Authorization Flow
[youtube+oauth2] To give yt-dlp access to your account, go to
https://www.google.com/device  and enter CODE ALT-SZD-VCD
```
Open URL, enter your CODE and authorize YouTube access your Google Account

## Commands
1. [s] - searching and playing the song from YouTube, you could drop youtube links and live links as well
    - example: s Metallica 
    - example: s https://www.youtube.com/watch?v=X4bgXH3sJ2Q

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
11. [?] - check current volume    
12. [f+] - add song to favorite list
13. [fl] - check favorite list
14. [fpX] - play song by id from favorite list
    - example fp10
15. [f-X] - remove song from favorite list
    - example f-10
16. [v] - version
17. [q] - quit the bot     

### Notes:

Telegram - <a href="https://t.me/TT5Link"> TT5Link</a>

Good Luck:
Котяра 🐾


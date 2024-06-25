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
API key could be created for free in <a href = "https://console.cloud.google.com/" Google Cloud Console</a>
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

### Release notes version:
1.0 - initial release

Telegram - <a href="https://t.me/TT5Link"> TT5RadioLink</a>

Good Luck:
Котяра 🐾


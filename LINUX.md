# 🛠️ Installation from zero on Linux Ubuntu 22+, Debian 12+

```shell script
sudo apt update
```
### ✅ Check in python is installed
```shell script
python3 --version 
```
### 🐍 Install python if need it
```shell script
sudo apt install python3
```
### ✅ Check if pip installed
```shell script
pip --version
```
### ➕ Instal pip if need it
```shell script
sudo apt install python3-pip
```
### 🛠️ Install git
```shell script
sudo apt install git
```
### 🔊 Install pulse audio, mpv and libmpv-dev
Linux
```shell script
sudo apt install -y pulseaudio mpv libmpv-dev
```

### ▶️ Start pulseaudio
```shell script
pulseaudio --start
```
### 🎙️ Add Virtual audio devices
```shell script
pactl load-module module-null-sink sink_name=Source
pactl load-module module-virtual-source source_name=VirtualMic master=Source.monitor
```
#### ✅ After steps above you shoud get number IDs after creating null-sinks, it means all goes well,create config file
```shell script
nano ~/.config/pulse/default.pa 
```
### 🛠️ Add configuratioon into default.pa and save the file 
```shell script
# include the default.pa pulseaudio config file
.include /etc/pulse/default.pa

# null sink
.ifexists module-null-sink.so
load-module module-null-sink sink_name=Source
.endif

# virtual source
.ifexists module-virtual-source.so
load-module module-virtual-source source_name=VirtualMic master=Source.monitor
.endif
```
### 🔄 Reload Systemd Daemon
After making these changes, reload the systemd user daemon:
```shell script
systemctl --user daemon-reload
```
### Enable and Start PulseAudio Service
```shell script
systemctl --user enable pulseaudio
systemctl --user start pulseaudio
```

### 📂 Clone the repository
```shell script
git clone https://github.com/safe-acid/TeamTalk5-YouTubeLink.git
```
### 📁 Change to the repository directory
```shell script
cd TeamTalk5-YouTubeLink
```

### 🐍 Set up a virtual environment
```shell script
python3 -m venv .env
```

### Activate the virtual environment
```shell script
source .env/bin/activate
```

### 📦 Install the required dependencies
```shell script
pip install -r requirements.txt
```

### ⚙️ Run the setup script
```shell script
python3 setup.py
```

### 🔍 Check Audio ID of Device Name: Virtual Source VirtualMic on Monitor
```shell script
python3 devices.py
```
### 🛠️ Setup you server settings, number of Audio ID and API Key
```shell script
nano config.py
```
### ▶️ Run the bot
```shell script
python3 youtube_main.py
```
### 🌐 Initiate OAuth (NOT SUPPORTED ANYMORE)
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
Open URL, enter your CODE and authorize YouTube access to your Google Account

### 🍪 Use Cookies (optional)
If you want to use cookies, set the value to True.
* 1. Download the plugin for Google Chrome: Get cookies.txt. 
       https://chromewebstore.google.com/detail/get-cookiestxt-clean/ahmnmhfbokciafffnknlekllgcnafnie?pli=1
* 2. Open YouTube and play any video.
* 3. In the plugin, select "Export All Cookies."
* 4. Copy all_cookies.txt to the root of the project.
    
* 📝 NOTES: Close the browser and do not use it; otherwise, the cookies will be refreshed and become invalid.

### 🛡️ Run the bot as servce 
* Read instructon in systemd/system/README.md

# 📬 Notes:
Telegram - <a href="https://t.me/TT5Link"> TT5Link</a>

Good Luck:
Котяра 

# Installation from zero on Linux Ubuntu 22+, Debian 12+

```shell script
sudo apt update
```
### Check in python is installed
```shell script
python3 --version 
```
### Install python if need it
```shell script
sudo apt install python3
```
### Check if pip installed
```shell script
pip --version
```
### Instal pip if need it
```shell script
sudo apt install python3-pip
```
### Install git
```shell script
sudo apt install git
```
### Install pulse audio, mpv and libmpv-dev
Linux
```shell script
sudo apt install -y pulseaudio mpv libmpv-dev
```

### Start pulseaudio
```shell script
pulseaudio --start
```
### Add Virtual audio devices
```shell script
pactl load-module module-null-sink sink_name=Source
pactl load-module module-virtual-source source_name=VirtualMic master=Source.monitor
```
#### After steps above you shoud get number IDs after creating null-sinks, it means all goes well,create config file
```shell script
nano ~/.config/pulse/default.pa 
```
### Add configuratioon into default.pa and save the file 
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
### Reload Systemd Daemon
After making these changes, reload the systemd user daemon:
```shell script
systemctl --user daemon-reload
```
### Enable and Start PulseAudio Service
```shell script
systemctl --user enable pulseaudio
systemctl --user start pulseaudio
```

### Clone the repository
```shell script
git clone https://github.com/safe-acid/TeamTalk5-YouTubeLink.git
```
### Change to the repository directory
```shell script
cd TeamTalk5-YouTubeLink
```

### Set up a virtual environment
```shell script
python3 -m venv .env
```

### Activate the virtual environment
```shell script
source .env/bin/activate
```

### Install the required dependencies
```shell script
pip install -r requirements.txt
```

### Run the setup script
```shell script
python3 setup.py
```

### Check Audio ID of Device Name: Virtual Source VirtualMic on Monitor
```shell script
python3 devices.py
```
### Setup you server settings, number of Audio ID and API Key
```shell script
nano config.py
```
### Run the bot
```shell script
python3 youtube_main.py
```

Good Luck: Котяра 🐾
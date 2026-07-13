# Run YouTubeLink with Docker

This guide runs the TeamTalk YouTube bot in a Docker container on Linux, Windows, or macOS. Docker installs Python, TeamTalk SDK, PulseAudio, MPV, FFmpeg, and the required Python packages inside the image.

## 1. Install Docker

- **Windows:** Install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) and use Linux containers.
- **macOS:** Install [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/).
- **Linux:** Install [Docker Engine](https://docs.docker.com/engine/install/) and the Docker Compose plugin for your distribution.

Verify that Docker and Compose are available:

```bash
docker --version
docker compose version
```

## 2. Configure the bot

Open `config.py` and update at least these settings:

| Setting | Description | Example |
| --- | --- | --- |
| `host` | TeamTalk server address | `"tt.example.com"` |
| `tcpPort` | TeamTalk TCP port | `10333` |
| `udpPort` | TeamTalk UDP port | `10333` |
| `botName` | Bot nickname | `"@YouTube"` |
| `username` | TeamTalk account username | `"musicbot"` |
| `password` | TeamTalk account password | `"secret"` |
| `ChannelName` | Full TeamTalk channel path | `"/Music"` |
| `ChannelPassword` | Channel password, or an empty string | `""` |
| `API_KEYS` | One or more YouTube Data API v3 keys | `["YOUR_KEY"]` |
| `audioInputID` | TeamTalk input device ID | `6` |

The YouTube Data API v3 must be enabled for the Google project that owns the API key.

> Keep real passwords, API keys, and cookie files private. Do not commit them to a public repository.

### Find the Docker audio input ID

The default configuration normally uses device ID `6`. If the bot connects but produces no sound, start it and list the devices inside the container:

```bash
docker compose up -d --build
docker exec -it tt5-youtubelink python devices.py
```

Copy the ID for `VirtualMic` into `audioInputID` in `config.py`, then rebuild the image.

## 3. Choose the bot language

English is used by default.

To use Russian, open `docker-compose.yml` and uncomment this line by removing its first `#`:

```yaml
# command: ["--language", "ru"]
```

After uncommenting it, the line must look like this:

```yaml
command: ["--language", "ru"]
```

Comment the line again to return to English.

## 4. Build and start

Run this command from the project directory containing `docker-compose.yml`:

```bash
docker compose up -d --build
```

The first build takes longer because Docker downloads the base image, system packages, Python packages, and TeamTalk SDK.

## 5. Check that the bot started

Follow the live logs:

```bash
docker compose logs -f tt5-youtubelink
```

Press `Ctrl+C` to leave the log view. This does not stop the bot.

Check the container state:

```bash
docker compose ps
```

The service should show as running. You can then send `h` to the bot in TeamTalk to see its commands.

## File-download command

When a song is selected, send `d` to download it as `yt_<song name>.mp3` and upload it to the current channel's files.

For this command to work:

- the bot must use a registered TeamTalk account;
- the account must have permission to upload files;
- file sharing must be enabled on the server;
- the channel must have enough free file quota; and
- a file with the same name must not already exist in the channel.

The Docker image already includes FFmpeg for MP3 conversion. If TeamTalk rejects an upload, the bot sends the server's error message to the requesting user.

## Common management commands

### Restart the bot

```bash
docker compose restart tt5-youtubelink
```

### Stop and remove the container

```bash
docker compose down
```

This removes the container but keeps the locally built image.

### Start it again

```bash
docker compose up -d
```

### Rebuild after changing code or configuration

`config.py` is copied into the image during the build. Rebuild after editing it:

```bash
docker compose up -d --build
```

### Show recent logs

```bash
docker compose logs --tail=100 tt5-youtubelink
```

## YouTube cookies

Cookies are only needed when YouTube blocks requests from the server's IP address.

1. Export YouTube cookies to `all_cookies.txt` in the project directory.
2. Set `cookies = True` in `config.py`.
3. Close the browser session used to export the cookies so they are not refreshed.
4. Rebuild the container:

```bash
docker compose up -d --build
```

Treat `all_cookies.txt` like a password and never publish it.

## Update yt-dlp

To install the latest version persistently, rebuild the image without Docker's package cache:

```bash
docker compose build --no-cache
docker compose up -d
```

For a faster temporary update in an already-running container, use:

```bash
docker exec -u app -it tt5-youtubelink python -m pip install --user --upgrade yt-dlp
docker compose restart tt5-youtubelink
```

Verify the installed version:

```bash
docker exec -u app -it tt5-youtubelink python -m yt_dlp --version
```

The temporary update is lost the next time the image is rebuilt.

## Troubleshooting

### The container immediately stops or restarts

Read the latest error:

```bash
docker compose logs --tail=200 tt5-youtubelink
```

Check the TeamTalk server settings, channel path, credentials, API key, and `audioInputID` in `config.py`.

### The bot connects but there is no audio

List the devices and confirm that `audioInputID` points to `VirtualMic`:

```bash
docker exec -it tt5-youtubelink python devices.py
```

After changing the ID, rebuild with `docker compose up -d --build`.

### You changed `config.py`, but nothing changed in the bot

A normal restart uses the old image. Rebuild it:

```bash
docker compose up -d --build
```

### YouTube search or playback fails

Check the logs, verify the YouTube Data API v3 key, and update yt-dlp. If YouTube is blocking the server IP, configure cookies as described above.

### MP3 upload fails

Read the private error sent by the bot. Typical causes are missing upload permission, disabled server file sharing, insufficient channel quota, or a duplicate filename.

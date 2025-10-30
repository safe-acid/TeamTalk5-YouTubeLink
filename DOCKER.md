# Install Docker on Linux

# 1. Install Docker Engine and Compose 
```shell script
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
# 2. Verify installation
```shell script
docker --version
docker compose version
```




# General Installation of YouTubeLink (Windows,Mac, Linux with installed Docker)
## 1. Setup config file
Located on root project "config.py"

## 2. Build and run Docker container
```shell script
docker compose up -d --build
```
## 3.Check logs
```shell script
docker compose logs -f tt5-youtubelink
```

# Helpers
## 4. Upgrade yt-dlp inside the running container (user = app)
```shell script
docker exec -u app -it tt5-youtubelink python -m pip install --user --upgrade yt-dlp
```

## 5. Verify version
```shell script
docker exec -u app -it tt5-youtubelink yt-dlp --version
```

## 6. Upgrade multiple packages at once
```shell script
docker exec -u app -it tt5-youtubelink python -m pip install --user --upgrade yt-dlp requests py7zr google-api-python-client
```

## 7. Restart the container (apply clean state)
```shell script
docker compose restart tt5-youtubelink
```




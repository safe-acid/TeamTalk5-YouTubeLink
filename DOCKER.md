# Installation on Docker
## 1. Setup config file
Located on root project config.py

## 2.Build and run Docker container
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



## 📁 Adjust the Service File

Open the youtube_user1.service file.
Modify the following fields:
Replace user1 with your username.

* Update the WorkingDirectory path to the location of your project:
```shell script
/home/<your_username>/TeamTalk5-YouTubeLink
```
* Ensure the ExecStart command correctly activates your virtual environment and runs the bot:

```shell script
source /home/<your_username>/TeamTalk5-YouTubeLink/.env/bin/activate && python3 -m youtube_main.py
```

## 📝 Use a Descriptive Service Name

To easily identify the running service, name it descriptively, e.g., youtube_<username>.service

## 📂 Deploy the Service File

* Place the modified service file in one of the following directories:
* System-wide services:
```shell script
/etc/systemd/system/
```
## ⚙️ Reload and Enable the Service

Run the following commands to register and enable the service:
```shell script
sudo systemctl daemon-reload
sudo systemctl enable youtube_user1.service
```

## ▶️ Start the Service
* Start the service with:
```shell script
sudo systemctl start youtube_user1.service
```
🔍 Check Service Status

## Verify the status of the service:
```shell script
sudo systemctl status youtube_user1.service
```
import sys, os, platform, ctypes, logging, time, threading, argparse, json
from config import Config as conf
from typing import Optional
from messages import messages
from mpv_controller import MPV_Controller
from collections import defaultdict
import library
from library import ttstr
# Add logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTClient:
    def __init__(self, host, tcpPort, udpPort, nickName, userName, password):
        self.host = host
        self.tcpPort = tcpPort
        self.udpPort = udpPort
        self.nickName = nickName
        self.userName = userName
        self.password = password
        self.tt = library.TeamTalk5.TeamTalk()
        self.tt.onConnectSuccess = self.onConnectSuccess
        self.tt.onConnectionLost = self.onConnectionLost
        self.tt.onCmdMyselfLoggedIn = self.onCmdMyselfLoggedIn
        self.tt.onCmdUserTextMessage = self.onCmdUserTextMessage
        self.connected = False   # Flag to track connection status
        self.reconnect_delay =  10 # Set reconnect interval to 10 seconds
        self.reconnect_thread = threading.Thread(target=self.reconnect_loop, daemon=True)
        self.reconnect_thread.start()
       
        self.admin = conf.admin  # Initialize the admin flag
        self.last_message_time = defaultdict(lambda: 0)  # Track last message time for each user

        # Instance of MPV_Controller with the callback
        self.mpv = MPV_Controller(self.update_nickname_with_remaining_time, self.update_status_with_song_name)

    def enable_voice_transmission(self) -> None:
        self.tt.enableVoiceTransmission(True)
        
    def disable_voice_transmission(self) -> None:
        self.tt.enableVoiceTransmission(False)
    
    def start(self):
        self.connect()
                   
    def connect(self):
        self.tt.connect(self.host, self.tcpPort, self.udpPort)

    def onConnectSuccess(self):
        self.connected = True # Connection established
        self.tt.doLogin(self.nickName, self.userName, self.password, ttstr(conf.botName))
        time.sleep(1)
              
    def onConnectionLost(self):
        self.mpv.stop_playback()
        self.tt.doChangeStatus(0, ttstr(self.get_message("info")))  
        self.connect()
        self.connected = False
        logger.info("Connection lost.")
        
    def set_input_device(self, id: int) -> None:
        self.tt.initSoundInputDevice(id)  
    
    def onCmdMyselfLoggedIn(self, userID, userAccount):
        print(f"Hello {userAccount.szUsername}. Your User ID is {userID}")
        time.sleep(2.0)
        channelID = self.tt.getChannelIDFromPath(ttstr(conf.ChannelName))
        print(channelID)
        time.sleep(1.0)
        self.tt.doJoinChannelByID(channelID, ttstr(conf.ChannelPassword))
        self.tt.doChangeStatus(0, ttstr(self.get_message("info")))     
        self.set_input_device(conf.audioInputID)
       
    def onChannelMessage(self, fromUserID, fromUserName, channelID, msgText):
         print(f"Channel message in channelid {ttstr(channelID)} from userid {ttstr(fromUserID)} username: {ttstr(fromUserName)} {ttstr(msgText)}")

    def change_nickname(self, nickname):
        self.tt.doChangeNickname(ttstr(nickname))
    #call back function 
    def update_nickname_with_remaining_time(self, remaining_time):
        if conf.showTime:
            new_nickname = f"{ttstr(self.nickName)} {remaining_time}"
            self.change_nickname(new_nickname)
        else:
            play_status = self.mpv.player_status
            self.change_nickname(f"{conf.botName} {play_status}")
        
        
     #callback function    
    def update_status_with_song_name(self, name):
        self.tt.doChangeStatus(0, ttstr(name) )
        

    def onCmdUserTextMessage(self, message):
        msgType = message.nMsgType
        if msgType == library.TeamTalk5.TextMsgType.MSGTYPE_USER:
            self.onUserMessage(message.nFromUserID, message.szFromUsername, message.szMessage)
        if msgType == library.TeamTalk5.TextMsgType.MSGTYPE_CHANNEL:
            self.onChannelMessage(message.nFromUserID, message.szFromUsername, message.nChannelID, message.szMessage)
        #if msgType == library.TeamTalk5.TextMsgType.MSGTYPE_BROADCAST:
            #self.onBroadcastMessage(message.nFromUserID, message.szFromUsername, message.szMessage)  
    
    # Grabbing users in channels
    def get_users_in_channels(self):
        user_ids = []
        bot_chanelId = self.tt.getMyChannelID()
        users_in_channel = self.tt.getChannelUsers(bot_chanelId)
        # Check if users_in_channel is not None and access user information accordingly
        if users_in_channel is not None:
            for user in users_in_channel:
                # Append each user ID to the list
                user_ids.append(user.nUserID)       
        return user_ids
      
    # Checking is user who sent message in channel
    def userID_inChannel(self, id_to_check):
        # Call the function to get the list of user IDs
        user_ids = self.get_users_in_channels()    
        if id_to_check in user_ids:
            return True
        return False 
   
    def isUserAdmin(self, user_id):
        user = self.tt.getUser(user_id)
        if user.uUserType == 2:
            return True
        return False
    
    def anonymous(self, szFromUsername):
        if len(szFromUsername) == 0:
            return False
        return True   
    
    def get_message(self, key):
        if key in messages:
            return messages[key][current_language]
        else:
            # Handle missing message key
            return "Message not found."
    
    # Player status        
    def isPlaying(self):
        if self.mpv.player_status == "playing":
            return True

    # Player status        
    def isPaused(self):
        if self.mpv.player_status == "paused":
            return True

    # Player status        
    def isStop(self):
        if self.mpv.player_status == "stopped":
            return True
    
    def send_message(self, text: str, user: Optional[library.User] = None, type: int = 1) -> None:
        message = library.TeamTalk5.TextMessage()
        message.nFromUserID = self.tt.getMyUserID()
        message.nMsgType = type
        message.szMessage = ttstr(text)
       
        if type == 1:
            if isinstance(user, int):
                message.nToUserID = user
            else:
                message.nToUserID = user.id
        elif type == 2:
            message.nChannelID = self.tt.getMyChannelID()
        self.tt.doTextMessage(message)
    
    # Read search_list.json
    def read_search_results(self):
        try:
            with open('search_list.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    # Prepare list to user check the list - command pl
    def send_search_results(self, fromUserID):
        search_results = self.read_search_results()
        global_index = 1
        for i in range(0, len(search_results), 3):
            chunk = search_results[i:i + 3]
            message = "\n".join([f"{global_index + j}. {item['name']}" for j, item in enumerate(chunk)])
            global_index += len(chunk)
            self.send_message(message, fromUserID, 1)

    # Get song by ID from search_json
    def get_song_by_number(self, number):
        search_results = self.read_search_results()
        if 1 <= number <= len(search_results):
            return search_results[number - 1]
        else:
            return None

    # Play song by ID
    def play_song_by_number(self, fromUserID, number):
        song = self.get_song_by_number(number)
        if song:
            song_name = song['name']
            song_url = song['url']
            threading.Thread(target=self.youtube_search_and_play_thread, args=(song_url, fromUserID, song_name)).start()
        else:
            self.send_message("Invalid song number. Please try again.", fromUserID, 1)        
    
    def onUserMessage(self, fromUserID, fromUserName, msg):
        anonymous = self.anonymous(fromUserName)
        userInChanel = self.userID_inChannel(fromUserID)
        msg = ttstr(msg)
        current_time = time.time()
        # Check for flooding
        if current_time - self.last_message_time[fromUserID] < conf.msgTimeDelay:
            self.send_message(self.get_message("flood_message"), fromUserID, 1)
        else:
            # Update last message time
            self.last_message_time[fromUserID] = current_time

            # User must be in channel and not anonymous
            if anonymous and userInChanel:
                if self.isUserAdmin(fromUserID) or not self.admin:
                    # About
                    if msg.lower() == "v":
                        self.send_message(self.get_message("about"), fromUserID, 1)
                    # Help
                    elif msg.lower() == "h":
                        self.send_message(self.get_message("help"), fromUserID, 1)
                        self.send_message(self.get_message("help1"), fromUserID, 1)
                    # Search and play   
                    elif msg.lower().startswith("s ") and len(msg.lower()) > 4:
                        search_query  = msg[2:].strip()
                        self.mpv.stop_playback()
                        self.send_message(f"{ttstr(fromUserName)}{self.get_message('requested')}{search_query}", fromUserID, 2)
                        self.send_message(self.get_message("searching_in_yt"), fromUserID, 1)
                        threading.Thread(target=self.youtube_search_and_play_thread, args=(search_query, fromUserID)).start()
                        # time.sleep(5)
                        # play_status = self.mpv.player_status
                        # self.change_nickname(f"{conf.botName} {play_status}")
                        
                    # Next song
                    elif msg == "+":
                        self.send_message(self.get_message("next_song"), fromUserID, 1)
                        song_name = self.mpv.play_next_song()
                        if song_name:                   
                            self.send_message(f"{self.get_message('playing')} {song_name}", fromUserID, 1)
                            # self.tt.doChangeStatus(0, ttstr(f"{song_name}"))
                    # Previous song
                    elif msg == "-":
                        self.send_message(self.get_message("prev_song"), fromUserID, 1)
        
                        song_name = self.mpv.play_previous_song()
                        if song_name:
                            self.send_message(f"{self.get_message('playing')} {song_name}", fromUserID, 1)
                            #self.tt.doChangeStatus(0, ttstr(f"{song_name}"))
                    # Rewind forward
                    elif msg.startswith("+") and len(msg) > 1 and self.isPlaying:
                        try:
                            seconds = int(msg[1:])
                            self.mpv.seek_forward(seconds, fromUserID, self.handle_message)
                        except ValueError:
                            self.send_message(self.get_message("wrong_search_format"), fromUserID, 1)
                    # Rewind backward
                    elif msg.startswith("-") and len(msg) > 1 and self.isPlaying:
                        try:
                            seconds = int(msg[1:])
                            self.mpv.seek_backward(seconds, fromUserID, self.handle_message)
                        except ValueError:
                            self.send_message(self.get_message("wrong_search_format"), fromUserID, 1)
                    # Pause/play
                    elif msg.lower() == "p":
                        self.mpv.pause_resume_playback()
                        play_status = self.mpv.player_status
                        self.change_nickname(f"{conf.botName} {play_status}")
                    # Quit
                    elif msg.lower() == "q":
                        self.disable_voice_transmission()
                        self.mpv.stop_playback()
                        self.send_message(f"бот уснул", fromUserID, 1)
                        self.tt.doChangeStatus(0, ttstr(self.get_message("info")))  
                    # Adjust speed 
                    elif msg.lower().startswith("sp") and len(msg) > 2:  # Check for at least one digit after "sp"
                        try:
                            speed = float(msg[2:]) 
                            if 1 <= speed <= 4.:
                                self.mpv.set_speed(speed)
                                self.send_message(f"{self.get_message('speed_set_to')}  {speed}", fromUserID, 2)
                            else:
                                self.send_message(self.get_message("wrong_speed"), fromUserID, 1)
                        except ValueError:
                            self.send_message((self.get_message("wrong_speed_format")), fromUserID, 1)    
                    # Volume control
                    elif msg.lower().startswith("v") and len(msg) > 1:  # Check for at least one digit after "v"
                        try:
                            volume_level = int(msg[1:])  # Extract digits after "v"
                            if 0 <= volume_level <= conf.max_volume:   
                                self.mpv.set_volume(volume_level)
                                self.send_message(f"{self.get_message('vol_set_to')}  {volume_level}", fromUserID, 2)
                            else:
                                self.send_message(self.get_message("wrong_volume"), fromUserID, 1)
                        except ValueError:
                            self.send_message((self.get_message("wrong_volume_format")), fromUserID, 1)  
                    # get volume
                    elif msg.lower() == "?":
                        self.send_message(f"vol={self.mpv.get_volume()}", fromUserID, 1) 
                    # Show saved search playlist
                    elif msg.lower() == "pl":
                        self.send_search_results(fromUserID)
                    # Play from last searched playlist
                    elif msg.lower().startswith("pl") and len(msg) > 2:
                        song_number = int(msg[2:])  # Extract digits after "pl"
                        self.play_song_by_number(fromUserID, song_number)  
                    
                    #check i admin allows user fav list for all users or selectged
                    if not conf.favUsers or ttstr(fromUserName) in conf.favUsers:       
                          
                        # add song to favorite
                        if msg.lower() == "f+":
                            current_song_name = self.mpv.current_song_name  # You need to implement this attribute in your MPV_Controller
                            current_song_url = self.mpv.current_song_url  # Likewise, this needs to be implemented
                            self.add_to_favorites(fromUserID, fromUserName, current_song_name, current_song_url)
                        # get fav list
                        elif msg.lower() == "fl":
                            self.get_fav_songs_list(fromUserID,fromUserName)
                        # delete item from favorite
                        elif msg.lower().startswith("f-"):
                            song_number_str = msg[2:].strip() 
                            if song_number_str.isdigit():
                                song_number = int(song_number_str)
                                self.delete_favorite_song(fromUserID, fromUserName, song_number)
                            else:
                                self.send_message(f"{self.get_message('fav_invalid_song')} f-.", fromUserID, 1)
                  
                        # play song from from favorite list
                        elif msg.lower().startswith("fp"):
                            song_number_str = msg[2:].strip() 
                            if song_number_str.isdigit():
                                song_number = int(song_number_str)
                                self.play_fav_song_by_number(fromUserID, fromUserName, song_number)
                            else:
                                self.send_message(f"{self.get_message('fav_invalid_song')} fp.", fromUserID, 1)
                    
                                             
    # user add song to favorite
    def add_to_favorites(self, fromUserID, fromUserName, song_name, song_url):
        # Create the directory if it does not exist
        favorites_dir = os.path.join(os.getcwd(), 'favorites')
        os.makedirs(favorites_dir, exist_ok=True)

        # Define the file path
        file_path = os.path.join(favorites_dir, f"{ttstr(fromUserName)}.json")

        # Check if the file exists
        if os.path.exists(file_path):
            # Read the existing data
            with open(file_path, 'r', encoding='utf-8') as file:
                favorites = json.load(file)
        else:
            # Initialize an empty list if the file does not exist
            favorites = []
       
        if len(favorites) >= conf.maxFavItems:
            self.send_message(f"{self.get_message('fav_limit_error')} {conf.maxFavItems}", fromUserID, 1)
            return
                 
        # Append the new favorite song
        favorites.append({
            "name": song_name,
            "url": song_url
        })

        # Write the updated list back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(favorites, file, indent=4, ensure_ascii=False)

        # Notify the user
        self.send_message(self.get_message('fav_song_added'), fromUserID, 1)
        
    #get favorities list 
    def get_fav_songs_list(self, fromUserID, fromUserName):
    
        filepath = os.path.join('favorites', f"{ttstr(fromUserName)}.json")
        # Check if the file exists
        if not os.path.exists(filepath):
            self.send_message(self.get_message('fav_no_list'), fromUserID, 1)
            return
        try:
            # Load the favorites from the file
            with open(filepath, 'r', encoding='utf-8') as f:
                favorites = json.load(f)           
            # Check if there are any favorites
            if not favorites:
                self.send_message(self.get_message('fav_empty_list'), fromUserID, 1)
                return
            # Send the favorites in chunks of 3 songs
            global_index = 1
            for i in range(0, len(favorites), 3):
                chunk = favorites[i:i + 3]
                message = "\n".join([f"{global_index + j}. {item['name']}" for j, item in enumerate(chunk)])
                self.send_message(message, fromUserID, 1)
                global_index += len(chunk)
        except json.JSONDecodeError:
            self.send_message(self.get_message('fav_format_err'), fromUserID, 1)
        except Exception as e:
            self.send_message(f"An error occurred: {str(e)}", fromUserID, 1)
            
    #delete song from favorities
    def delete_favorite_song(self, fromUserID, fromUserName, song_number):
        
        file_path = os.path.join('favorites', f"{ttstr(fromUserName)}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                favorites = json.load(file)
            if 1 <= song_number <= len(favorites):
                removed_song = favorites.pop(song_number - 1)  # Adjust for zero-based index
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(favorites, file, indent=4, ensure_ascii=False)
                self.send_message(f"{self.get_message('fav_del')} {removed_song['name']}", fromUserID, 1)
            else:
                self.send_message("Invalid song number. Please check the favorite list and try again, use command: fl", fromUserID, 1)
        else:
            self.send_message("No favorites list found.", fromUserID, 1) 
            return None

    # Play favorite sng song by ID
    def play_fav_song_by_number(self, fromUserID, fromUserName, number):
        song = self.get_fav_song_by_number(fromUserName, number)
    
        if song:
            song_name = song['name']
            song_url = song['url']
            threading.Thread(target=self.youtube_search_and_play_thread, args=(song_url, fromUserID, song_name)).start()
        else:
            self.send_message(self.get_message('fav_inval_err'), fromUserID, 1) 
    
    # Get favoritge song by ID from search_json
    def get_fav_song_by_number(self,fromUserName, number):
        search_results = self.fav_read_search_results(fromUserName)
        if 1 <= number <= len(search_results):
            return search_results[number - 1]
        else:
            return None
    #read json favorite user list
    def fav_read_search_results(self, fromUserName): 
        file_path = os.path.join(os.getcwd(), 'favorites', f"{ttstr(fromUserName)}.json")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Log that no file was found for the user
            logging.info(f"No favorites file found for user: {fromUserName}")
            return []
        except json.JSONDecodeError:
            # Log if the file is found but cannot be decoded
            logging.error(f"Error decoding JSON for file: {file_path}")
            return []
        except Exception as e:
            # General exception handling to catch any other unforeseen errors
            logging.error(f"An unexpected error occurred while reading the favorites file: {str(e)}")
            return []
    
    # Search and play thread
    def youtube_search_and_play_thread(self, query, fromUserID, song_name=None):
        song = self.mpv.youtube_search_and_play(query)
        if song:
            self.enable_voice_transmission()
            # If user playing from saved search_list argument song_name is passed
            # If playing from search pass the song as argument 
            if song_name is None:
                song_name = song       
            self.send_message(f"{self.get_message('playing')} {song_name}", fromUserID, 1)
            #self.tt.doChangeStatus(0, ttstr(f"играет: {song_name}"))
        else:
            self.send_message(f"{self.get_message('search_empty')}", fromUserID, 1)                               
    
    # Define the handling method from other class
    def handle_message(self, message, fromUserID):
        self.send_message(message, fromUserID, 1)
        
    # Reconnect
    def reconnect_loop(self):
        while True:   
            if not self.connected:
                logger.info("Attempting to reconnect...")
                self.tt.disconnect()
                time.sleep(2)
                # Attempt to reconnect
                self.connect()
            time.sleep(self.reconnect_delay)    

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('--language', action='store', help='Select language (ru or en)', default="")
        args = parser.parse_args()
        
        # Set current_language based on the argument
        if args.language == "ru":
            current_language = "ru"
        elif args.language == "en":
            current_language = "en"
        else:
            # Handle unsupported languages (optional: log a warning or provide default language)
            current_language = "en"  # Assuming default to English
        
        ttClient = TTClient(ttstr(conf.host), conf.tcpPort, conf.udpPort, ttstr(conf.botName), ttstr(conf.username), ttstr(conf.password))
        
        # Start the TeamTalk client if not displaying devices
        time.sleep(1.5)
        ttClient.start()
        while True:
            ttClient.tt.runEventLoop()
                
    except KeyboardInterrupt:
        running = False

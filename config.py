class Config:
    #Version
    version = "2.5"
    sdk = "SDK 5.15a"

    #Server settings
    host = "tt5.live"
    tcpPort = 10333
    udpPort = 10333
    botName = "@YouTube"
    username = ""
    password = ""
    ChannelName = "/IT"
    ChannelPassword = ""
    
    #YouTube Api Key instruction in Telegram @
    API_KEYS = ["APIKEY_1", 
                "APIKEY_2", 
                "APIKEY_3",
                "APIKEY_4",
                "APIKEY_5",
                "APIKEY_6"
                ]
    

    #Audio Device ID - INT 
    audioInputID = 6
    #Audio Device ID - INT   
    max_volume = 75
    #Only admin can operaate this bot - Boolean        
    admin = False 
    #time in seconds when user can send message, avoid flood
    msgTimeDelay = 5
    #users nick names who allowed to add songs into favorite list
    #if epmpty - all registered could create favorite list
    favUsers = []
    #maximum songs in list
    maxFavItems = 100
    #Show or hide time when playing True/False avoid screen jumping
    showTime = True
    #Max search result per one request - INT
    max_search_number = 20
    #Login with OAuth is no longer supported
    oAuth = False
    
    #use the cookies if your server's IP is blocked by google
    cookies = False
    """
    If you want to use cookies, set the value to True.
    1. Download the plugin for Google Chrome: Get cookies.txt. 
       https://chromewebstore.google.com/detail/get-cookiestxt-clean/ahmnmhfbokciafffnknlekllgcnafnie?pli=1
    2. Open YouTube and play any video.
    3. In the plugin, select "Export All Cookies."
    4. Copy all_cookies.txt to the root of the project.
    
    NOTES:
    Close the browser and do not use it; otherwise, the cookies will be refreshed and become invalid.
    """
    
    
    current_key_index = 0
    @classmethod
    def get_api_key(cls):
        """Return the current API key and rotate to the next one if needed"""
        key = cls.API_KEYS[cls.current_key_index]
        cls.current_key_index = (cls.current_key_index + 1) % len(cls.API_KEYS)
        return key



    #Personal use // ignore below
    # Стерео 💭
    #ChannelName = "/! Xвосты без дела ✨"
    #ChannelName = "/!Jazz Cafe🎷"
    #ChannelName = "/!Small talk📚"
    #ChannelName = "/!White Panther🤍"
    #ChannelName = "/!Борщ 🥣"
    #ChannelName = "/!Дворец принцессы"
    #ChannelName = "/мур-мяу😍"

class Config:
    #Version
    version = "2.2"
    sdk = "SDK 5.15a"

    #Server settings
    host = "46.36.217.170"
    tcpPort = 10333
    udpPort = 10333
    botName = "@YouTube"
    username = ""
    password = ""
    ChannelName = "/IT"
    ChannelPassword = ""
    

    
    #Other settings
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
    
    #YouTube Api Key
    youtubeAPIkey = str("")  
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
    
             


    #Example
    # host = "46.89.217.170"
    # tcpPort = 10333
    # udpPort = 10333
    # botName = "_radioFM"
    # username = "open"
    # password = "open"
    # ChannelName = "/_Audio bot"
    # #ChannelPassword = "1112"
    # ChannelPassword = "private"
    # audioInputID = 6
    # max_volume = 50
    # admin = False 
    # msgTimeDelay = 5
    # youtubeAPIkey = str("AIzaSyCU6L_4VxmBRwsEQS8ApKwuWS9090900")
    # max_search_number = 20
    # favUsers = ["peri", "kot", "sergey"]
    # favLimit = 100

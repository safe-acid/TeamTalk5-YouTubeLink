class Config:
    #Version
    version = "1.5"
    sdk = "SDK 5.15a"

    #Server settings
    host = "46.36.217.170"
    tcpPort = 10555
    udpPort = 10555
    botName = "@YouTube"
    username = ""
    password = ""
    ChannelName = "/"
    ChannelPassword = ""
    
    #Other settings
    #Audio Device ID - INT 
    audioInputID = 100
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
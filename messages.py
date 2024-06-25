from config import Config as conf

messages = {
    "help_top": {
        "en": "Radio Selection:\n",
        "ru": "Выбор Радио:\n"
    },
    
    "help": {
        "en": "s: search the song name\np: pause\play\n+: next song\n-: previous song\nvX: set up the volume\nspX: set up speed from 1 to 4\npl: show last searches\nplX: play song by ID from last search\n+X: seek forward\n-X: seek backward see\nv: about\nq: exit",
        "ru": "s: поиск песни\np: пауза\воспроизведение\n+: следующий трек\n-: предыдущий трек\nvX: настройка громкости\nspX: настройка скорости от 1 до 4\npl: просмотр последнего поиска\nplX: выбор песни из последнего поиска\n+X перемотка\n-X перемотка\nv: версия\nq: выход"  
    },
    
     "info": {
        "en": "\"h\" help",
        "ru": "\"h\" справка"
    },
    
    "about": {
        "en": f"YoutTubeLink version: {conf.version}, {conf.sdk} - Котяра 🐾",
        "ru": f"YouTubeLink version: {conf.version}, {conf.sdk} - Котяра 🐾"
    },
    "vol_set_to": {
        "en": "Volume set to",
        "ru": "Громкость установлена на "
    },
    
    "wrong_volume": {
        "en": f"Invalid volume level. Please use a number from 0 to {conf.max_volume}",
        "ru": f"Неверный уровень громкости. Пожалуйста, используйте число от 0 до {conf.max_volume}"
    },
     
    "wrong_volume_format": {
        "en": f"Invalid volume command format. Use 'v' followed by a number from 0 to {conf.max_volume}",
        "ru": f"Неверный формат команды громкости. Используйте 'v' с числом от 0 до {conf.max_volume}"
    },
     "speed_set_to": {
        "en": "Speed set to",
        "ru": "Скорость устанаовлена "
    },
    
    "wrong_speed": {
        "en": f"Invalid speed level. Please use a number from 0 to 4",
        "ru": f"Неверный уровень скорости. Пожалуйста, используйте число от 0 до 4"
    },
     
    "wrong_speed_format": {
        "en": f"Invalid speed command format. Use 'sp' followed by a number from 0 to 4",
        "ru": f"Неверный формат команды громкости. Используйте 'sp' с числом от 0 до 4"
    },
    
    "flood_message": {
        "en": "Too fast, wait a bit.",
        "ru": "Слишком быстро. Подождите немного."
    },
    "searching_in_yt": {
        "en": "Searching in YouTube...",
        "ru": "Запрашиваем Youtube..."
    },
    "next_song": {
        "en": "next song",
        "ru": "следующий трек"
    },
    "prev_song": {
        "en": "previous song",
        "ru": "предыдущий трек"
    },
     "playing": {
        "en": "playing:",
        "ru": "играет:"
    },
      "wrong_search_format": {
        "en": "Invalid format. Please enter a number after the '+'.",
        "ru": "Неверный формат для перемотки вперед. Пожалуйста, введите число после '+'."
    },
       "blank": {
        "en": "",
        "ru": ""
    },
        
}
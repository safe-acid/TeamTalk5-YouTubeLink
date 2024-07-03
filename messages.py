from config import Config as conf

messages = {
   
    "help": {
        "en": "s: Search the song name.\np: Pause/play.\n+: Next song.\n-: Previous song.\nvX: Set the volume.\nspX: Set the speed from 1 to 4.\npl: Show last searches.\nplX: Play song by ID from last search.\n+X: Seek forward.\n-X: Seek backward.",
        "ru": "s: Поиск названия песни.\np: Пауза/воспроизведение.\n+: Следующая песня.\n-: Предыдущая песня.\nvX: Установить громкость.\nspX: Установить скорость от 1 до 4.\npl: Показать последний поиск.\nplX: Воспроизвести песню по ID из последнего поиска.\n+X: Перемотать вперёд.\n-X: Перемотать назад."
    },
    "help1": {
        "en": "f+: Add to favorites.\nfl: Favorite list.\nfpX: Play by ID from favorites.\nf-X: Remove by ID from favorites.\nv: About.\nq: Exit.",
        "ru": "f+: Добавить в избранное.\nfl: Список избранного.\nfpX: Воспроизвести по ID из избранного.\nf-X: Удалить по ID из избранного.\nv: О программе.\nq: Выход."
    },
    
     "info": {
        "en": "\"h\" help",
        "ru": "\"h\" справка",
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
        "en": "playing: ",
        "ru": "играет: "
    },
      "wrong_search_format": {
        "en": "Invalid format. Please enter a number after the '+'.",
        "ru": "Неверный формат для перемотки вперед. Пожалуйста, введите число после '+'."
    },
      
    "fav_invalid_song": {
        "en": "Invalid song number. Please provide a valid number after ",
        "ru": "Неверный номер песни. Пожалуйста, укажите номер после"
    },
    "fav_limit_error": {
        "en": "You have reached the maximum songs limit of: ",
        "ru": "Вы достигли максимального лимита песен:"
    },
    
       "fav_song_added": {
        "en": "Song added to your favorites.",
        "ru": "Песня добавлена ​​в избранное."
    },
       
    "fav_no_list": {
        "en": "No favorites list found.",
        "ru": "Список избранного не найден."
    },
    
    "fav_empty_list": {
        "en": "Your favorites list is empty.",
        "ru": "Ваш список избранного пуст."
    },
    
    "fav_format_err": {
        "en": "Failed to read your favorites list due to a formatting error.",
        "ru": "Не удалось прочитать список избранного из-за ошибки форматирования."
    },
    
    "fav_del": {
        "en": "Removed: ",
        "ru": "Удалено: "
    },
    
    "fav_inval_err": {
        "en": "Invalid song number. Please try again.",
        "ru": "Неверный номер песни. Пожалуйста, попробуйте еще раз."
    },

    "search_empty": {
        "en": "nothing found",
        "ru": "ничего не найдено"
    },
    
    "requested": {
        "en": " requested ",
        "ru": " запросил "
    },
    
     "blank": {
        "en": "",
        "ru": ""
    },
        
}
from config import Config as conf

messages = {
   
    "help": {
        "en": "s: Search the song name.\np: Pause/play.\nd: Download current song as MP3 to channel files.\n+: Next song.\n-: Previous song.\nvX: Set the volume.\nspX: Set the speed from 1 to 4.\npl: Show last searches.\nplX: Play song by ID from last search.\n+X: Seek forward.\n-X: Seek backward.",
        "ru": "s: Поиск названия песни.\np: Пауза/воспроизведение.\nd: Скачать текущую песню в MP3 в файлы канала.\n+: Следующая песня.\n-: Предыдущая песня.\nvX: Установить громкость.\nspX: Установить скорость от 1 до 4.\npl: Показать последний поиск.\nplX: Воспроизвести песню по ID из последнего поиска.\n+X: Перемотать вперёд.\n-X: Перемотать назад."
    },
    "help1": {
        "en": "?: Chck the volume\nf+: Add to favorites.\nfl: Favorite list.\nfpX: Play by ID from favorites.\nf-X: Remove by ID from favorites.\nv: About.\nq: Exit.",
        "ru": "?: Проверить громкость\nf+: Добавить в избранное.\nfl: Список избранного.\nfpX: Воспроизвести по ID из избранного.\nf-X: Удалить по ID из избранного.\nv: О программе.\nq: Выход."
    },
    
    "info": {
        "en": "\"h\" help",
        "ru": "\"h\" справка",
    },

    "download_started": {
        "en": "Downloading the current song as MP3...",
        "ru": "Скачиваю текущую песню в MP3..."
    },
    "download_busy": {
        "en": "Another MP3 download is already in progress. Please wait.",
        "ru": "Уже выполняется другая загрузка MP3. Подождите."
    },
    "download_no_song": {
        "en": "No song is currently available to download.",
        "ru": "Сейчас нет песни для скачивания."
    },
    "download_failed": {
        "en": "Failed to create the MP3 file.",
        "ru": "Не удалось создать MP3-файл."
    },
    "upload_started": {
        "en": "Uploading to channel files:",
        "ru": "Загружаю в файлы канала:"
    },
    "upload_complete": {
        "en": "MP3 added to channel files:",
        "ru": "MP3 добавлен в файлы канала:"
    },
    "upload_no_channel": {
        "en": "Cannot upload because the bot is not in a channel.",
        "ru": "Загрузка невозможна: бот не в канале."
    },
    "upload_failed_start": {
        "en": "TeamTalk could not start the file upload.",
        "ru": "TeamTalk не смог начать загрузку файла."
    },
    "upload_failed": {
        "en": "TeamTalk rejected the file upload:",
        "ru": "TeamTalk отклонил загрузку файла:"
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

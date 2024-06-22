import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import Config as conf

# Set up the YouTube API client
YOUTUBE_API_KEY = conf.youtubeAPIkey
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def search_you_tube(query):
    try:
        # Prepare the request with the specified parameters
        request = youtube.search().list(
            part='id,snippet',
            q=query,
            maxResults=conf.max_search_number,
            type='video'
        )
        
        # Execute the request and get the response
        response = request.execute()       
        search_results = []

        # Process each video in the response
        for video in response['items']:
            title = video["snippet"]["title"]
            video_id = video["id"]["videoId"]
           
            item = {
                'name': title,
                'value': f'https://www.youtube.com/watch?v={video_id}',
            }
            
            search_results.append(item)
        ##debug
        #print(search_results)
        return search_results
    
    except HttpError as e:
        if e.resp.status == 403:
            error_message = e._get_reason()
            print(f"Warning: Encountered 403 Forbidden - {error_message}")
            return None
        else:
            raise
        
# ##Test your Key for debug
# if __name__ == "__main__":
#     # Example query
#     search_you_tube("metallica")

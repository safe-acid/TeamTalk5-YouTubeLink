import json
import os
import time
import uuid
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import ExtractorError, traverse_obj
from config import Config as config

# OAuth2 credentials and scopes
CLIENT_ID = config.YOUR_CLIENT_ID
CLIENT_SECRET = config.YOUR_CLIENT_SECRET
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

class YouTubeOAuth2Handler(InfoExtractor):
    def __init__(self):
        super().__init__()
        self.token_file = 'oauth2_token.json'
        self.client_config = {
            "installed": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }

    def store_token(self, token_data):
        with open(self.token_file, 'w') as token:
            json.dump(token_data, token)

    def get_token(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as token:
                return json.load(token)
        return None

    def refresh_token(self, refresh_token):
        token_response = self._download_json(
            'https://oauth2.googleapis.com/token',
            video_id='oauth2',
            note='Refreshing OAuth2 token',
            data=json.dumps({
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token'
            }).encode(),
            headers={'Content-Type': 'application/json'}
        )
        if 'error' in token_response:
            raise ExtractorError(f"Failed to refresh access token: {token_response['error']}")
        return token_response

    def authorize(self):
        flow = InstalledAppFlow.from_client_config(self.client_config, SCOPES)
        creds = flow.run_local_server(port=0)
        return {
            'access_token': creds.token,
            'expires_in': creds.expiry.timestamp(),
            'refresh_token': creds.refresh_token,
            'token_type': 'Bearer'
        }

    def initialize_oauth(self):
        token_data = self.get_token()

        if token_data and token_data.get('expires_in', 0) < time.time():
            token_data = self.refresh_token(token_data['refresh_token'])
            self.store_token(token_data)

        if not token_data:
            token_data = self.authorize()
            self.store_token(token_data)

        return token_data

    def handle_oauth(self, request):
        token_data = self.initialize_oauth()
        request.headers.update({'Authorization': f"Bearer {token_data['access_token']}"})

    def _create_request(self, url):
        request = super()._create_request(url)
        self.handle_oauth(request)
        return request

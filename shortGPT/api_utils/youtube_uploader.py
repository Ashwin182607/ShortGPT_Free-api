from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from shortGPT.config.api_db import ApiKeyManager
import os
import json
import pickle

class YouTubeUploader:
    def __init__(self):
        self.youtube = None
        self.credentials = None
        self._initialize_youtube()

    def _initialize_youtube(self):
        """Initialize YouTube API client"""
        credentials_path = ApiKeyManager.get_api_key('YOUTUBE_CREDENTIALS')
        token_path = 'token.pickle'

        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.credentials = pickle.load(token)

        if not self.credentials or not self.credentials.valid:
            if credentials_path:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path,
                    ['https://www.googleapis.com/auth/youtube.upload']
                )
                self.credentials = flow.run_local_server(port=0)
                with open(token_path, 'wb') as token:
                    pickle.dump(self.credentials, token)
            else:
                raise ValueError("YouTube credentials not found. Please add them to API keys.")

        self.youtube = build('youtube', 'v3', credentials=self.credentials)

    def upload_video(self, video_path, title, description, tags=None, is_short=True):
        """Upload a video to YouTube"""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # Set up video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': '22'  # People & Blogs category
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }

        # Add #Shorts to title and description for vertical videos
        if is_short:
            body['snippet']['title'] = f"{title} #Shorts"
            if not body['snippet']['description'].endswith('#Shorts'):
                body['snippet']['description'] += '\n\n#Shorts'

        # Create media file upload
        media = MediaFileUpload(
            video_path,
            mimetype='video/mp4',
            resumable=True
        )

        # Execute upload request
        request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        # Upload the video
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")

        return response

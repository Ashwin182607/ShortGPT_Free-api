# shortGPT/api_utils/youtube_cc_api.py

import yt_dlp
from typing import List, Tuple
import random

def search_cc_videos(query: str, max_results: int = 5) -> List[Tuple[str, str, int]]:
    """Search for Creative Commons videos on YouTube
    Returns: List of (video_id, title, duration) tuples
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'default_search': 'ytsearch',
        'license': 'creativecommon'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Search for videos
        results = ydl.extract_info(f'ytsearch{max_results}:{query}', download=False)
        if not results or 'entries' not in results:
            return []
            
        videos = []
        for entry in results['entries']:
            if entry and 'duration' in entry:
                videos.append((
                    entry['id'],
                    entry.get('title', ''),
                    entry.get('duration', 0)
                ))
        return videos

def get_best_cc_video(query: str, target_duration: int = 15) -> str:
    """Get best matching Creative Commons video URL"""
    videos = search_cc_videos(query, max_results=5)
    if not videos:
        return None
        
    # Sort by duration difference from target
    videos.sort(key=lambda x: abs(x[2] - target_duration))
    
    # Get video URL for best match
    video_id = videos[0][0]
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best[height<=1080]'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
        return info.get('url')
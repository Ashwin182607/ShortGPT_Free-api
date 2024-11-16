from typing import Optional, List
from shortGPT.api_utils import pixabay_api, youtube_cc_api, pexels_api

class VideoSourceManager:
    """Manages multiple video sources with fallback options"""
    
    @staticmethod
    def get_best_video(query: str, orientation_landscape: bool = True, used_vids: List[str] = None) -> Optional[str]:
        """Try multiple video sources in order until a suitable video is found"""
        if used_vids is None:
            used_vids = []
            
        # Try Pixabay first (free)
        video_url = pixabay_api.get_best_video(query, orientation_landscape, used_vids)
        if video_url:
            return video_url
            
        # Try YouTube CC as backup (free)
        video_url = youtube_cc_api.get_best_cc_video(query)
        if video_url:
            return video_url
            
        # Fallback to Pexels if all else fails (requires API key)
        return pexels_api.getBestVideo(query, orientation_landscape, used_vids)

import requests
from shortGPT.config.api_db import ApiKeyManager

def search_images(query_string, per_page=20):
    """Search for images on Pixabay"""
    url = "https://pixabay.com/api/"
    params = {
        "key": ApiKeyManager.get_api_key("PIXABAY"),
        "q": query_string,
        "per_page": per_page,
        "image_type": "photo",
        "min_width": 1920,
        "min_height": 1080
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def search_videos(query_string, orientation_landscape=True):
    """Search for videos on Pixabay"""
    url = "https://pixabay.com/api/videos/"
    params = {
        "key": ApiKeyManager.get_api_key("PIXABAY"),
        "q": query_string,
        "per_page": 15,
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def get_best_video(query_string, orientation_landscape=True, used_vids=[]):
    """Get the best video match from Pixabay"""
    vids = search_videos(query_string, orientation_landscape)
    if not vids or 'hits' not in vids:
        return None
        
    videos = vids['hits']
    filtered_videos = []
    
    for video in videos:
        videos_list = video.get('videos', {})
        large = videos_list.get('large', {})
        
        if orientation_landscape:
            if large.get('width', 0) >= 1920 and large.get('height', 0) >= 1080:
                filtered_videos.append((video, large))
        else:
            if large.get('width', 0) >= 1080 and large.get('height', 0) >= 1920:
                filtered_videos.append((video, large))
    
    # Sort by duration
    sorted_videos = sorted(filtered_videos, key=lambda x: abs(15-int(x[0].get('duration', 0))))
    
    for video, video_file in sorted_videos:
        if video_file['url'] not in used_vids:
            return video_file['url']
            
    return None

def get_best_images(query, num_images=5):
    """Get best matching images from Pixabay"""
    response = search_images(query, per_page=num_images)
    if not response or 'hits' not in response:
        return []
        
    images = []
    for hit in response['hits']:
        if hit.get('largeImageURL'):
            images.append({
                'url': hit['largeImageURL'],
                'width': hit['imageWidth'],
                'height': hit['imageHeight']
            })
    
    return images
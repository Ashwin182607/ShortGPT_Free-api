import os
from typing import List
from shortGPT.engine.content_short_engine import ContentShortEngine
from shortGPT.config.languages import Language
from shortGPT.audio.voice_module import VoiceModule

class BatchShortEngine:
    def __init__(self, 
                 voice_module: VoiceModule,
                 background_video_name: str,
                 background_music_name: str,
                 num_videos: int = 5,
                 language: Language = Language.ENGLISH):
        self.voice_module = voice_module
        self.background_video_name = background_video_name
        self.background_music_name = background_music_name
        self.num_videos = num_videos
        self.language = language
        self.generated_videos = []
        
    def generate_batch(self, topic: str, output_dir: str):
        """Generate multiple short videos based on a topic
        
        Args:
            topic (str): The main topic to generate videos about (e.g., "reddit relationships")
            output_dir (str): Directory to save the generated videos
        """
        os.makedirs(output_dir, exist_ok=True)
        
        for i in range(self.num_videos):
            # Create a new short engine for each video
            engine = ContentShortEngine(
                short_type=f"{topic}_short_{i+1}",
                background_video_name=self.background_video_name,
                background_music_name=self.background_music_name,
                voiceModule=self.voice_module,
                language=self.language
            )
            
            # Generate the video
            for step in range(1, 12):  # Skip step 12 which is YouTube metadata
                if step in engine.stepDict:
                    engine.stepDict[step]()
            
            # Get the output video path
            video_path = engine.get_video_output_path()
            if video_path:
                # Use the generated title if available, otherwise extract from script
                title = getattr(engine, '_db_title', None) or self._extract_title_from_script(engine._db_script)
                title = self._clean_title(title)
                new_path = os.path.join(output_dir, f"{title}.mp4")
                
                # Move the video to the output directory with the new name
                if os.path.exists(video_path):
                    os.rename(video_path, new_path)
                    self.generated_videos.append(new_path)
    
    def _extract_title_from_script(self, script: str) -> str:
        """Extract a title from the script content
        
        Args:
            script (str): The video script
            
        Returns:
            str: A cleaned title suitable for a filename
        """
        # Take first line/sentence as title
        title = script.split('\n')[0].split('.')[0]
        
        return title
    
    def _clean_title(self, title: str) -> str:
        """Clean a title to make it suitable for a filename
        
        Args:
            title (str): The raw title
            
        Returns:
            str: A cleaned title suitable for a filename
        """
        # Clean the title for use as filename
        title = title.strip().lower()
        title = ''.join(c for c in title if c.isalnum() or c.isspace())
        title = title.replace(' ', '_')
        return title[:50]  # Limit length for filename

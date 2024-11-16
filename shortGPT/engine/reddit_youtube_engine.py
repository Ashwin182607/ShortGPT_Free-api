from shortGPT.config.reddit_types import RedditStoryType
from shortGPT.engine.content_engine import ContentEngine
from shortGPT.audio import VoiceModule
import openai

class RedditToYoutubeEngine(ContentEngine):
    def __init__(self, story_type, num_videos=1, vertical_format=True, tts_engine="EdgeTTS",
                 voice="en-US-AriaNeural", language="English", add_watermark=True,
                 custom_background=True, background_music=True):
        super().__init__()
        self.story_type = story_type
        self.num_videos = num_videos
        self.vertical_format = vertical_format
        self.tts_engine = tts_engine
        self.voice = voice
        self.language = language
        self.add_watermark = add_watermark
        self.custom_background = custom_background
        self.background_music = background_music

    def generate_story(self):
        """Generate a Reddit story using OpenAI"""
        prompt = f"Generate a realistic {self.story_type} story. Make it engaging and emotional."
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative writer specializing in Reddit stories."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message['content']

    def generate_metadata(self, story):
        """Generate metadata for the video"""
        prompt = f"Generate a catchy title and description for this Reddit {self.story_type} story:\n{story}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Generate engaging YouTube metadata."},
                {"role": "user", "content": prompt}
            ]
        )
        
        metadata = response.choices[0].message['content']
        title, description = metadata.split('\n\n', 1)
        return {
            'title': title.replace('Title: ', ''),
            'description': description.replace('Description: ', '')
        }

    def generate_videos(self):
        """Generate multiple Reddit story videos"""
        videos = []
        for _ in range(self.num_videos):
            story = self.generate_story()
            metadata = self.generate_metadata(story)
            
            video = self.create_video(story, metadata)
            videos.append(video)
        
        return videos

    def create_video(self, story, metadata):
        """Create a single video from a story"""
        # Initialize voice module based on engine choice
        voice_module = self._get_voice_module()
        
        # Generate audio from story
        audio_path = voice_module.generate_voice(story)
        
        # Get background video and music
        background = self._get_background()
        music = self._get_background_music() if self.background_music else None
        
        # Create video with all components
        video = self._create_video_with_components(
            audio_path,
            background,
            music,
            metadata,
            self.vertical_format,
            self.add_watermark
        )
        
        return video

    def _get_voice_module(self):
        """Initialize the appropriate voice module"""
        if self.tts_engine == "ElevenLabs":
            from shortGPT.audio.elevenlabs_voice_module import ElevenLabsVoiceModule
            return ElevenLabsVoiceModule(voice_name=self.voice)
        elif self.tts_engine == "EdgeTTS":
            from shortGPT.audio.edge_tts_voice_module import EdgeTTSVoiceModule
            return EdgeTTSVoiceModule(voice_name=self.voice)
        else:  # CoquiTTS
            from shortGPT.audio.coqui_voice_module import CoquiVoiceModule
            return CoquiVoiceModule(voice_name=self.voice)

    def _get_background(self):
        """Get background video based on story type and format"""
        if not self.custom_background:
            return None
            
        # Implementation for background video selection
        pass

    def _get_background_music(self):
        """Get background music based on story type"""
        # Implementation for background music selection
        pass

    def _create_video_with_components(self, audio, background, music, metadata, vertical, watermark):
        """Combine all components into final video"""
        # Implementation for video creation
        pass

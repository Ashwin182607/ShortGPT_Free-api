import os
from openai import OpenAI
from shortGPT.audio.voice_module import VoiceModule
from shortGPT.config.languages import Language
from shortGPT.config.api_db import ApiKeyManager

class OpenAIVoiceModule(VoiceModule):
    """
    Voice module that uses OpenAI's Text-to-Speech API.
    Provides high-quality voices at a lower cost than ElevenLabs.
    
    Available voices:
    - alloy: Neutral and balanced
    - echo: Warm and conversational
    - fable: British accent, expressive
    - onyx: Deep and authoritative
    - nova: Energetic and upbeat
    - shimmer: Clear and pleasant
    """
    
    def __init__(self, voice_name="nova", model="tts-1"):
        """Initialize OpenAI TTS module
        
        Args:
            voice_name (str): Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            model (str): TTS model to use (tts-1 or tts-1-hd)
        """
        self.voice_name = voice_name
        self.model = model
        self.api_key = ApiKeyManager.get_api_key("OPENAI")
        if not self.api_key:
            raise Exception("OpenAI API key not found. Please add it to your .env file")
        
        self.client = OpenAI(api_key=self.api_key)
        super().__init__()
    
    def generate_voice(self, text, outputfile):
        """Generate speech from text using OpenAI's TTS API
        
        Args:
            text (str): Text to convert to speech
            outputfile (str): Path to save the audio file
            
        Returns:
            str: Path to the generated audio file
        """
        try:
            # Generate speech using OpenAI API
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice_name,
                input=text
            )
            
            # Save the audio file
            response.stream_to_file(outputfile)
            
            if not os.path.exists(outputfile):
                raise Exception("Failed to generate audio file")
                
            return outputfile
            
        except Exception as e:
            print(f"Error generating audio using OpenAI TTS: {e}")
            raise Exception("Failed to generate audio using OpenAI TTS", e)
    
    def update_usage(self):
        """No usage tracking needed as OpenAI bills per character"""
        return None
    
    def get_remaining_characters(self):
        """No character limit, billed per use"""
        return float('inf')

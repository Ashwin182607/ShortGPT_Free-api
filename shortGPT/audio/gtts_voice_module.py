from gtts import gTTS
import os
from shortGPT.audio.voice_module import VoiceModule
from shortGPT.config.languages import Language

class GTTSVoiceModule(VoiceModule):
    """Google Text-to-Speech voice module - completely free with no API key required"""
    
    def __init__(self, language="en"):
        self.language = language
        super().__init__()
        
    def update_usage(self):
        return None
        
    def get_remaining_characters(self):
        return 999999999999  # No limit
        
    def generate_voice(self, text, outputfile):
        try:
            # Convert text to speech
            tts = gTTS(text=text, lang=self.language, slow=False)
            
            # Save the audio file
            tts.save(outputfile)
            
            if not os.path.exists(outputfile):
                raise Exception("Failed to generate audio file")
                
            return outputfile
            
        except Exception as e:
            print(f"Error generating audio using Google TTS: {e}")
            raise Exception("Failed to generate audio using Google TTS", e)

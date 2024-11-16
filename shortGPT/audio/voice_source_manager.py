from typing import Optional
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.audio.gtts_voice_module import GTTSVoiceModule
from shortGPT.audio.coqui_voice_module import CoquiVoiceModule
from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.audio.openai_voice_module import OpenAIVoiceModule
from shortGPT.config.api_db import ApiKeyManager
from torch.cuda import is_available

class VoiceSourceManager:
    """Manages multiple voice sources with fallback options"""
    
    @staticmethod
    def get_voice_module(voice_engine: str = "edge-tts", voice_name: str = "en-US-JennyNeural", language: str = "en") -> Optional[object]:
        """Get the best available voice module based on preferences and availability
        
        Args:
            voice_engine: Preferred voice engine ("openai", "edge-tts", "gtts", "coqui", "eleven-labs")
            voice_name: Voice name/character to use
            language: Language code (e.g., "en" for English)
            
        Returns:
            VoiceModule object or None if no suitable module found
        """
        # Try user's preferred engine first
        if voice_engine == "openai":
            api_key = ApiKeyManager.get_api_key("OPENAI")
            if api_key:
                try:
                    return OpenAIVoiceModule(voice_name)
                except Exception as e:
                    print(f"Warning: OpenAI TTS error: {e}. Falling back to free options.")
        
        elif voice_engine == "edge-tts":
            return EdgeTTSVoiceModule(voice_name)
            
        elif voice_engine == "gtts":
            return GTTSVoiceModule(language)
            
        elif voice_engine == "coqui":
            # Check if GPU is available for CoquiTTS
            if is_available():
                return CoquiVoiceModule(voice_name, language)
            print("Warning: CoquiTTS requires GPU. Falling back to other options.")
            
        elif voice_engine == "eleven-labs":
            # Check if API key is available
            api_key = ApiKeyManager.get_api_key("ELEVEN LABS")
            if api_key:
                try:
                    return ElevenLabsVoiceModule(api_key, voice_name)
                except Exception as e:
                    print(f"Warning: ElevenLabs error: {e}. Falling back to free options.")
            
        # Fallback chain: OpenAI -> Edge TTS -> gTTS -> CoquiTTS (if GPU) -> ElevenLabs (if key)
        api_key = ApiKeyManager.get_api_key("OPENAI")
        if api_key:
            try:
                return OpenAIVoiceModule("nova")  # Default to nova voice
            except:
                pass
                
        try:
            return EdgeTTSVoiceModule(voice_name)
        except:
            try:
                return GTTSVoiceModule(language)
            except:
                if is_available():
                    try:
                        return CoquiVoiceModule(voice_name, language)
                    except:
                        pass
                        
                api_key = ApiKeyManager.get_api_key("ELEVEN LABS")
                if api_key:
                    try:
                        return ElevenLabsVoiceModule(api_key, voice_name)
                    except:
                        pass
                        
        return None  # No voice module available

# ShortGPT Free API Version 🚀

This is an enhanced version of [RayVentura's ShortGPT](https://github.com/RayVentura/ShortGPT), optimized for better voice generation and batch processing capabilities.

## 🌟 What's New

### 1. Enhanced Voice Generation System
- **OpenAI TTS Integration**
  - High-quality voice synthesis at lower cost
  - 6 unique voices: alloy, echo, fable, onyx, nova, shimmer
  - Support for both tts-1 and tts-1-hd models
  - Automatic fallback to free alternatives

### 2. Batch Processing Improvements
- **Efficient Multi-Video Generation**
  - Generate multiple videos from a single topic
  - Dynamic script and title generation
  - Improved content diversity

### 3. Simplified Architecture
- Removed YouTube upload dependencies
- Direct video download functionality
- More flexible voice engine selection
- Improved error handling and fallback mechanisms

## 🛠️ Features

### Voice Options
1. **OpenAI TTS (New!)**
   - Premium quality at lower cost
   - Multiple voice personalities
   - High-definition model option

2. **Free Alternatives**
   - Edge TTS
   - Google TTS
   - CoquiTTS (requires GPU)

3. **Premium Option**
   - ElevenLabs (requires API key)

### Content Generation
- GPT-powered script creation
- Multilingual support
- Dynamic content adaptation
- Automated video assembly

## 🚀 Getting Started

1. **Installation**
```bash
git clone https://github.com/Ashwin182607/ShortGPT_Free-api.git
cd ShortGPT_Free-api
pip install -r requirements.txt
```

2. **API Keys Setup**
```python
# Add your API keys in the configuration
OPENAI_API_KEY=your_key_here  # Optional for OpenAI TTS
ELEVEN_LABS_API_KEY=your_key_here  # Optional for ElevenLabs
```

3. **Run the Application**
```bash
python runShortGPT.py  # For local installation
# OR
python runShortGPTColab.py  # For Google Colab
```

## 💡 Usage Examples

### Basic Video Generation
```python
from shortGPT.engine.batch_short_engine import BatchShortEngine

engine = BatchShortEngine(
    topic="Interesting Science Facts",
    num_videos=5,
    voice_engine="openai",  # or "edge-tts" for free option
    voice_name="nova"  # OpenAI voice option
)
engine.generate_videos()
```

### Custom Voice Selection
```python
# Using OpenAI TTS
engine.set_voice_engine("openai", voice_name="echo")

# Using Free Alternative
engine.set_voice_engine("edge-tts", voice_name="en-US-JennyNeural")
```

## 🌐 Google Colab Support
- Run ShortGPT directly in Google Colab
- No local GPU required
- Easy setup and execution
- Check `ShortGPT_Colab.ipynb` for instructions

## 📊 Performance Comparison

| Voice Engine | Quality | Cost | Speed |
|--------------|---------|------|--------|
| OpenAI TTS   | High    | Low  | Fast   |
| Edge TTS     | Good    | Free | Fast   |
| ElevenLabs   | Best    | High | Medium |
| Google TTS   | Good    | Free | Fast   |

## 🤝 Contributing
Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
- Original ShortGPT by [RayVentura](https://github.com/RayVentura/ShortGPT)
- Enhanced with additional features and optimizations

## ⚠️ Disclaimer
This is an unofficial enhanced version of ShortGPT. While we've added new features and improvements, all credit for the original implementation goes to RayVentura.

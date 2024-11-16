# 🚀🎬 ShortGPT 
## AI video automation framework
<p align="center">
  <a href="https://discord.gg/uERx39ru3R">
    <img src="https://dcbadge.vercel.app/api/server/uERx39ru3R?compact=true&style=flat">
  </a>
  <a href="https://star-history.com/#rayventura/shortgpt)">
    <img src="https://img.shields.io/github/stars/rayventura/shortgpt?style=social">
  </a>
  <a href="https://pypi.org/project/shortgpt/">
    <img src="https://static.pepy.tech/personalized-badge/shortgpt?period=month&units=international_system&left_color=blue&right_color=green&left_text=Downloads/month">
  </a>
  <a href="https://docs.shortgpt.ai/">
    <img src="https://img.shields.io/badge/docs-visit-blue">
  </a>  
</p>

<div align="center" style="border-radius: 20px;" width="18%">
    <img src="https://github.com/RayVentura/ShortGPT/assets/121462835/083c8dc3-bac5-42c1-a08d-3ff9686d18c5" alt="ShortGPT-logo" style="border-radius: 20px;" width="18%"/>
</div>
<div align="center">
  <a href="https://discord.gg/uERx39ru3R">
    <img src="https://img.shields.io/discord/1126042224979886160?color=7289da&logo=discord&logoColor=blue&labelColor=white&color=cyan" alt="Join our Discord" height="34">
  </a>
</div>

<div align="center">
⚡ Automating video and short content creation with AI ⚡
</div>
</br>

Follow the installation steps below for running the web app locally (running the google Colab is highly recommanded). 
Please read "installation-notes.md" for more details.

## 🚀 Quick Start with Google Colab

The easiest way to use ShortGPT is through Google Colab. Follow these steps:

1. Open our [ShortGPT Colab Notebook](https://colab.research.google.com/github/RayVentura/ShortGPT/blob/main/ShortGPT_Colab.ipynb)
2. Click "Runtime" -> "Run all"
3. Wait for the installation to complete
4. Access the web interface through the provided link

## 🌟 Show Your Support
We hope you find ShortGPT helpful! If you do, let us know by giving us a star ⭐ on the repo. It's easy, just click on the 'Star' button at the top right of the page. Your support means a lot to us and keeps us motivated to improve and expand ShortGPT. Thank you and happy content creating! 🎉 

[![GitHub star chart](https://img.shields.io/github/stars/rayventura/shortgpt?style=social)](https://github.com/RayVentura/ShortGPT/stargazers)

## 🛠️ How it works
![alt text](https://github.com/RayVentura/ShortGPT/assets/121462835/fcee74d4-f856-4481-949f-244558bf3bfa)

## 📝 Introduction to ShortGPT 
ShortGPT is a powerful framework for automating content creation. It simplifies video creation, footage sourcing, voiceover synthesis, and editing tasks. Of the most popular use-cases of ShortGPT is youtube automation and Tiktok creativity program automation.

- 🎞️ **Automated editing framework**: Streamlines the video creation process with an LLM oriented video editing language.

- 📃 **Scripts and Prompts**: Provides ready-to-use scripts and prompts for various LLM automated editing processes.

- 🗣️ **Voiceover / Content Creation**: Supports multiple languages including English 🇺🇸, Spanish 🇪🇸, Arabic 🇦🇪, French 🇫🇷, Polish 🇵🇱, German 🇩🇪, Italian 🇮🇹, Portuguese 🇵🇹, Russian 🇷🇺, Mandarin Chinese 🇨🇳, Japanese 🇯🇵, Hindi 🇮🇳,Korean 🇰🇷, and way over 30 more languages (with EdgeTTS)

- 🔗 **Caption Generation**: Automates the generation of video captions.

- 🌐🎥 **Asset Sourcing**: Sources images and video footage from the internet, connecting with the web and Pexels API as necessary.

- 🧠 **Memory and persistency**: Ensures long-term persistency of automated editing variables with TinyDB.

## 🛠️ Local Installation

If you prefer running locally:

```bash
git clone https://github.com/RayVentura/ShortGPT.git
cd ShortGPT
pip install -r requirements.txt
python run.py
```

## 🔑 API Keys Setup

You'll need:
1. OpenAI API key for content generation
2. (Optional) ElevenLabs API key for premium voices

Add these to your `.env` file:
```
OPENAI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
```

## 🎮 Usage

1. Enter your topic (e.g., "interesting science facts")
2. Choose number of videos to generate (1-10)
3. Select TTS engine and language
4. Click "Generate Videos"
5. Download your generated videos!

## ⚡ Tips for Best Results

- Use specific topics for better content generation
- Keep video count under 5 for faster generation
- Test different TTS engines for best voice quality
- Ensure stable internet connection for API calls

## 🚀 Framework overview

- 🎬 The `ContentShortEngine` is designed for creating shorts, handling tasks from script generation to final rendering, including adding metadata.

- 🎥 The `ContentVideoEngine` is ideal for longer videos, taking care of tasks like generating audio, automatically sourcing background video footage, timing captions, and preparing background assets.

- 🗣️ The `ContentTranslationEngine` is designed to dub and translate entire videos, from mainstream languages to more specific target languages. It takes a video file, or link, transcribe it's audio, translates the content, voices it in a target language, adds captions , and gives back a new video, in a totally different language.

- 🎞️ The automated `EditingEngine`, using Editing Markup Language and JSON, breaks down the editing process into manageable and customizable blocks, comprehensible to Large Language Models.

💡 ShortGPT offers customization options to suit your needs, from language selection to watermark addition.

🔧 As a framework, ShortGPT is adaptable and flexible, offering the potential for efficient, creative content creation.

More documentation incomming, please be patient.


## Technologies Used

ShortGPT utilizes the following technologies to power its functionality:

- **Moviepy**: Moviepy is used for video editing, allowing ShortGPT to make video editing and rendering

- **Openai**: Openai is used for automating the entire process, including generating scripts and prompts for LLM automated editing processes.

- **ElevenLabs**: ElevenLabs is used for voice synthesis, supporting multiple languages for voiceover creation.

- **EdgeTTS**: Microsoft's FREE EdgeTTS is used for voice synthesis, supporting way many more language than ElevenLabs currently.

- **Pexels**: Pexels is used for sourcing background footage, allowing ShortGPT to connect with the web and access a wide range of images and videos.

- **Bing Image**: Bing Image is used for sourcing images, providing a comprehensive database for ShortGPT to retrieve relevant visuals.

These technologies work together to provide a seamless and efficient experience in automating video and short content creation with AI.

## 💁 Contributing

As an open-source project in a rapidly developing field, we are extremely open to contributions, whether it would be in the form of a new feature, improved infrastructure, or better documentation.
<p align="center">
  <a href="https://star-history.com/#RayVentura/ShortGPT&Date">
    <img src="https://api.star-history.com/svg?repos=RayVentura/ShortGPT&type=Date" alt="Star History Chart">
  </a>
</p>

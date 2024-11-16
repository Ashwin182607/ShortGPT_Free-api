import os
import traceback
import gradio as gr
import shutil
from pathlib import Path

from gui.asset_components import AssetComponentsUtils
from gui.ui_abstract_component import AbstractComponentUI
from gui.ui_components_html import GradioComponentsHTML
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.audio.coqui_voice_module import CoquiVoiceModule
from shortGPT.audio.gtts_voice_module import GTTSVoiceModule
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.languages import (EDGE_TTS_VOICENAME_MAPPING,
                                   ELEVEN_SUPPORTED_LANGUAGES,
                                   COQUI_SUPPORTED_LANGUAGES,
                                   LANGUAGE_ACRONYM_MAPPING,
                                   Language)
from shortGPT.engine.batch_short_engine import BatchShortEngine

class BatchAutomationUI(AbstractComponentUI):
    def __init__(self, shortGptUI: gr.Blocks):
        self.shortGptUI = shortGptUI
        self.progress_counter = 0
        self.batch_engine = None
        self.output_dir = "output_videos"
        
    def create_ui(self):
        with gr.Row(visible=True) as batch_automation:
            with gr.Column():
                # Basic settings
                topic = gr.Textbox(label="Topic for videos (e.g., 'reddit relationships', 'interesting facts')", 
                                 placeholder="Enter topic here...")
                num_videos = gr.Slider(minimum=1, maximum=10, value=5, step=1, 
                                     label="Number of videos to generate")
                
                # TTS Engine Selection
                tts_engine = gr.Radio(
                    [AssetComponentsUtils.ELEVEN_TTS, AssetComponentsUtils.EDGE_TTS, 
                     AssetComponentsUtils.COQUI_TTS, "Google TTS"],
                    label="Text to speech engine",
                    value=AssetComponentsUtils.EDGE_TTS
                )
                
                # Language selection containers
                with gr.Column(visible=True) as eleven_tts:
                    language_eleven = gr.Radio(
                        [lang.value for lang in ELEVEN_SUPPORTED_LANGUAGES],
                        label="Language",
                        value="English"
                    )
                    voice_eleven = AssetComponentsUtils.voiceChoice(
                        provider=AssetComponentsUtils.ELEVEN_TTS
                    )
                    
                with gr.Column(visible=False) as edge_tts:
                    language_edge = gr.Dropdown(
                        [lang.value.upper() for lang in Language],
                        label="Language",
                        value="ENGLISH"
                    )
                    
                with gr.Column(visible=False) as coqui_tts:
                    language_coqui = gr.Radio(
                        [lang.value for lang in COQUI_SUPPORTED_LANGUAGES],
                        label="Language",
                        value="English"
                    )
                    voice_coqui = AssetComponentsUtils.voiceChoice(
                        provider=AssetComponentsUtils.COQUI_TTS
                    )
                    
                with gr.Column(visible=False) as gtts:
                    language_gtts = gr.Dropdown(
                        [lang.value.upper() for lang in Language],
                        label="Language",
                        value="ENGLISH"
                    )
                
                # Background assets
                AssetComponentsUtils.background_video_checkbox()
                AssetComponentsUtils.background_music_checkbox()
                
                # Generation button
                generate_btn = gr.Button("Generate Videos", variant="primary")
                
                # Output area
                output_status = gr.Markdown("No videos generated yet.")
                download_btn = gr.Button("Download Generated Videos", visible=False)
                
                def tts_engine_change(x):
                    return (
                        gr.update(visible=x == AssetComponentsUtils.ELEVEN_TTS),
                        gr.update(visible=x == AssetComponentsUtils.EDGE_TTS),
                        gr.update(visible=x == AssetComponentsUtils.COQUI_TTS),
                        gr.update(visible=x == "Google TTS")
                    )
                
                def create_voice_module(tts_engine, language_eleven, language_edge, 
                                     language_coqui, language_gtts, voice_eleven, voice_coqui):
                    if tts_engine == AssetComponentsUtils.ELEVEN_TTS:
                        return ElevenLabsVoiceModule(voice_eleven)
                    elif tts_engine == AssetComponentsUtils.EDGE_TTS:
                        return EdgeTTSVoiceModule(EDGE_TTS_VOICENAME_MAPPING[Language(language_edge.lower())])
                    elif tts_engine == AssetComponentsUtils.COQUI_TTS:
                        return CoquiVoiceModule(voice_coqui)
                    else:
                        return GTTSVoiceModule(LANGUAGE_ACRONYM_MAPPING[Language(language_gtts.lower())])
                
                def generate_videos(topic, num_videos, tts_engine, language_eleven,
                                 language_edge, language_coqui, language_gtts,
                                 voice_eleven, voice_coqui, background_video_list,
                                 background_music_list, progress=gr.Progress()):
                    try:
                        # Validate inputs
                        if not topic.strip():
                            raise gr.Error("Please enter a topic for the videos")
                            
                        if not background_video_list or not background_music_list:
                            raise gr.Error("Please select background video and music")
                            
                        # Create voice module
                        voice_module = create_voice_module(tts_engine, language_eleven,
                                                        language_edge, language_coqui,
                                                        language_gtts, voice_eleven,
                                                        voice_coqui)
                        
                        # Create output directory
                        output_dir = os.path.join(os.getcwd(), "output_videos")
                        os.makedirs(output_dir, exist_ok=True)
                        
                        # Create and run batch engine
                        self.batch_engine = BatchShortEngine(
                            voice_module=voice_module,
                            background_video_name=background_video_list[0],
                            background_music_name=background_music_list[0],
                            num_videos=int(num_videos)
                        )
                        
                        self.batch_engine.generate_batch(topic, output_dir)
                        
                        # Update UI
                        num_generated = len(self.batch_engine.generated_videos)
                        status = f"✅ Generated {num_generated} videos successfully!"
                        return status, gr.update(visible=True)
                        
                    except Exception as e:
                        return f"❌ Error: {str(e)}", gr.update(visible=False)
                
                def create_zip_and_download():
                    if not self.batch_engine or not self.batch_engine.generated_videos:
                        return None
                        
                    # Create zip file of generated videos
                    zip_path = os.path.join(os.getcwd(), "generated_videos.zip")
                    output_dir = os.path.join(os.getcwd(), "output_videos")
                    
                    if os.path.exists(zip_path):
                        os.remove(zip_path)
                        
                    shutil.make_archive("generated_videos", 'zip', output_dir)
                    return zip_path
                
                # Wire up the UI components
                tts_engine.change(
                    tts_engine_change,
                    tts_engine,
                    [eleven_tts, edge_tts, coqui_tts, gtts]
                )
                
                generate_btn.click(
                    generate_videos,
                    inputs=[
                        topic, num_videos, tts_engine,
                        language_eleven, language_edge, language_coqui, language_gtts,
                        voice_eleven, voice_coqui,
                        AssetComponentsUtils.background_video_list,
                        AssetComponentsUtils.background_music_list
                    ],
                    outputs=[output_status, download_btn]
                )
                
                download_btn.click(
                    create_zip_and_download,
                    inputs=[],
                    outputs=[gr.File(label="Download Videos")]
                )
                
        return batch_automation

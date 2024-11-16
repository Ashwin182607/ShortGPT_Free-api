import gradio as gr
from shortGPT.config.reddit_types import RedditStoryType
from shortGPT.engine.reddit_youtube_engine import RedditToYoutubeEngine
from shortGPT.api_utils.youtube_uploader import YouTubeUploader
from gui.ui_abstract_base import AbstractBaseUI

class RedditAutomationUI(AbstractBaseUI):
    def __init__(self, shortGptUI):
        self.shortGptUI = shortGptUI
        self.youtube_uploader = None
        try:
            self.youtube_uploader = YouTubeUploader()
        except Exception as e:
            print(f"YouTube uploader initialization failed: {e}")

    def create_ui(self):
        with gr.Tab("Reddit Automation"):
            with gr.Row():
                with gr.Column():
                    story_type = gr.Dropdown(
                        choices=[story_type.value for story_type in RedditStoryType],
                        value=RedditStoryType.AITA.value,
                        label="Story Type"
                    )
                    num_videos = gr.Slider(minimum=1, maximum=10, value=1, step=1, label="Number of Videos")
                    vertical_format = gr.Checkbox(value=True, label="Vertical Format (Shorts)")
                    
                    with gr.Row():
                        with gr.Column():
                            tts_choice = gr.Radio(
                                choices=["ElevenLabs", "EdgeTTS", "CoquiTTS"],
                                value="EdgeTTS",
                                label="Text-to-Speech Engine"
                            )
                            voice_choice = gr.Dropdown(
                                choices=["en-US-AriaNeural", "en-US-GuyNeural", "en-GB-SoniaNeural"],
                                value="en-US-AriaNeural",
                                label="Voice"
                            )
                            language = gr.Dropdown(
                                choices=["English", "Spanish", "French", "German"],
                                value="English",
                                label="Language"
                            )

                    with gr.Row():
                        with gr.Column():
                            add_watermark = gr.Checkbox(value=True, label="Add Watermark")
                            custom_background = gr.Checkbox(value=True, label="Use Custom Background")
                            background_music = gr.Checkbox(value=True, label="Add Background Music")

                    # YouTube Upload Settings
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### 📺 YouTube Upload Settings")
                            auto_upload = gr.Checkbox(value=False, label="Auto Upload to YouTube")
                            youtube_tags = gr.Textbox(
                                label="YouTube Tags (comma-separated)",
                                placeholder="reddit, story, viral",
                                visible=True
                            )
                            custom_description = gr.Textbox(
                                label="Custom Description (optional)",
                                placeholder="Add your custom description here...",
                                lines=3,
                                visible=True
                            )

                    generate_btn = gr.Button("Generate & Upload Reddit Videos", variant="primary")

                with gr.Column():
                    output_text = gr.Textbox(label="Generation Progress", lines=10)
                    preview_video = gr.Video(label="Preview")
                    upload_status = gr.Textbox(label="Upload Status", visible=True)

            def generate_and_upload(story_type, num_videos, vertical, tts, voice, lang, 
                                 watermark, bg, music, auto_upload, tags, custom_desc):
                try:
                    engine = RedditToYoutubeEngine(
                        story_type=story_type,
                        num_videos=num_videos,
                        vertical_format=vertical,
                        tts_engine=tts,
                        voice=voice,
                        language=lang,
                        add_watermark=watermark,
                        custom_background=bg,
                        background_music=music
                    )
                    
                    videos = engine.generate_videos()
                    status_text = ""
                    
                    for i, video in enumerate(videos):
                        status_text += f"Generated video {i+1}: {video['path']}\n"
                        
                        if auto_upload and self.youtube_uploader:
                            try:
                                # Prepare video metadata
                                video_tags = [tag.strip() for tag in tags.split(',')] if tags else []
                                description = custom_desc if custom_desc else video['metadata']['description']
                                
                                # Upload to YouTube
                                response = self.youtube_uploader.upload_video(
                                    video_path=video['path'],
                                    title=video['metadata']['title'],
                                    description=description,
                                    tags=video_tags,
                                    is_short=vertical
                                )
                                
                                video_id = response['id']
                                status_text += f"✅ Uploaded to YouTube: https://youtu.be/{video_id}\n"
                            except Exception as e:
                                status_text += f"❌ Upload failed: {str(e)}\n"
                        
                    return videos[0]['path'], status_text
                except Exception as e:
                    return None, f"Error: {str(e)}"

            generate_btn.click(
                fn=generate_and_upload,
                inputs=[
                    story_type, num_videos, vertical_format, tts_choice, 
                    voice_choice, language, add_watermark, custom_background, 
                    background_music, auto_upload, youtube_tags, custom_description
                ],
                outputs=[preview_video, upload_status]
            )

        return "Reddit Automation"

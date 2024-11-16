from gui.gui_gradio import ShortGptUI

# Initialize and launch the UI with Colab-specific settings
ui = ShortGptUI()
ui.launch(server_name="0.0.0.0", server_port=31415, share=True)

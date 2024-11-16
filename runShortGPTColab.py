from gui.gui_gradio import ShortGptUI

# Initialize and launch the UI with Colab-specific settings
try:
    import gradio
    print(f"Gradio version: {gradio.__version__}")
except Exception as e:
    print(f"Error importing gradio: {e}")

ui = ShortGptUI(colab=True)
ui.launch(host="0.0.0.0", port=31415)

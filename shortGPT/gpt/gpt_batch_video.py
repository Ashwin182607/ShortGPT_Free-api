from shortGPT.gpt import gpt_utils
import json

def generate_batch_script(topic: str, language: str) -> dict:
    """Generate a script with title for batch video creation
    
    Args:
        topic (str): The topic to generate content about
        language (str): Target language for the script
        
    Returns:
        dict: Dictionary containing 'title' and 'script' keys
    """
    out = {'title': '', 'script': ''}
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/batch_video_script.yaml')
    
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": chat.format(description=topic, language=language)}
    ]
    
    while not (out.get('title') and out.get('script')):
        try:
            response = gpt_utils.gpt_completion(messages=messages, temperature=1)
            result = response.choices[0].message.content
            out = json.loads(result)
        except Exception as e:
            print(f"Error generating batch script: {e}")
            continue
            
    return out

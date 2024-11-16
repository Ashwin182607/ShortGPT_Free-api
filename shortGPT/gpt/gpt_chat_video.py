from shortGPT.gpt import gpt_utils
import json

def generateScript(script_description, language):
    out = {'script': ''}
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/chat_video_script.yaml')
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": chat.format(description=script_description, language=language)}
    ]
    while not ('script' in out and out['script']):
        try:
            response = gpt_utils.gpt_completion(messages=messages, temperature=1)
            result = response.choices[0].message.content
            out = json.loads(result)
        except Exception as e:
            print(e, "Difficulty parsing the output in gpt_chat_video.generateScript")
    return out['script']

def correctScript(script, correction):
    out = {'script': ''}
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/chat_video_edit_script.yaml')
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": chat.format(original_script=script, corrections=correction)}
    ]
    while not ('script' in out and out['script']):
        try:
            response = gpt_utils.gpt_completion(messages=messages, temperature=1)
            result = response.choices[0].message.content
            out = json.loads(result)
        except Exception as e:
            print("Difficulty parsing the output in gpt_chat_video.generateScript")
    return out['script']
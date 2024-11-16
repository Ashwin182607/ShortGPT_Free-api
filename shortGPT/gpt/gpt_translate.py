from shortGPT.gpt import gpt_utils

def translateContent(content, language):
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/translate_content.yaml')
    if language == "arabic":
        language = "arabic, and make the translated text two third of the length of the original."
    
    messages = [
        {"role": "system", "content": system.format(language=language)},
        {"role": "user", "content": chat.format(content=content)}
    ]
    response = gpt_utils.gpt_completion(messages=messages, temperature=1)
    return response.choices[0].message.content
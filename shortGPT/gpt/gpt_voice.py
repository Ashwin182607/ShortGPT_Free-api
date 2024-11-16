from shortGPT.gpt import gpt_utils

def getGenderFromText(text):
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/voice_identify_gender.yaml')
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": chat.format(story=text)}
    ]
    response = gpt_utils.gpt_completion(messages=messages)
    result = response.choices[0].message.content.replace("\n", "").lower()
    if 'female' in result:
        return 'female'
    return 'male'
from shortGPT.gpt import gpt_utils
import json

def generate_title_description_dict(content):
    out = {"title": "", "description":""}
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/yt_title_description.yaml')
    chat = chat.format(content=content)
    while out["title"] == "" or out["description"] == "":
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": chat}
        ]
        response = gpt_utils.gpt_completion(messages=messages, temperature=1)
        try:
            result = response.choices[0].message.content
            json_response = json.loads(result)
            if "title" in json_response:
                out["title"] = json_response["title"]
            if "description" in json_response:
                out["description"] = json_response["description"]
        except Exception as e:
            pass
        
    return out['title'], out['description']

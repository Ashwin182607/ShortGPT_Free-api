from shortGPT.gpt import gpt_utils
import json

def generateFacts(facts_type):
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/facts_generator.yaml')
    chat = chat.format(facts_type=facts_type)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": chat}
    ]
    response = gpt_utils.gpt_completion(messages=messages, temperature=1.3)
    return response.choices[0].message.content

def generateFactSubjects(n):
    out = []
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/facts_subjects_generation.yaml')
    chat = chat.format(n=n)
    count = 0
    while len(out) != n:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": chat}
        ]
        response = gpt_utils.gpt_completion(messages=messages, temperature=1.69)
        result = response.choices[0].message.content
        count += 1
        try:
            out = json.loads(result.replace("'", '"'))
        except Exception as e:
            print(f"INFO - Failed generating {n} fact subjects after {count} trials", e)
            pass
        
    return out
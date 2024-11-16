import json
import os
import re
from time import sleep, time

import openai
import tiktoken
import yaml
from shortGPT.gpt.huggingface_utils import HuggingFaceAPI
from shortGPT.config.api_db import ApiKeyManager


def num_tokens_from_messages(texts, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        if isinstance(texts, str):
            texts = [texts]
        score = 0
        for text in texts:
            score += 4 + len(encoding.encode(text))
        return score
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
        See https://github.com/openai/openai-python/blob/main/chatml.md for information""")


def extract_biggest_json(string):
    json_regex = r"\{(?:[^{}]|(?R))*\}"
    json_objects = re.findall(json_regex, string)
    if json_objects:
        return max(json_objects, key=len)
    return None


def get_first_number(string):
    pattern = r'\b(0|[1-9]|10)\b'
    match = re.search(pattern, string)
    if match:
        return int(match.group())
    else:
        return None


def load_yaml_file(file_path: str) -> dict:
    """Reads and returns the contents of a YAML file as dictionary"""
    return yaml.safe_load(open_file(file_path))


def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data

from pathlib import Path

def load_local_yaml_prompt(file_path):
    _here = Path(__file__).parent
    _absolute_path = (_here / '..' / file_path).resolve()
    json_template = load_yaml_file(str(_absolute_path))
    return json_template['chat_prompt'], json_template['system_prompt']


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def gpt_completion(messages: list, model="gpt-3.5-turbo", temperature=0.7, max_tokens=None, stop=None):
    """
    Function to get GPT completion. Will try Hugging Face first, then fall back to OpenAI if not available.
    """
    try:
        # Try Hugging Face first
        if ApiKeyManager.get_api_key("HUGGINGFACE"):
            try:
                return HuggingFaceAPI.create_chat_completion(
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stop=stop
                )
            except Exception as e:
                print('Error with Hugging Face API:', e)
                print('Falling back to OpenAI...')
        
        # Fall back to OpenAI
        openai.api_key = ApiKeyManager.get_api_key("OPENAI")
        if not openai.api_key:
            raise ValueError("Neither HUGGINGFACE nor OPENAI API keys are available. Please set at least one in the config.")
            
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop
        )
        return response
    except Exception as oops:
        print('Error communicating with APIs:', oops)
        raise ValueError("Failed to get response from both Hugging Face and OpenAI APIs")
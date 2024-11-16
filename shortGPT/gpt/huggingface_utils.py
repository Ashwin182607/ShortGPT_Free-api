import requests
from shortGPT.config.api_db import ApiKeyManager
from typing import List, Optional, Union, Dict

class HuggingFaceAPI:
    API_URL = "https://api-inference.huggingface.co/models/"
    DEFAULT_MODEL = "tiiuae/falcon-7b-instruct"  # Free alternative to GPT
    
    @classmethod
    def get_api_key(cls) -> str:
        """Get the Hugging Face API key."""
        return ApiKeyManager.get_api_key("HUGGINGFACE")
    
    @classmethod
    def create_chat_completion(
        cls,
        messages: List[Dict[str, str]],
        model: str = DEFAULT_MODEL,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
    ) -> dict:
        """
        Create a chat completion using Hugging Face's API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (defaults to falcon-7b-instruct)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            stop: Stop sequence(s) to use
            
        Returns:
            Dictionary containing the response
        """
        api_key = cls.get_api_key()
        if not api_key:
            raise ValueError("HUGGINGFACE API key not found. Please set it in the config.")

        # Convert OpenAI-style messages to Hugging Face format
        prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt += f"System: {content}\n"
            elif role == "user":
                prompt += f"Human: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
        prompt += "Assistant: "

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": temperature,
                "max_new_tokens": max_tokens if max_tokens else 100,
                "stop": stop if stop else []
            }
        }

        response = requests.post(
            f"{cls.API_URL}{model}",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"Error from Hugging Face API: {response.text}")
            
        result = response.json()[0]["generated_text"]
        # Extract only the assistant's response
        result = result.split("Assistant: ")[-1].strip()
        
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": result
                }
            }]
        }

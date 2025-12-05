import requests
from .ollama_errors import format_ollama_error
import json

OLLAMA_URL= "http://localhost:11434/api/chat"
DEFAULT_MODEL = "gemma3:1b"



def call_llm(prompt: str=None, messages: list=None) -> str:
    # if messages provided directly, use.
    if messages is not None:
        final_messages = messages

    # otherwise convert prompt to message
    elif prompt is not None:
        final_messages = [{
            "role": "user",
            "content": prompt
        }]
    else:
        raise ValueError("Either prompt or messages must be provided to call_llm.")
    
    payload = {"model": DEFAULT_MODEL, "messages": final_messages, "stream": False}           # what Ollama's /api/chat expects

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)                  # where code calls Ollama API
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"].strip()
    except Exception as e:
        return format_ollama_error(e)

def call_llm_stream(prompt: str=None, messages: list=None):
    # if messages provided directly, use.
    if messages is not None:
        final_messages = messages

    # otherwise convert prompt to message
    elif prompt is not None:
        final_messages = [{
            "role": "user",
            "content": prompt
        }]
    else:
        raise ValueError("Either prompt or messages must be provided to call_llm.")
    
    payload = {"model": DEFAULT_MODEL, "messages": final_messages, "stream": True}
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60, stream=True) 
        
        # Check for errors before processing
        if response.status_code != 200:
            error_text = response.text
            yield f"Error: {error_text}"
            return
        
        # iterate through response lines
        for line in response.iter_lines():
            if line:
                chunk_data = json.loads(line)
                #extract content from chunk
                if "message" in chunk_data and "content" in chunk_data["message"]:
                    yield chunk_data["message"]["content"]

    except Exception as e:
        yield format_ollama_error(e)
                    
    


# def call_llm_with_tools(prompt: str, tools: list) -> str:
#     try:
#         response = genai.generate_text(
#             model = model_with_tools,
#             contents = [prompt],
#             tools = ollama_tools
#         )

#         return response.text
#     except Exception as e:
#         print(f"ollama call_llm_with_tools error: {e}")
#         friendly = format_ollama_error(e)
#         return {
#             "type": "error",
#             "content": friendly,
#             # "debug": str(e),  # optional: for logs / dev tools, not for UI
#     }

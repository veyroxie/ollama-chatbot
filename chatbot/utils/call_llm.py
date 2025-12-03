import requests
from .ollama_errors import format_ollama_error

OLLAMA_URL= "http://localhost:11434/api/chat"
DEFAULT_MODEL = "gemma3:1b"



def call_llm(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]                                    # chat format for OpenAI / Gemini / Ollama
    payload = {"model": DEFAULT_MODEL, "messages": messages, "stream": False}           # what Ollama's /api/chat expects

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)                  # where code calls Ollama API
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"].strip()
    except Exception as e:
        return format_ollama_error(e)


    


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

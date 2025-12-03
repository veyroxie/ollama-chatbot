from chatbot.utils.call_llm import call_llm
from chatbot.nodes.simple_chat_node import SimpleChatNode

# print("Sending prompt to Ollama...")
# print(call_llm("Hello from Ollama!"))


node = SimpleChatNode()
print("Testing SimpleChatNode...")
response = node.process("Explain what an IoT sensor is in one sentence.")
print("Reply:" + response)
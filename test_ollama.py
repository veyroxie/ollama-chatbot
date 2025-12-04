from chatbot.utils.call_llm import call_llm
from chatbot.nodes.simple_chat_node import SimpleChatNode

# print("Sending prompt to Ollama...")
# print(call_llm("Hello from Ollama!"))


# node = SimpleChatNode()
# print("Testing SimpleChatNode...")
# response = node.process("Explain what an IoT sensor is in one sentence.")
# print("Reply:" + response)

from chatbot.nodes.planner_node import PlannerNode

node = PlannerNode()

tests = [
    "hi how are you",
    "what time is it now?",
    "give me a random number",
    "what is the weather like in Tokyo?"
]

for t in tests:
    plan = node.process(t)
    print("User:", t)
    print("Plan:", plan)
    print("-" * 40)

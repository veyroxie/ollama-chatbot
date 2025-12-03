from chatbot.nodes.simple_chat_node import SimpleChatNode


def main():
    node = SimpleChatNode()                                 # create one node instance to handle convo


    print("Ollama Chatbot (type 'quit' to exit)")
    while True:
        user_message = input("You: ").strip()
        if user_message.lower() in {"quit", "exit"}:
            print("Exiting. Goodbye!")
            break

        reply = node.process(user_message)                  # hands text to LLM pipeline through call_llm -> Ollama API
        print("Assistant:", reply)

    

if __name__ == "__main__":
    main()
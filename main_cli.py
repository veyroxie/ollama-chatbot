from chatbot.nodes.planner_node import PlannerNode
from chatbot.nodes.tool_runner_node import ToolRunnerNode
from chatbot.nodes.answer_node import AnswerNode


def main():
    planner = PlannerNode()                    
    runner = ToolRunnerNode()
    answerer = AnswerNode()       # create one node instance to handle convo

    conversation_history = []   # track convo history

    print("Ollama Chatbot (type 'quit' to exit)")
    while True:
        user_message = input("You: ").strip()

        conversation_history.append({
            "role": "user",
            "content": user_message
        })

        if user_message.lower() in {"quit", "exit"}:
            print("Exiting. Goodbye!")
            break

        # Planning phase
        plan = planner.process(user_message, conversation_history)
        print("[debug] Plan:", plan)

        tool_output = None

        # Tool execution phase
        if plan.get("action") == "use_tool":
            tool_output = runner.process(plan)
            print("[debug] Tool output:", tool_output)

        else:
            print("[debug] No tool used, proceeding to answer generation.")

        # Answer generation phase
        final_reply = answerer.process(user_message, tool_output, conversation_history)
        print("Bot:", final_reply)
        print("-" * 40)

        # Add bot response to conversation history
        conversation_history.append({
            "role": "assistant",
            "content": final_reply
        })
    

if __name__ == "__main__":
    main()
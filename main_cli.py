from chatbot.nodes.planner_node import PlannerNode
from chatbot.nodes.tool_runner_node import ToolRunnerNode
from chatbot.nodes.answer_node import AnswerNode
from chatbot.nodes.chain_executor_node import ChainExecutorNode


def main():
    planner = PlannerNode()                    
    runner = ToolRunnerNode()
    answerer = AnswerNode()   
    chain_executor = ChainExecutorNode()    # create one node instance to handle convo

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
        if plan.get("action") in ["use_tool", "use_tools"]:
            # Use ChainExecutorNode for both single and multi-tool execution
            execution_result = chain_executor.process(plan)
            print("[debug] Execution result:", execution_result)
            tool_output = execution_result
        elif plan.get("action") == "answer_direct":
            print("[debug] No tools used, proceeding to answer generation.")
        else:
            print(f"[debug] Unknown action: {plan.get('action')}")

        # Answer generation phase
        final_reply = answerer.process(user_message, tool_output, conversation_history)
        print("Bot:", end = "", flush = True)
        full_response = ""
        for chunk in final_reply:
            print(chunk, end="", flush=True)
            full_response += chunk
        print()  # for newline after streaming
        print("-" * 40)

        # Add bot response to conversation history
        conversation_history.append({
            "role": "assistant",
            "content": full_response
        })
    

if __name__ == "__main__":
    main()
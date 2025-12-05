import json
from .base_node import BaseNode
from chatbot.utils.call_llm import call_llm_stream


class AnswerNode(BaseNode):
    """
    Answer node (LLM call #2).

    Inputs:
    - user_message: original user question
    - tool_output: dict from ToolRunner, e.g. {"result": {...}} or {"error": "..."}

    Output:
    - final string answer for the user
    """

    def process(self, user_message: str, tool_output: dict | None = None, conversation_history: list = None) -> str:
        # 1. Prepare a safe representation of tool_output for the prompt
        if tool_output is None:
            tool_block = "No tools were used."
        else:
            # Pretty-print as JSON so LLM can read it clearly
            tool_block = json.dumps(tool_output, indent=2)

        # 2. Build system-style instructions
        system_instructions = (
            "You are a helpful assistant for a simple chatbot.\n"
            "You receive outputs from tools that execute to get information.\n"
            "\n"
            "CRITICAL INSTRUCTION:\n"
            "When you see tool results with ✓ (checkmark), those tools SUCCEEDED.\n"
            "When you see tool results with ✗ (X mark), those tools FAILED.\n"
            "\n"
            "YOUR JOB:\n"
            "1. Look at ALL the results in the summary\n"
            "2. Find the ones marked with ✓ - these have the ACTUAL DATA\n"
            "3. Use that data to answer the user's question\n"
            "4. Ignore the ✗ failures unless they prevent answering completely\n"
            "\n"
            "EXAMPLE:\n"
            "If summary shows:\n"
            "✓ Step 1 (get_time): {'time': '2025-12-05T15:15:31+08:00'}\n"
            "✗ Step 2 (failing_tool): ERROR\n"
            "\n"
                "You should answer: 'The current time is 3:15 PM, your other request failed'\n"
                "NOT: 'The tool failed to execute.'\n"
            "\n"
            "Do not mention 'tools', 'steps', or technical details.\n"
            "Be concise and friendly.\n"
        )

        # build messages w convo history
        messages =  []

        # add system instructions
        messages.append({
            "role": "system",
            "content": system_instructions
        })

        # add convo history if present
        if conversation_history:
            # add all previous messages except last user message
            for msg in conversation_history[:-1]:
                messages.append(msg)

        # add current user message with tool output
        user_content = f"User question: {user_message}\n\nTool output (if any):\n{tool_block}\n\nNow write the final answer for the user:"
        messages.append({
            "role": "user",
            "content": user_content
            })

        # 3. Call the LLM to compose the answer
        for chunk in call_llm_stream(messages=messages):
            yield chunk

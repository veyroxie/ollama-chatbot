import json
from .base_node import BaseNode
from chatbot.utils.call_llm import call_llm


class AnswerNode(BaseNode):
    """
    Answer node (LLM call #2).

    Inputs:
    - user_message: original user question
    - tool_output: dict from ToolRunner, e.g. {"result": {...}} or {"error": "..."}

    Output:
    - final string answer for the user
    """

    def process(self, user_message: str, tool_output: dict | None = None) -> str:
        # 1. Prepare a safe representation of tool_output for the prompt
        if tool_output is None:
            tool_block = "No tools were used."
        else:
            # Pretty-print as JSON so LLM can read it clearly
            tool_block = json.dumps(tool_output, indent=2)

        # 2. Build system-style instructions
        system_instructions = (
            "You are a helpful assistant for a simple chatbot.\n"
            "You may receive outputs from tools (like current time, random numbers, or fake weather).\n"
            "If tool results are present, treat them as accurate and use them in your answer.\n"
            "If no tool results are present, just answer the user directly.\n"
            "Do not mention 'tools' or 'planner' or 'internal JSON' in your reply.\n"
            "Reply in a concise, friendly way.\n"
        )

        full_prompt = (
            f"{system_instructions}\n"
            f"User message:\n{user_message}\n\n"
            f"Tool output (if any, JSON):\n{tool_block}\n\n"
            "Now write the final answer for the user:"
        )

        # 3. Call the LLM to compose the answer
        answer = call_llm(full_prompt)
        return answer.strip()

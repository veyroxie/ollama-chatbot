from chatbot.tools.simple_tools import get_time, random_number, fake_weather, failing_tool
import json
from .base_node import BaseNode
from chatbot.utils.call_llm import call_llm

TOOL_MAP = {
    "get_time": get_time,
    "random_number": random_number,
    "fake_weather": fake_weather,
    "failing_tool": failing_tool
}

AVAILABLE_TOOLS = {
    "get_time": "Returns the current system time. Parameters: NONE (use empty args: {})",
    "random_number": "Returns a random integer between 1 and 100. Parameters: NONE (use empty args: {})",
    "fake_weather": "Returns a fake weather report for a given location. Parameters: NONE (use empty args: {})",
    "failing_tool": "A tool that always fails to demonstrate error handling. Parameters: NONE (use empty args: {})"
}


class ReactNode(BaseNode):
    def process(self, user_message: str, conversation_history: list) -> dict:
        # build sys instructions
        tools_desc = "\n".join([f"- {name}: {desc}" for name, desc in AVAILABLE_TOOLS.items()])

        system_instructions = (
            "You are a ReAct agent. Your job is to decide what to do next. \n"
            f"Available tools:\n{tools_desc}\n"
            "\n"
            "You must respond with JSON in one of two formats:\n"
            "1. To use a tool (when you need more information):\n"
            '{action": "use_tool", "tool": "get_time", "args": {}}\n'
            "2. To finish (when you have enough information to answer):\n"
            '{"action": "finish", "answer": Example: "The time is 3PM"}'
            "\n"
            "Think step by step:\n"
            "- What information do I need?\n"
            "- Do I already have it from previous observations?\n"
            "- If not, which tool should I use?\n"
            "- If yes, provide the final answer.\n"
        )


        # initialise tracking
        observations = []
        max_iter = 5

        # ReAct loop
        for iteration in range(max_iter):
            # build observation history for LLM
            obs_text = "\n".join([f"Observation {i+1}: {obs}" for i, obs in enumerate(observations)])

            # build prompt for LLM decision
            if obs_text:
                user_prompt = f"User question: {user_message}\n\nPrevious observations:\n{obs_text}\n\nWhat should I do next?"
            else:
                user_prompt = f"User question: {user_message}\n\nWhat should I do next?"

            messages = [
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_prompt}
            ]


            # Ask LLM for decision
            raw_response = call_llm(messages=messages)

            try:
                start = raw_response.find("{")
                end = raw_response.find("}")
                if start != -1 and end != -1:
                    json_str = raw_response[start:end+1]
                    decision = json.loads(json_str)
                else:
                    decision = {"action": "finish", "answer": "I couldn't process that request."}

            except:
                decision = {"action": "finish", "answer": "I encountered an error processing your request."}

            print(f"[DEBUG] Decision: {decision}")


            # Handle decision
            if decision.get("action" == "use_tool"):
                tool_name = decision.get("tool")
                args = decision.get("args", {})

            # execute tool
                if tool_name in TOOL_MAP:
                    try:
                        result = TOOL_MAP[tool_name](**args)
                        observations.append(f"Tool {tool_name} returned {result}")
                    except Exception as e:
                        observations.append(f"Tool {tool_name} failed: {str(e)}")
                
                else:
                    observations.append(f"Unknown tool: {tool_name}")


            elif decision.get("action") == "finish":
                return {"action": "finish", "answer": decision.get("answer", "No answer provided")}


        return {
            "action": "finish",
            "answer": f"I gathered information but couldn't form a complete answer. Observations: {observations}"
        }
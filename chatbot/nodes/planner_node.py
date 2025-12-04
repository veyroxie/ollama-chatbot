import json
from .base_node import BaseNode
from chatbot.utils.call_llm import call_llm

AVAILABLE_TOOLS = {
    "get_time": "Returns the current system time.",
    "random_number": "Returns a random integer between 1 and 100.",
    "fake_weather": "Returns a fake weather report for a given location."
}


class PlannerNode(BaseNode):
    """
    Planner Node: LLM call #1

    Given a user message, decide whether to:
    - answer directly
    - use one of the available tools

    Returns small 'plan' dict with keys:
    - {}"action": "answer_direct"}
    - {"action": "use_tool", "tool": "get_time", "args": {}}
    """

    def process(self, user_message: str) -> dict:
        
        # 1. Build a description of tools for the prompt
        tools_lines = []

        for name, desc in AVAILABLE_TOOLS.items():
            tools_lines.append(f"- {name}: {desc}")
        tools_block = "\n".join(tools_lines)

        # 2. System-style instructions for planner
        system_instructions = (
            "You are a planning assistant for a chatbot.\n"
            "Your job is NOT to answer the user directly, but to decide whether to:\n"
            "\n"
            "Tools you can choose from:\n"
            f"{tools_block}\n"
            "\n"
            "You must respond ONLY with a single JSON object on one line.\n"
            "Do NOT include any explanation, comments, or markdown.\n"
            "Example of a valid response:\n"
            '{"action": "use_tool", "tool": "get_time", "args": {}}\n'
            '{"action"} can be either "use_tool" or "answer_direct".\n'
            "\n"
            "Rules:\n"
            "- if the question is simple chit-chat, use action 'answer_direct.'\n"
            "- if the user asks about current time, use tool 'get_time'.\n"
            "- if the user asks for a random number, use tool 'random_number'.\n"
            "- if the user asks about weather, use tool 'fake_weather' with args{\"location\":\"<city>\"}.\n"
        )

        full_prompt = (
            f"{system_instructions}\n"
            f"User Message: {user_message}\n"
            "Planner JSON Response:"
        )

        raw = call_llm(full_prompt).strip()
        print("[DEBUG planner ra]:", repr(raw))

        # 3. Parse LLM output as JSON
        try:
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1 and end > start:
                json_str = raw[start:end+1]
            else:
                json_str = raw

            plan = json.loads(json_str)

            action = plan.get("action")

            if action is None:
                raise ValueError("Missing 'action' in planner response.")
            
            if action == "answer_direct":
                plan["action"] = "answer_direct"
                plan["tool"] = None
                plan.setdefault("args", {})

            elif action == "use_tool":
                tool_name = plan.get("tool")
                if not tool_name or tool_name not in AVAILABLE_TOOLS:
                    raise ValueError(f"Invalid or missing 'tool' in planner response: {tool_name}")
                plan["action"] = "use_tool"
                plan["tool"] = tool_name
                plan.setdefault("args", {})

            else:
                tool_name = action
                plan = {
                    "action": "use_tool",
                    "tool": tool_name,
                    "args": plan.get("args", {})
                }

            return plan
        
        except Exception:
            # if anything goes wrong, fall back: answer directly
            return {
                "action": "answer_direct",
                "tool": None,
                "args": {}
            }
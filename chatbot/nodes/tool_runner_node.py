from .base_node import BaseNode
from chatbot.tools.simple_tools import get_time, random_number, fake_weather, failing_tool

TOOL_MAP = {
    "get_time": get_time,
    "random_number": random_number,
    "fake_weather": fake_weather,
    "failing_tool": failing_tool
}

class ToolRunnerNode(BaseNode):
    """
    Node that undertakes tool execution based on the plan from the PlannerNode.
    """
    
    def process(self, plan: dict) -> dict:
        if plan["action"] != "use_tool":                        # if planner node says answer_direct
            # Nothing to do
            return {"result": None}

        tool_name = plan["tool"]                                # which tool to use     
        args = plan.get("args", {})

        if tool_name not in TOOL_MAP:                           # if tool not found
            return {"error": f"Unknown tool: {tool_name}"}

        tool_fn = TOOL_MAP[tool_name]                           # get the tool function
        try:                                                    # call the tool with args
            result = tool_fn(**args)
            return {"result": result}
        except Exception as e:
            return {"error": f"Tool execution failed: {e}"}

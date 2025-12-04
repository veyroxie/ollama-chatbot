import inspect
from typing import Callable, Any, Dict, List
from functools import wraps


class Tool:
    """
    Represents a single tool that chatbot can use.

    Attr:
    - name: tool name (str)
    - description: brief description of tool purpose (str)
    - func: callable function implementing the tool
    - parameters: dict of parameter names to types (from func signature)
    """


    def __init__(self, name: str, description: str, function: Callable):
        self.name = name
        self.description = description
        self.function = function
        self.parameters = self._extract_parameters()


    def _extract_parameters(self) -> Dict[str, Any]:
        """ Extract parameter info fr function sig using introspection"""
        sig = inspect.signature(self.function)
        params = {}

        for param_name, param in sig.parameters.items():
            params[param_name] = {
                "type": param.annotation if param.annotation != inspect.Parameter.empty else Any,   #check if has type
                "required": param.default == inspect.Parameter.empty     # check if has default value
            }

        return params
    

    def to_llm_desc(self) -> str:
        """
        Generate a desc for LLM in clear format.

        Example output:
        "get_time: Returns the current time as a string. No parameters."
        "fake_weather: Returns fake weather for a location. Parameters: location (str)."

        """

        if not self.parameters:
            return f"{self.name}: {self.description} No parameters."
        
        # build param string
        param_parts = []
        required_params = []


        for param_name, param_info in self.parameters.items():
            param_type = param_info["type"].__name__ if hasattr(param_info["type"], "__name__") else str(param_info["type"])
            param_parts.append(f"{param_name} ({param_type})")

        if param_info["required"]:
            required_params.append(param_name)

        params_str = ", ".join(param_parts)
        desc = f"{self.name}({params_str}: {self.description})."

        if required_params:
            desc += f" Required parameters: {', '.join(required_params)}."


    def execute(self, **kwargs) -> Any:
        """
        Call the tool function with given args.

        Validates required parameters before execution.

        """
        return self.function(**kwargs)
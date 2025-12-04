from .base_node import BaseNode
from .tool_runner_node import ToolRunnerNode
from typing import List, Dict, Any


class ChainExecutorNode(BaseNode):
    """
    Executes a chain of tool calls in sequence.
    
    Takes a plan with multiple steps and executes them one by one,
    collecting all results.
    
    Input: 
        plan: List of action dicts or single action dict
    
    Output:
        {"results": [result1, result2, ...], "final_result": combined_output}
    """
    
    def __init__(self):
        self.tool_runner = ToolRunnerNode()
    
    def process(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute plan (single step or multi-step).
        
        Args:
            plan: Either:
                - Single step: {"action": "use_tool", "tool": "...", "args": {...}}
                - Multi-step: {"action": "use_tools", "steps": [{...}, {...}]}
        
        Returns:
            {"results": [...], "summary": "..."}
        """
        action = plan.get("action")
        
        # Single tool execution (backward compatible)
        if action == "use_tool":
            result = self.tool_runner.process(plan)
            return {
                "results": [result],
                "summary": self._format_single_result(plan, result)     # Format single result from steps
            }
        
        # Answer directly (no tools)
        elif action == "answer_direct":
            return {
                "results": [],
                "summary": "No tools needed."
            }
        
        # Multi-step execution (new!)
        elif action == "use_tools":
            steps = plan.get("steps", [])
            return self._execute_chain(steps)
        
        else:
            return {
                "results": [],
                "summary": f"Unknown action: {action}"
            }
    
    def _execute_chain(self, steps: List[Dict]) -> Dict[str, Any]:
        """
        Execute multiple tool calls in sequence.
        
        Args:
            steps: List of step dicts: [{"tool": "...", "args": {...}}, ...]
        
        Returns:
            {"results": [...], "summary": "..."}
        """
        all_results = []
        summary_parts = []
        
        for i, step in enumerate(steps):
            print(f"[ChainExecutor] Executing step {i+1}/{len(steps)}: {step.get('tool')}")
            
            # Execute this step
            result = self.tool_runner.process({
                "action": "use_tool",
                "tool": step.get("tool"),
                "args": step.get("args", {})
            })
            
            all_results.append(result)
            
            # Format result for summary
            if "result" in result:
                summary_parts.append(
                    f"Step {i+1} ({step.get('tool')}): {result['result']}"
                )
            elif "error" in result:
                summary_parts.append(
                    f"Step {i+1} ({step.get('tool')}): ERROR - {result['error']}"
                )
        
        return {
            "results": all_results,
            "summary": "\n".join(summary_parts)
        }
    
    def _format_single_result(self, plan: Dict, result: Dict) -> str:
        """Format a single tool result as a summary string."""
        tool_name = plan.get("tool", "unknown")
        
        if "result" in result:
            return f"{tool_name}: {result['result']}"
        elif "error" in result:
            return f"{tool_name}: ERROR - {result['error']}"
        else:
            return f"{tool_name}: No result"
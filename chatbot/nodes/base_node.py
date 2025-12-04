from abc import ABC, abstractmethod

class BaseNode(ABC):
    """
    Minimal base class for all nodes in the chatbot framework.

    A node:
    - Receives user message (str) and optional context
    - returns response (str or dict, depending on node type)
    - Can accept additional args/kwargs for enhanced functionality
    
    """

    @abstractmethod
    def process(self, user_message: str, *args, **kwargs) -> str:
        """
        Process the user message and return a response.
        
        Args:
        - user_message: user's input message
        - *args: additional positional arguments (e.g. conversation history)
        - **kwargs: additional keyword arguments (e.g. tool outputs)

        Returns:
        - Response (type varies by node: str, dict, etc.)
        
        
        """
        pass
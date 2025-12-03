from abc import ABC, abstractmethod

class BaseNode(ABC):
    """
    Minimal base class for all nodes in the chatbot framework.

    A node:
    - Receives user message (str)
    - returns response (str)
    
    """

    @abstractmethod
    def process(self, user_message: str) -> str:
        """Process the user message and return a response."""
        pass
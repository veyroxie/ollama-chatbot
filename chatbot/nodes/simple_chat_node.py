from .base_node import BaseNode
from chatbot.utils.call_llm import call_llm

class SimpleChatNode(BaseNode):
    """
    Simplest possible chat node:
    - takes user message as input
    - builds basic prompt w system instructions
    - sends to call_llm
    - returns LLM response as output string
    """
    def process(self, user_message: str) -> str:
        """
        Process the user message by calling the LLM and returning its response.

        Args:
            user_message (str): The message from the user.
        """

        # simple system instructions
        system_instructions = (
            "You are a helpful AI assistant designed to assist users with their questions and provide information."
            "Answer clearly and concisely."
        )

        # combine into full prompt string
        full_prompt = (
            f"{system_instructions}\n\n"
            f"User: {user_message}\n"
            f"Assistant:   "
        )


        # call llm utility function
        reply = call_llm(full_prompt)

        return reply.strip()
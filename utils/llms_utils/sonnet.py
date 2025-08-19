# File to generate code reviews from vulnerability-fixing
# commits with Anthropic's model with different prompts
from dotenv import load_dotenv
from .llm import LLM
import anthropic
import os

class Sonnet(LLM):
    """
    Class to handle the Anthropic models for code review generation.
    """
    def __init__(self, model_name: str):
        super().__init__(model_name, retry_max=5)
        load_dotenv()
        self.client = anthropic.Anthropic(api_key=os.getenv("anthropic_api_key"))
    
    def ask(self, message: list[dict], max_length: int = 1024, name: str = 'zero-shot') -> str:
        """
        Generate a response from the Anthropic model based on the input message.
        
        Args:
            message (list[dict]): The input message for the LLM.
            max_length (int): The maximum length of the generated response.
            name (str): The name of the prompt technique.

        Returns:
            str: The generated response from the LLM.
        """
        input_message = [m for m in message if m.get('role') == 'user']
        instruction = next((m['content'] for m in message if m.get('role') == 'system'), '')

        response = self.client.messages.create(
            max_tokens=max_length,
            model=self.model_name,
            messages=input_message,
            system=instruction,
        )
        return response.content[0].text if response.content else ""

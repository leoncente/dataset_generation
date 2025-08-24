# File to generate code reviews from vulnerability-fixing
# commits with OpenAI's model with different prompts
from openai import OpenAI
from dotenv import load_dotenv
from .llm import LLM
import os

class Gpt(LLM):
    """
    Class to handle the OpenAI models for code review generation.
    """
    def __init__(self, model_name: str):
        super().__init__(model_name)
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OpenAI_API_KEY"))
    
    def ask(self, message: list[dict], max_length: int = 1024, name: str = 'zero-shot') -> str:
        """
        Generate a response from the OpenAI model based on the input message.
        
        Args:
            message (list[dict]): The input message for the LLM.
            max_length (int): The maximum length of the generated response.
            name (str): The name of the prompt technique.

        Returns:
            str: The generated response from the LLM.
        """
        
        input_message = next((m['content'] for m in message if m.get('role') == 'user'), '')
        instruction = next((m['content'] for m in message if m.get('role') == 'system'), '')

        reasoning = {"effort": "medium"}
        if name == 'zero-shot':
            reasoning = {"effort": "low"}
        response = self.client.responses.create(
            reasoning=reasoning,
            model=self.model_name,
            input=input_message,
            max_output_tokens=max_length,
            instructions=instruction,
        )

        text = response.output_text
        return text.strip()

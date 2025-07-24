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
    
    def generate_cot(self, commit_info: str, prompt: str) -> str:
        return f'cot {self.model_name}'
    
    def generate_self_reflection(self, commit_info: str, prompt: str) -> str:
        return f'self-reflection {self.model_name}'
    
    def generate_zero_shot(self, commit_info: str, prompt: str) -> str:
        return f'zero-shot {self.model_name}'

OpenAI_API_Key = os.getenv("OpenAI_API_KEY")
client = OpenAI(api_key=OpenAI_API_Key)

def ask_openai(message: list[dict], model: str) -> str:
    """
    Ask OpenAI's model with a message and return the response.
    
    Args:
        message (list[dict]): The message to send to the model.
        model (str): The model to use for the request.
    
    Returns:
        str: The response from the model.
    """
    response = client.responses.create(
        model=model,
        input=message
    )
    return response.output_text

def generate_openai(model: str, prompt: dict, commit_details: dict, version: str) -> str:
    """
    Generate a response using the OpenAI model.
    
    Args:
        model (str): The model to use for the request.
        prompt (dict): The prompt to use for the request.
        commit_details (dict): The commit details to include in the request.
        version (str): The version of the experiment.

    Returns:
        str: The response from the model.
    """
    return ''


if __name__ == "__main__":
    print("Testing OpenAI API Key...")

    model = "gpt-4o"
    message = [
        {
            "role": "developer",
            "content": "Talk like a pirate."
        },
        {
            "role": "user",
            "content": "Are semicolons optional in JavaScript? answer with one word."
        }
    ]

    print(ask_openai(message, model))
# File to generate code reviews from vulnerability-fixing
# commits with Anthropic's model with different prompts
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

anthropic_api_key = os.getenv("anthropic_api_key")
client = anthropic.Anthropic(api_key=anthropic_api_key)

def ask_anthropic(message: list[dict], model: str) -> str:
    """
    Ask Anthropic's model with a message and return the response.
    
    Args:
        message (list[dict]): The message to send to the model.
        model (str): The model to use for the request.
    
    Returns:
        str: The response from the model.
    """
    response = client.messages.create(
        max_tokens=1000,
        model=model,
        #system="You are a helpful assistant.",
        messages=message
    )
    return response.content[0].text if response.content else ""

def generate_anthropic(model: str, prompt: dict, commit_details: dict, version: str) -> str:
    """
    Generate a response using the Anthropic model.
    
    Args:
        model (str): The model to use for the request.
        prompt (dict): The prompt to use for the request.
        commit_details (dict): The commit details to include in the request.
        version (str): The version of the experiment.

    Returns:
        str: The generated response from the model.
    """
    return ''

if __name__ == "__main__":
    print("Testing Anthropic API Key...")

    model = "claude-opus-4-20250514"
    message = [
        {
            "role": "user",
            "content": "Why is the ocean salty?"
        }
    ]

    print(ask_anthropic(message, model))
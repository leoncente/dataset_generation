# File to generate code reviews from vulnerability-fixing
# commits with OpenAI's model with different prompts
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

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
# File to generate code reviews from vulnerability-fixing
# commits with Anthropic's model with different prompts
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
from dotenv import load_dotenv
from .llm import LLM
import anthropic
import copy
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

    def generate_batch(self, batch_prompts: list[tuple[dict, dict]]) -> str:
        """
        Generate responses for a batch of prompts.

        Args:
            batch_prompts (list[tuple[dict, dict]]): A list of tuples containing commit_info and prompt.
        Returns:
            str: the reference to the batch job created.
        """
        requests = []
        for commit_info, prompt in batch_prompts:
            p = copy.deepcopy(prompt)
            commit_text = f'Commit Message: {commit_info["message"]}\n\nDiff:\n{commit_info["patch"]}'

            for prompt_element in p['prompt']:
                if prompt_element['role'] == 'user':
                    prompt_element['content'] = prompt_element['content'].replace('[Insert fix content here]', commit_text)

            input_message = [m for m in p['prompt'] if m.get('role') == 'user']
            instruction = next((m['content'] for m in p['prompt'] if m.get('role') == 'system'), '')

            requests.append(Request(
                custom_id=commit_info["sha"],
                params=MessageCreateParamsNonStreaming(
                    model=self.model_name,
                    max_tokens=3072,
                    messages=input_message,
                    system=instruction,
                )
            ))
        
        responses = self.client.messages.batches.create(requests=requests)

        return responses.id
            
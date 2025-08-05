# File to generate code reviews from vulnerability-fixing
# commits with Google's model with different prompts

from transformers import T5ForConditionalGeneration, AutoTokenizer
from .llm import LLM
import torch
import gc

class Flan(LLM):
    """
    Class to handle the Flan models for code review generation.
    """
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name, device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model.eval()

    def end_model(self):
        del self.model
        del self.tokenizer
        gc.collect()
        torch.cuda.empty_cache()
        for i in range(torch.cuda.device_count()):
            with torch.cuda.device(i):
                torch.cuda.empty_cache()

    def ask(self, message: list[dict], enable_thinking: bool = False, max_length: int = 1024) -> str:
        """
        Generate a response from the Flan model based on the input message.
        
        Args:
            message (list[dict]): The input message for the LLM.
            enable_thinking (bool): Whether to enable thinking in the response.
            max_length (int): The maximum length of the generated response.

        Returns:
            str: The generated response from the LLM.
        """
        if self.tokenizer.chat_template is not None:
            prompt = self.tokenizer.apply_chat_template(
                message,
                add_generation_prompt=True,
                enable_thinking=enable_thinking
            )
        else:
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in message])

        inputs = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(inputs, max_length=max_length)
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

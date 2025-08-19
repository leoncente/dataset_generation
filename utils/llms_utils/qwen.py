# File to generate code reviews from vulnerability-fixing
# commits with Qwen's model with different prompts using Hugging Face Transformers

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from .llm import LLM
import torch
import gc

class Qwen(LLM):
    """
    Class to handle the Qwen models for code review generation.
    """
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        quantization_config = BitsAndBytesConfig(
            load_in_8_bit=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", quantization_config=quantization_config)
        self.model.eval()
        self.device = self.model.device
    
    def end_model(self):
        del self.model
        del self.tokenizer
        gc.collect()
        torch.cuda.empty_cache()
        for i in range(torch.cuda.device_count()):
            with torch.cuda.device(i):
                torch.cuda.empty_cache()

    def ask(self, message: list[dict], enable_thinking: bool = False, max_length: int = 1024, name: str = 'zero-shot') -> str:
        """
        Generate a response from the Qwen model based on the input message.
        
        Args:
            message (list[dict]): The input message for the LLM.
            enable_thinking (bool): Whether to enable thinking in the response.
            max_length (int): The maximum length of the generated response.
            name (str): The name of the prompt technique.

        Returns:
            str: The generated response from the LLM.
        """
        input_ids = self.tokenizer.apply_chat_template(
            message,
            add_generation_prompt=True,
            return_tensors="pt",
            enable_thinking= (name == 'cot')
        ).to(self.device)

        # Create attention_mask manually
        attention_mask = (input_ids != self.tokenizer.eos_token_id).long()

        with torch.no_grad():
            output = self.model.generate(
                input_ids=input_ids,
                max_new_tokens=max_length,
                attention_mask=attention_mask
            )

        text = self.tokenizer.decode(output[0], skip_special_tokens=True)

        text = text.split('<think>')[-1] if '</think>' not in text else text
        text = text.split('</think>')[-1] if '</think>' in text else text
        # Remove all \n at the start of the text
        text = text.lstrip('\n')

        return text
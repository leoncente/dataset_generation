# File to generate code reviews from vulnerability-fixing
# commits with Google's model with different prompts

from transformers import T5ForConditionalGeneration, AutoTokenizer, BitsAndBytesConfig
from .llm import LLM
import torch
import gc

class Flan(LLM):
    """
    Class to handle the Flan models for code review generation.
    """
    def __init__(self, model_name: str):
        super().__init__(model_name)
        quantization_config = BitsAndBytesConfig(
            load_in_8_bit=True)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name, device_map="auto", quantization_config=quantization_config)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model.eval()

        # Ensure pad/eos ids are set (important for T5/UL2)
        if self.model.config.pad_token_id is None and self.tokenizer.pad_token_id is not None:
            self.model.config.pad_token_id = self.tokenizer.pad_token_id
        if self.model.config.eos_token_id is None and self.tokenizer.eos_token_id is not None:
            self.model.config.eos_token_id = self.tokenizer.eos_token_id

        # Cache a reasonable encoder context limit
        cfg = self.model.config
        # Prefer model config if present, else tokenizer default, else safe fallback
        self.max_ctx = (
            getattr(cfg, "max_position_embeddings", None)
            or getattr(cfg, "n_positions", None)
            or (self.tokenizer.model_max_length if self.tokenizer.model_max_length and self.tokenizer.model_max_length < 10**9 else None)
            or 2048  # FLAN-UL2 typical context
        )

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
        Generate a response from the Flan model based on the input message.
        
        Args:
            message (list[dict]): The input message for the LLM.
            enable_thinking (bool): Whether to enable thinking in the response.
            max_length (int): The maximum length of the generated response.
            name (str): The name of the prompt technique.

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
        
        # Tokenize with truncation to avoid "sequence length > max" errors
        enc = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_ctx,
            padding=False,
        )
        enc = {k: v.to(self.model.device) for k, v in enc.items()}

        # Optional hard ceiling on total length (input + output), extra safety
        total_cap = self.max_ctx + max_length

        #inputs = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **enc,
                max_new_tokens=max_length,
                eos_token_id=self.model.config.eos_token_id,
                pad_token_id=self.model.config.pad_token_id,
            )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

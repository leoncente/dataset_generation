# File to generate code reviews from vulnerability-fixing
# commits with Qwen's model with different prompts using Hugging Face Transformers

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def load_qwen(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
    model.eval()

    device = model.device

    return model, tokenizer, device

def ask_qwen(message: list[dict], model_name: str, enable_thinking: bool) -> str:
    model, tokenizer, device = load_qwen(model_name)

    input_ids = tokenizer.apply_chat_template(
        message,
        add_generation_prompt=True,
        return_tensors="pt",
        enable_thinking=enable_thinking
    ).to(device)

    # Create attention_mask manually
    attention_mask = (input_ids != tokenizer.eos_token_id).long()

    with torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            max_new_tokens=1024,
            #do_sample=True,
            #temperature=0.7,
            #top_p=0.9,
            attention_mask=attention_mask
        )

    return tokenizer.decode(output[0], skip_special_tokens=True)

def generate_qwen(model: str, prompt: dict, commit_details: dict, version: str) -> str:
    """
    Generate a response using the Qwen model.

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
    print("Testing Qwen model...")

    #model_id = "Qwen/Qwen3-0.6B"
    model_id = "Qwen/Qwen3-14B"
    prompt = "Hello, please introduce yourself and tell me what you can do."
    message = [{"role": "user", "content": prompt}]

    response = ask_qwen(message, model_id, enable_thinking=False)
    print(response)

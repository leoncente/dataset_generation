# File to generate code reviews from vulnerability-fixing
# commits with Google's model with different prompts

from transformers import T5ForConditionalGeneration, AutoTokenizer

def ask_flan_ul2(message: list[dict], model: str, enable_thinking: bool) -> str:
    model = T5ForConditionalGeneration.from_pretrained(model, device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained(model.name_or_path)

    if tokenizer.chat_template is not None:
        prompt = tokenizer.apply_chat_template(
            message,
            add_generation_prompt=True,
            enable_thinking=enable_thinking
        )
    else:
        prompt = tokenizer.apply_chat_template(message)
    
    device = model.device

    inputs = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    outputs = model.generate(inputs, max_length=1024)
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def generate_flan_ul2(model: str, prompt: dict, commit_details: dict, version: str) -> str:
    """
    Generate a response using the Flan-UL2 model.
    
    Args:
        model (str): The model to use for the request.
        prompt (dict): The prompt to use for the request.
        commit_details (dict): The commit details to include in the request.

    Returns:
        str: The generated response from the model.
    """
    return ''


if __name__ == "__main__":
    model = T5ForConditionalGeneration.from_pretrained("google/flan-ul2", device_map="auto")                                                                 
    tokenizer = AutoTokenizer.from_pretrained("google/flan-ul2")

    input_string = "Answer the following question by reasoning step by step. The cafeteria had 23 apples. If they used 20 for lunch, and bought 6 more, how many apple do they have?"                                               

    device = model.device

    inputs = tokenizer(input_string, return_tensors="pt").input_ids.to(device)
    outputs = model.generate(inputs, max_length=1024)

    print(tokenizer.decode(outputs[0], skip_special_tokens=True))

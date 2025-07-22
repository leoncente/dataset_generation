# File to generate code reviews from vulnerability-fixing
# commits with Qwen's model with different prompts

from mlx_lm import load, generate

def ask_qwen(message: list[dict], model: str, enable_thinking: bool) -> str:

    model, tokenizer = load(model)
    if tokenizer.chat_template is not None:
        prompt = tokenizer.apply_chat_template(
            message,
            add_generation_prompt=True,
            enable_thinking=enable_thinking
        )
    response = generate(
        model,
        tokenizer,
        prompt=prompt,
        verbose=False,
        max_tokens=1024
    )
    return response

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

    model, tokenizer = load("Qwen/Qwen3-0.6B-MLX-6bit")
    prompt = "Hello, please introduce yourself and tell me what you can do."
    message = [{"role": "user", "content": prompt}]

    response = ask_qwen(message, "Qwen/Qwen3-0.6B-MLX-6bit", enable_thinking=True)
    print(response)
from .gpt import generate_openai
from .qwen import generate_qwen
from .sonnet import generate_anthropic
from .flan_ul2 import generate_flan_ul2

def generate_code_review(commit_info: dict, provider: str, model: str, prompt: dict, version: str) -> str:
    """
    Generate a code review for the given parameters.

    Args:
        sha (str): The commit SHA.
        provider (str): The provider of the model.
        model (str): The model identifier.
        prompt (dict): The prompt to use for generation.
        version (str): The version of the experiment.
        
    Returns:
        dict: The generated code review.
    """

    if provider == "OpenAI":
        return generate_openai(model, prompt, commit_info, version)
    elif provider == "Qwen":
        return generate_qwen(model, prompt, commit_info, version)
    elif provider == "Sonnet":
        return generate_anthropic(model, prompt, commit_info, version)
    elif provider == "Google":
        return generate_flan_ul2(model, prompt, commit_info, version)
    else:
        raise ValueError(f"Unknown provider: {provider}")

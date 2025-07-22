
from ..os_utils import exists_or_create_folder, exists_file, read_json_file, write_json_file
import os

def get_models(least_expensive: bool = False, OpenAI: bool = True, Google: bool = True, Qwen: bool = True, Sonnet: bool = True) -> dict:
    """
    Retrieve the available models for code review generation.
    
    Returns:
        dict: A dictionary mapping model names to their identifiers.
    """
    models = {}
    if OpenAI:
        models["OpenAI"] = "gpt-3.5-turbo" if least_expensive else "gpt-4o"
    if Google:
        models["Google"] = "google/flan-ul2"
    if Qwen:
        models["Qwen"] = "Qwen/Qwen3-0.6B-MLX-6bit" if least_expensive else "Qwen/Qwen3-4B-MLX-bf16"
    if Sonnet:
        models["Sonnet"] = "claude-3-haiku-20240307" if least_expensive else "claude-sonnet-4-20250514"

    return models

def generated_prompt_model(sha: str, provider: str, model: str, prompt_name: str, version: str, path: str = "LLMs/Results") -> bool:
    """
    Check if the result for the given SHA, provider, model, and prompt already exists.
    
    Args:
        sha (str): The commit SHA.
        provider (str): The provider of the model.
        model (str): The model identifier.
        prompt_name (str): The name of the prompt.
        version (str): The version of the experiment.
    
    Returns:
        bool: True if the result exists, False otherwise.
    """
    
    results_folder = os.path.join(path, version, prompt_name)
    exists_or_create_folder(results_folder)

    if not exists_file(results_folder, f"{sha}.json"):
        return False
    
    generated_review = read_json_file(results_folder, f"{sha}.json")
    if provider not in generated_review or model not in generated_review[provider] or generated_review[provider][model] is None:
        return False

    return True

def save_code_review(code_review: str, sha: str, provider: str, model: str, prompt_name: str, version: str, path: str = "LLMs/Results"):
    """
    Save the generated code review to a file.
    
    Args:
        code_review (str): The generated code review.
        sha (str): The commit SHA.
        model (str): The model identifier.
        prompt_name (str): The name of the prompt.
        version (str): The version of the experiment.
    """
    
    results_folder = os.path.join(path, version, prompt_name)
    exists_or_create_folder(results_folder)

    generated_reviews = {}
    if exists_file(results_folder, f"{sha}.json"):
        generated_reviews = read_json_file(results_folder, f"{sha}.json")

    generated_reviews[provider] = generated_reviews.get(provider, {})
    generated_reviews[provider][model] = code_review

    write_json_file(results_folder, f"{sha}.json", generated_reviews)

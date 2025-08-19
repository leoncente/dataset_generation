
from ..os_utils import exists_or_create_folder, exists_file, read_json_file, write_json_file
from .sonnet import Sonnet
from .flan import Flan
from .qwen import Qwen
from .gpt import Gpt
from .llm import LLM
import json
import os

LLM_REGISTRY : dict[str, type[LLM]] = {
    "OpenAI": Gpt,
    "Google": Flan,
    "Qwen": Qwen,
    "Sonnet": Sonnet
}

def create_llm(provider: str, model: str) -> LLM:
    """
    Create an instance of the LLM based on the provider and model.
    
    Args:
        provider (str): The provider of the model (e.g., "OpenAI", "Google", "Qwen", "Sonnet").
        model (str): The model identifier.
    
    Returns:
        LLM: An instance of the LLM class for the specified provider and model.
    """
    if provider not in LLM_REGISTRY:
        raise ValueError(f"Provider {provider} is not supported.")
    
    llm_class = LLM_REGISTRY[provider]
    return llm_class(model_name=model)

def get_models(least_expensive: bool = False, OpenAI: bool = True, Google: bool = True, Qwen: bool = True, Sonnet: bool = True) -> dict:
    """
    Retrieve the available models for code review generation.
    
    Returns:
        dict: A dictionary mapping model names to their identifiers.
    """
    models = {}
    if OpenAI:
        models["OpenAI"] = "gpt-3.5-turbo" if least_expensive else "gpt-5"
    if Google:
        models["Google"] = "google/flan-t5-small" if least_expensive else "google/flan-ul2"
    if Qwen:
        models["Qwen"] = "Qwen/Qwen3-0.6B" if least_expensive else "Qwen/Qwen3-32B"
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
    if provider not in generated_review or model not in generated_review[provider] or generated_review[provider][model] is None or generated_review[provider][model] == "":
        return False

    return True

def save_code_review(code_review: str, sha: str, provider: str, model: str, prompt_name: str, version: str, path: str = "LLMs/Results", prompt_used: str = None):
    """
    Save the generated code review to a file.
    
    Args:
        code_review (str): The generated code review.
        sha (str): The commit SHA.
        model (str): The model identifier.
        prompt_name (str): The name of the prompt.
        version (str): The version of the experiment.
        path (str): The base path where results are stored.
        prompt_used (str): The name of the prompt used for generation.
    """
    
    results_folder = os.path.join(path, version, prompt_name)
    exists_or_create_folder(results_folder)

    generated_reviews = {}
    if exists_file(results_folder, f"{sha}.json"):
        generated_reviews = read_json_file(results_folder, f"{sha}.json")

    generated_reviews[provider] = generated_reviews.get(provider, {})
    generated_reviews[provider][model] = code_review

    if prompt_used:
        if "prompt_used" in generated_reviews:
            p1 = json.dumps(generated_reviews["prompt_used"])
            p2 = json.dumps(prompt_used)
            if p1 != p2:
                if prompt_name == "self-reflection":
                    generated_reviews[provider]["prompt_used"] = prompt_used
                else:
                    raise ValueError(f"Prompt used does not match existing prompt")
            del generated_reviews["prompt_used"]
        if prompt_name != "self-reflection":
            generated_reviews["prompt_used"] = prompt_used
        else:
            generated_reviews[provider]["prompt_used"] = prompt_used

    write_json_file(results_folder, f"{sha}.json", generated_reviews)

def get_code_review(sha: str, provider: str, model: str, prompt_name: str, version: str, path: str = "LLMs/Results") -> str:
    """
    Retrieve the generated code review for the given parameters.
    
    Args:
        sha (str): The commit SHA.
        provider (str): The provider of the model.
        model (str): The model identifier.
        prompt_name (str): The name of the prompt.
        version (str): The version of the experiment.
    
    Returns:
        str: The generated code review if it exists, otherwise an empty string.
    """
    
    results_folder = os.path.join(path, version, prompt_name)
    if not exists_file(results_folder, f"{sha}.json"):
        raise FileNotFoundError(f"No results found for SHA {sha} in {results_folder}")

    generated_reviews = read_json_file(results_folder, f"{sha}.json")
    if provider not in generated_reviews or model not in generated_reviews[provider]:
        raise ValueError(f"No review found for provider {provider} and model {model} in {results_folder}")
    
    return generated_reviews[provider][model]

def get_code_reviews(sha: str, prompt_name: str, version: str, path: str = "LLMs/Results") -> dict:
    """
    Retrieve all code reviews for a specific SHA and prompt name.
    
    Args:
        sha (str): The commit SHA.
        prompt_name (str): The name of the prompt.
        version (str): The version of the experiment.
        path (str): The base path where results are stored.
    
    Returns:
        dict: A dictionary containing code reviews for all providers and models.
    """
    
    results_folder = os.path.join(path, version, prompt_name)
    if not exists_file(results_folder, f"{sha}.json"):
        raise FileNotFoundError(f"No results found for SHA {sha} in {results_folder}")

    return read_json_file(results_folder, f"{sha}.json")

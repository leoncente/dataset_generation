from .os_utils import exists_or_create_folder
from .utils import Utils
from .llms_utils.llms_utils import get_models, generated_prompt_model, save_code_review, create_llm, get_code_review, get_code_reviews
from .llms_utils.llm import LLM

def get_prompts(version: str, path: str = "LLMs/Prompts") -> list[dict]:
    """
    Retrieve prompts for the given version.

    Args:
        version (str): The version of the experiment.
    Returns:
        list[dict]: A list of prompts for the version.  
    """
    return Utils.get_prompts(version, path)

__all__ = [
    'exists_or_create_folder',
    'get_prompts',
    'Utils',
    'get_models',
    'generated_prompt_model',
    'save_code_review',
    'get_code_review',
    'get_code_reviews',
    'create_llm',
    'LLM'
]
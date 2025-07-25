from .os_utils import exists_or_create_folder
from .utils import Utils
from .llms_utils.llms_utils import get_models, generated_prompt_model, save_code_review
from .llms_utils.llms import generate_code_review

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
    'generate_code_review',
    'save_code_review'
]

class LLM:
    """
    Base class for Language Model (LLM) providers.
    This class should be extended by specific LLM implementations.
    """
    
    def __init__(self, model_name: str):
        self.model_name = model_name

    def ask(self, message: str, *args, **kwargs) -> str:
        """
        Method to be implemented by subclasses to generate a response from the LLM.
        Accepts 'message' as required argument, plus additional variable arguments.

        Args:
            message (str): The input message for the LLM.
            *args: Additional positional arguments for the LLM.
            **kwargs: Additional keyword arguments for the LLM.

        Returns:
            str: The generated response from the LLM.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def generate(self, commit_info: str, prompt: str) -> str:
        """
        Call the proper method to generate a code review based on the prompt technique.

        Args:
            commit_info (str): Information about the commit.
            prompt (str): The input prompt for the LLM.

        Returns:
            str: The generated code review from the LLM.
        """
        match prompt['name']:
            case 'cot':
                return self.generate_cot(commit_info, prompt)
            case 'self-reflection':
                return self.generate_self_reflection(commit_info, prompt)
            case 'zero-shot':
                return self.generate_zero_shot(commit_info, prompt)
            case _:
                raise ValueError(f"Unknown prompt technique: {prompt['name']}")
        
    def generate_cot(self, commit_info: str, prompt: str) -> str:
        """
        Generate a code review using the Chain of Thought (CoT) technique.

        Args:
            commit_info (str): Information about the commit.
            prompt (str): The input prompt for the LLM.

        Returns:
            str: The generated code review using CoT.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def generate_self_reflection(self, commit_info: str, prompt: str) -> str:
        """
        Generate a code review using the Self-Reflection technique.

        Args:
            commit_info (str): Information about the commit.
            prompt (str): The input prompt for the LLM.

        Returns:
            str: The generated code review using Self-Reflection.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def generate_zero_shot(self, commit_info: str, prompt: str) -> str:
        """
        Generate a code review using the Zero-Shot technique.

        Args:
            commit_info (str): Information about the commit.
            prompt (str): The input prompt for the LLM.

        Returns:
            str: The generated code review using Zero-Shot.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def end_model(self):
        """
        Clean up resources used by the model.
        This method should be called when the model is no longer needed.
        """
        pass


class LLM:
    """
    Base class for Language Model (LLM) providers.
    This class should be extended by specific LLM implementations.
    """
    
    def __init__(self, model_name: str, retry_max: int = 15):
        self.model_name = model_name
        self.retry_max = retry_max

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
    
    def generate(self, commit_info: dict, prompt: dict) -> tuple[str, list[dict]]:
        """
        Call the proper method to generate a code review based on the prompt technique.

        Args:
            commit_info (dict): Information about the commit.
            prompt (dict): The prompt to use for code review generation.

        Returns:
            str: The generated code review from the LLM.
            list[dict]: The prompt used for the generation.
        """
        commit_text = f'Commit Message: {commit_info['message']}\n\nDiff:\n{commit_info['patch']}'

        max_length = 1024
        if prompt['name'] == 'cot':
            max_length = 3072
        for prompt_element in prompt['prompt']:
            if prompt_element['role'] == 'user':
                prompt_element['content'] = prompt_element['content'].replace('[Insert fix content here]', commit_text)
                
                if prompt['name'] == 'self-reflection':
                    prompt_element['content'] = prompt_element['content'].replace('[previous_response]', prompt['code_review'])
        
        retry_count = 0
        while retry_count < self.retry_max:
            text = self.ask(message=prompt['prompt'], name=prompt['name'], max_length=max_length)
            text = text.strip()
            if text != '' and text != None:
                break
            retry_count += 1
            print(f"Retrying {self.model_name} generation, attempt {retry_count}/{self.retry_max}")
        
        if retry_count == self.retry_max:
            return '', prompt['prompt']

        return text, prompt['prompt']
    
    def end_model(self):
        """
        Clean up resources used by the model.
        This method should be called when the model is no longer needed.
        """
        pass

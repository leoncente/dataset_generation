from .gh_utils import get_remaining_calls, wait_for_rate_limit_reset, get_commit_details
from .db_utils import DatabaseConnection
from .os_utils import exists_or_create_folder, exists_file, read_json_file, write_json_file, read_all_files_in_folder
import os

class Utils:
    def __init__(self, db_host: str, db_user: str, db_password: str, db_port: int, db_name: str):

        self.db = DatabaseConnection(
            db_host=db_host,
            db_user=db_user,
            db_password=db_password,
            db_port=db_port,
            db_name=db_name
        )

    @staticmethod
    def generated_prompt_model(sha, model, prompt_name, version):
        # Check if the result already exists
        return False

    @staticmethod
    def generate_code_review(sha, model, prompt, version):
        # Generate the code review
        return "code review"

    @staticmethod
    def save_code_review(code_review, sha, model, prompt_name, version):
        # Save the code review
        pass

    @staticmethod
    def get_prompts(version: str, path: str = "LLMs/Prompts") -> list[dict]:
        """
        Retrieve prompts for the given version.

        Args:
            version (str): The version of the experiment.
        Returns:
            list[dict]: A list of prompts for the version.
        """
        prompts_folder = os.path.join(path, version)
        prompts_files = read_all_files_in_folder(prompts_folder)
        prompts = []
        for f in prompts_files:
            if f.endswith('.json'):
                data = read_json_file(prompts_folder, f)
                data['name'] = os.path.splitext(f)[0]
                prompts.append(data)
        # Invert the list to have zero-shot prompts before self-reflextion
        # since the latter needs the former to be generated.
        prompts.reverse()
        return prompts

    def get_vulnerability_fixes(self, version: str, limit: int = 50, path: str = "LLMs/Results") -> list[str]:
        """
        Retrieve vulnerability-fixing commits from the folders if they exist.
        If not, it will call the database to get the commits.

        Args:
            version (str): The version of the experiment.
            limit (int): The maximum number of commits to retrieve (0 for no limit).
            path (str): The path to the results folder.
        Returns:
            list[str]: A list of vulnerability-fixing commit SHAs.
        """
        results_folder = os.path.join(path, version)
        exists_or_create_folder(results_folder)

        shas = []
        if exists_file(results_folder, 'shas.json'):
            shas = read_json_file(results_folder, 'shas.json')

        if len(shas) >= limit and limit > 0:
            print(f"Using {len(shas)} shas from the file for version {version}.")
            return shas

        # If we don't have enough shas, get more from the database
        more_shas = self.db.get_vulnerability_fixes(version)

        # Add the new shas to the existing ones, ensuring we don't exceed 50
        shas = list(set(shas))
        shas.extend(more_shas)
        shas = list(set(shas))
        if limit > 0:
            shas = shas[:limit]

        # Save the shas to the file
        write_json_file(results_folder, 'shas.json', shas)

        return shas
    
    def get_commit_info(self, sha: str) -> dict:
        """
        Get the commit details for a given SHA.

        Args:
            sha (str): The commit SHA.

        Returns:
            dict: The commit details.
        """
        if exists_file("LLMs/Results", f"{sha}.json"):
            commit_info = read_json_file("LLMs/Results", f"{sha}.json")
            return commit_info
        
        repo_info = self.db.get_commit_info(sha)

        while True:
            remaining_calls = get_remaining_calls()
            if remaining_calls > 5:
                break
            wait_for_rate_limit_reset()

        commit_info = get_commit_details(
            owner=repo_info['owner'],
            repo=repo_info['name'],
            sha=sha
        )

        write_json_file("LLMs/Results", f"{sha}.json", commit_info)

        return commit_info
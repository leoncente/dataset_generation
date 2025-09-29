from dotenv import load_dotenv
import requests
import time
import os

load_dotenv()

git_token = os.getenv("git_token")

def get_remaining_calls() -> int:
    """
    Get the remaining API calls for the GitHub token.

    Returns:
        int: The number of remaining API calls.
    """
    headers = {
        "Authorization": f"Bearer {git_token}"
    }
    response = requests.get("https://api.github.com/rate_limit", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["rate"]["remaining"]
    return 0

def wait_for_rate_limit_reset():
    """
    Wait until the rate limit resets.
    """
    headers = {
        "Authorization": f"Bearer {git_token}"
    }
    response = requests.get("https://api.github.com/rate_limit", headers=headers)
    if response.status_code == 200:
        data = response.json()
        reset_time = data["rate"]["reset"]
        current_time = time.time()
        if reset_time > current_time:
            wait_time = reset_time - current_time
            time.sleep(wait_time)

def get_commit_details(owner: str, repo: str, sha: str) -> dict:
    """
    Get the details of a commit from GitHub.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        sha (str): The SHA of the commit.

    Returns:
        dict: The details of the commit.
    """
    headers = {
        "Authorization": f"Bearer {git_token}"
    }
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        commit_message = response_data['commit']['message']
        for file in response_data['files']:
            if file['filename'].endswith('.java') and 'patch' in file and file['patch'] is not None:
                raw_url = file['raw_url']
                file_response = requests.get(raw_url)
                if file_response.status_code == 200:
                    file_response = file_response.text
                    break
                else:
                    raise Exception(f"Failed to fetch file content for {owner}/{repo} with sha {sha}:\n {file['filename']}")

        return {
            "sha": sha,
            "message": commit_message,
            "filename": file['filename'],
            "patch": file['patch'],
            "raw_url": raw_url,
            "raw_content": file_response
        }
    
    raise Exception(f"Failed to fetch commit details for {owner}/{repo} with sha {sha}. Status code: {response.status_code}")

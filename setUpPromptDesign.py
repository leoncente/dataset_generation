# Set up the prompt design experiment to test different prompting techniques
#
# EXPERIMENT:
# Read the database for those commites evaluated as "vulnerability-fixing"
# and randomly select 50 of them.
# The prompts will be designed to generate code reviews for these commits.
# The prompts used will be in the folder LLMs/Prompts under a VX folder
# where X is the version of the experiment.
# The results will be saved in the folder LLMs/Results under a VX folder
# where X is the version of the experiment.
# This script is meant to be run without any arguments and generate the
# necessary files for every prompt design experiment, if it is not already done.

from dotenv import load_dotenv
import os
from utils import *
from utils import Utils

load_dotenv()

db_host = os.getenv("db_host")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_port = os.getenv("db_port")
db_name = os.getenv("db_name")


# Repeat the process for each version of the experiment.
folder = "LLMs/Prompts"
versions = [v for v in os.listdir(folder) if os.path.isdir(os.path.join(folder, v))]

util = Utils(
    db_host=db_host,
    db_user=db_user,
    db_password=db_password,
    db_port=db_port,
    db_name=db_name
)

for version in versions:
    # Read the database for vulnerability-fixing commits
    # and randomly select 50 of them or see if they are already selected.
    shas = util.get_vulnerability_fixes(version, limit=50)
    
    # Read the prompts for the version
    prompts = get_prompts(version)

    # Read the available models
    models = get_models(least_expensive=True)

    # Create the results folder if it does not exist
    results_folder = f"LLMs/Results/{version}"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    
    # Generate the code reviews for each prompt and model
    # if it has not been done already.
    for prompt in prompts:
        # Create a subfolder for the prompt if it does not exist
        prompt_folder = os.path.join(results_folder, prompt['name'])
        exists_or_create_folder(prompt_folder)

        for sha in shas:
            # Get the commit info
            commit_info = util.get_commit_info(sha)
            for provider in models.keys():
                # Check if the result already exists
                if generated_prompt_model(sha, provider, models[provider], prompt['name'], version):
                    continue

                # Generate the code review
                code_review = generate_code_review(commit_info, provider, models[provider], prompt, version)

                # Save the code review
                save_code_review(code_review, sha, provider, models[provider], prompt['name'], version)

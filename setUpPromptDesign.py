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
    
    # Iterate over the models
    for provider, model in models.items():
        llm = create_llm(provider, model)

        for sha in shas:
            # Get the commit info
            commit_info = util.get_commit_info(sha)

            # Generate the code review for all prompts
            for prompt in prompts:
                # Check if the result already exists
                if generated_prompt_model(sha, provider, model, prompt['name'], version):
                    continue
                
                # If the prompt is self-reflection, get the code review from the zero-shot prompt
                if prompt['name'] == 'self-reflection':
                    prompt['code_review'] = get_code_review(sha, provider, model, 'zero-shot', version)
                
                # Generate the code review
                code_review = llm.generate(commit_info, prompt)

                # Save the code review
                save_code_review(code_review, sha, provider, model, prompt['name'], version)
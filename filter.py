import os
import re

def contains_keyword(message: str, security_keywords: list) -> tuple[bool, list[str]]:
    '''
    Check if the commit message contains a security keyword

    Parameters:

    :param message: The commit message
    :param security_keywords: The list of security keywords

    Returns:

    :return: A tuple with a boolean indicating if the message contains a keyword
             and a list with the keywords found in the message
    '''
    keywords = []
    for keyword in security_keywords:
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', message.lower()):
            keywords.append(keyword)
    return len(keywords) > 0, keywords

def get_security_keywords(file_path: str) -> list[str]:
    '''
    Load security keywords from a file

    :param file_path: The path to the keywords file

    :return: A list of security keywords
    '''
    keywords = []
    with open(file_path, 'r') as f:
        for line in f:
            keywords.append(line.strip())
    return keywords

def get_all_security_keywords_files(path: str = './') -> list[str]:
    '''
    Get all security keywords files in the current directory

    :return: A list of security keywords files
    '''
    files = os.listdir(path)
    return [f for f in files if f.startswith('security_keywords_') and f.endswith('.txt')]

def get_sample_number(amount: int, confidence: int = 95, margin_of_error: float = 0.05) -> int:
    '''
    Calculate the sample size needed for a given amount of data using finite population correction.

    :param amount: The total amount of data (population size)
    :param confidence: The confidence level (default is 95)
    :param margin_of_error: The margin of error (default is 0.05)

    :return: The sample size needed
    '''
    z_score = {90: 1.645, 95: 1.96, 99: 2.576}.get(confidence, 1.96)
    p = 0.5  # Maximum variability
    # Initial sample size for infinite population
    n_0 = (z_score ** 2) * p * (1 - p) / (margin_of_error ** 2)
    # Adjust for finite population
    n = n_0 / (1 + ((n_0 - 1) / amount))
    return max(1, int(round(n)))

if __name__ == "__main__":
    print(get_sample_number(1000))
    print(get_sample_number(22))
    print(get_sample_number(10000))
    print(get_sample_number(100000000))
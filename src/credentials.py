import os
from json import load


def retrieve_credentials(target_file):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(PROJECT_ROOT,
                           '../' + target_file)) as json_file:
        file_content = load(json_file)
    key = list(file_content.keys())[0]
    value = file_content[key]
    return key, value

import os
from json import load

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def read_json(target_file,
              json_key=None):
    with open(os.path.join(PROJECT_ROOT,
                           '../' + target_file)) as json_file:
        file_content = load(json_file)
    if json_key is None:
        key = list(file_content.keys())[0]
        value = file_content[key]
        return key, value
    value = file_content[json_key]
    return value

# end of file

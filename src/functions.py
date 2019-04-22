from json import load
from api_calls import Caller
import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

API_HOST = 'api_host.json'
API_KEY = 'api_key.json'

SET_CODES = 'set_codes.json'
STD_SETS = 'standard_sets'
WILD_SETS = 'wild_sets'


def read_json(hs_format):
    """
    Reads a JSON File and converts it into a Python Dictionary
    :param hs_format: Standard Format or Wild Format (which are both keys in the JSON file)
    :return: A Python Dictionary which holds Card Set Codes
    """
    with open(os.path.join(PROJECT_ROOT,
                           '../' + SET_CODES)) as json_file:
        file_content = load(json_file)
    value = file_content[hs_format]
    return value


def retrieve_std_sets():
    """
    Retrieves all Card Sets which are available in Hearthstone's Standard Format
    :return: A dictionary which holds every Standard Card Set with its codes (custom code (key), api code (value))
    """
    return read_json(STD_SETS)


def retrieve_wild_sets():
    """
    Retrieves all Card Sets which are available in Hearthstone's Wild Format including The Hall Of Fame
    :return: A dictionary which holds every Wild Card Set with its codes (custom code (key), api code (value))
    """
    wild_sets = read_json(WILD_SETS)  # First we collect all Wild Exclusive Sets
    std_sets = retrieve_std_sets()  # Then we collect all standard sets which are playable in wild as well
    for set_code, set_api_code in std_sets.items():
        # We are adding new keys to wild_sets dictionary without checking for duplicate keys because we know that
        # standard sets have different keys from wild sets (logic flow)
        wild_sets[set_code] = set_api_code  # Adding to Wild Exclusive Sets all of the Standard Sets
    return wild_sets  # A Dictionary which holds both Wild Exclusive and Standard Sets


def collect_cards(card_codes):
    caller = Caller(API_HOST,
                    API_KEY)
    cards = {}  # Holds every card from all standard format's sets
    for set_code, set_api_code in card_codes.items():
        cards[set_code] = caller.card_set_call(set_api_code)
    return cards


def collect_std_sets():
    return collect_cards(retrieve_std_sets())


def collect_wild_sets():
    return collect_cards(retrieve_wild_sets())

# Testing Zone


if __name__ == '__main__':
    pass
# end of file

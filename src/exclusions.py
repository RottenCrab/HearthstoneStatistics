from api_calls import Caller
from json_handler import read_json
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

API_HOST = 'api_host.json'
API_KEY = 'api_key.json'

MINION_EXCLUSIONS_PATH = 'Rules/MINION_EXCLUSIONS.md'
ARENA_EXCLUSIONS_PATH = 'Rules/ARENA_EXCLUSIONS.md'

DATASET_FILTERS = 'dataset_filters.json'
ARENA_FILTERS = 'arena_filters.json'
KEYWORDS = {'taunt': 'taunt_filters',
            'rush': 'rush_filters',
            'charge': 'charge_filters'}

MINION_EXCLUSIONS = '# LIST OF EXCLUDED MINIONS \n'
INTRODUCTION = 'The following Minions are not counted as **Taunt**, **Rush** or **Charge** Minions, ' \
               'thus they are excluded from the **Taunt**, **Rush** and **Charge** Pools in order to produce correct ' \
               'statistics and probabilities for the corresponding Plots. \n'
NOTE = '***\n NOTE: Some of the Card Image URLs may not work properly due to HearthstoneAPI \n***'
ARENA_EXCLUSIONS = '# LIST OF MINIONS UNABLE TO BE DRAFTED IN ARENA FORMAT \n'
ARENA_INTRODUCTION = 'The following Minions cannot be drafted in Arena Format, thus they are excluded in order to ' \
                     'produce correct statistics and probabilities for the corresponding Plots. \n'


def writer(filepath, exclusion_title, introduction, filters, notes):
    caller_obj = Caller(API_HOST,
                        API_KEY)
    with open(os.path.join(PROJECT_ROOT,
                           '../' + filepath), 'w') as markdown:
        markdown.write(exclusion_title)
        markdown.write(introduction)
        for keyword, list_of_exclusions in filters.items():
            markdown.write('### {title} \n'.format(title=" ".join(keyword.split('_')).title()))
            for card in list_of_exclusions:
                card_details = caller_obj.single_card_call(card)[0]
                card_name, card_img = card_details['name'], card_details['img']
                markdown.write('* [{card}]({img_url}) \n'.format(card=card_name,
                                                                 img_url=card_img))
            markdown.write('\n')
        markdown.write(notes)


def report_exclusions():
    # first of all collect all dataset filters
    dataset_filters = read_json(DATASET_FILTERS,
                                json_key='all_keys')
    arena_filters = read_json(ARENA_FILTERS,
                              json_key='all_keys')
    writer(MINION_EXCLUSIONS_PATH,
           MINION_EXCLUSIONS,
           INTRODUCTION,
           dataset_filters,
           NOTE)
    writer(ARENA_EXCLUSIONS_PATH,
           ARENA_EXCLUSIONS,
           ARENA_INTRODUCTION,
           arena_filters,
           NOTE)


if __name__ == '__main__':
    report_exclusions()

# end of file

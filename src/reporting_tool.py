from string import Template
from .json_handler import read_json
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def reporting(total_card_pool_standard,
              total_card_pool_wild):
    template_dictionary = read_json('image_urls.json',
                                    json_key='all_keys')
    template_dictionary['total_card_pool_standard'] = total_card_pool_standard
    template_dictionary['total_card_pool_wild'] = total_card_pool_wild
    filein = open('../Templates/REPORT_TEMPLATE.md')
    out = open('../Reports/REPORT.md', 'w')
    src = Template(filein.read())
    result = src.safe_substitute(template_dictionary)
    out.write(result)
    filein.close()
    out.close()

# end of file

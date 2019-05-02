import os
import pandas as pd
import functions
from custom_exceptions import UnsupportedHearthstoneFormat, UnknownKeyword
from json_handler import read_json
from math import isnan
from pprint import pprint
# TODO Create a function for .md Files (Write a Report)
# TODO Remove "Test Zones" from every file in the package

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


class CardPool:
    # Valid Hearthstone Formats
    valid_formats = [
        'standard_format',
        'wild_format',
    ]
    mana_costs = list(range(0, 13))
    STD_FORMAT = 'standard_format'
    WILD_FORMAT = 'wild_format'
    # DataFrame's Column selection filters
    COLUMN_FILTERS = ['cost',  # card's mana cost
                      'name',  # card's name
                      'cardSet',  # Hearthstone set that a card belongs to
                      'rarity',  # rarity of the card (basic, common, rare, epic, legendary)
                      'playerClass',  # Class that this card belongs to
                      'type',  # Type of the card (minion, spell, weapon etc)
                      'race',  # card's race (beast, demon etc)
                      'attack',  # card's attack (if type is minion)
                      'health',  # card's health (if type is minion)
                      'text',  # card's text
                      'img'  # card's image link
                      ]
    # keyword filters project file
    KEYWORD_FILTERS = 'dataset_filters.json'
    # JSON key for taunt minion filters
    TAUNT_FILTERS = 'taunt_filters'
    # JSON key for rush minion filters
    RUSH_FILTERS = 'rush_filters'
    # JSON key for charge minion filters
    CHARGE_FILTERS = 'charge_filters'
    # Charge Exception
    CHARGE_EXC = 'Charrrrrge'
    # Sorting Rule
    SORTING_RULE = ['cost']
    nan_replacements = {'attack': 0,
                        'text': ' '
                        }

    def __init__(self, hs_format):
        if hs_format.lower() not in CardPool.valid_formats:
            raise UnsupportedHearthstoneFormat('Invalid Hearthstone Format')
        self.hs_format = hs_format
        self.card_pool = self.__build_dataframe()

    def __is_std_format(self):
        if self.hs_format == CardPool.STD_FORMAT:
            return True
        return False

    def __build_dataframe(self):
        cards_df = pd.DataFrame()
        dataset = {}
        if self.__is_std_format():
            dataset = functions.collect_std_sets()
        else:
            dataset = functions.collect_wild_sets()
        for key, value in dataset.items():
            cards_df = cards_df.append(pd.DataFrame(data=value),
                                       ignore_index=True,
                                       sort=True)
        cards_df = cards_df[CardPool.COLUMN_FILTERS]
        card_pool = cards_df[cards_df['type'] == 'Minion']
        card_pool.fillna(value=CardPool.nan_replacements, inplace=True)
        return card_pool

    def __dataframe_length(self, dataframe):
        return len(dataframe.index)

    def __card_pool_filtering(self, keyword, keyword_filter):
        filters = read_json(CardPool.KEYWORD_FILTERS, keyword_filter)
        filtered_pool = self.card_pool[self.card_pool['text'].str.contains(keyword, case=False)]
        for flt in filters:
            filtered_pool = filtered_pool[~filtered_pool.name.str.contains(flt, case=False)]
        return filtered_pool

    def __pool_selection(self, keyword):
        if keyword.lower() == 'taunt':
            return self.taunt_pool
        elif keyword.lower() == 'rush':
            return self.rush_pool
        elif keyword.lower() == 'charge':
            return self.charge_pool
        else:
            raise UnknownKeyword('Keyword ' + keyword + ' is not supported.')

    def __count_total_minions(self, keyword):
        filtered_pool = self.__pool_selection(keyword)
        minions = {}
        for mana_cost in CardPool.mana_costs:
            minions[mana_cost] = len(filtered_pool[filtered_pool['cost'] == mana_cost])
        return minions

    @property
    def total_card_pool(self):
        return self.__dataframe_length(self.card_pool)

    @property
    def total_taunts(self):
        return self.__dataframe_length(self.taunt_pool)

    @property
    def total_rush(self):
        return self.__dataframe_length(self.rush_pool)

    @property
    def total_charge(self):
        return self.__dataframe_length(self.charge_pool)

    @property
    def total_minion_per_mana_cost(self):
        minions = {}
        for mana_cost in CardPool.mana_costs:
            minions[mana_cost] = len(self.card_pool[self.card_pool['cost'] == mana_cost].index)
        return minions

    @property
    def total_taunt_per_mana_cost(self):
        return self.__count_total_minions('taunt')

    @property
    def total_rush_per_mana_cost(self):
        return self.__count_total_minions('rush')

    @property
    def total_charge_per_mana_cost(self):
        return self.__count_total_minions('charge')

    @property
    def taunt_pool(self):
        return self.__card_pool_filtering('taunt', CardPool.TAUNT_FILTERS).sort_values(by=CardPool.SORTING_RULE)

    @property
    def rush_pool(self):
        return self.__card_pool_filtering('rush', CardPool.RUSH_FILTERS).sort_values(by=CardPool.SORTING_RULE)

    @property
    def charge_pool(self):
        return self.__card_pool_filtering('charge|Charrrrrge',
                                          CardPool.CHARGE_FILTERS).sort_values(by=CardPool.SORTING_RULE)

    def probability(self, keyword):
        filtered_pool = self.__pool_selection(keyword)
        card_probabilities = {}
        for mana_cost in CardPool.mana_costs:
            probability = 0
            minions = len(self.card_pool[self.card_pool['cost'] == mana_cost].index)
            keyword_minions = len(filtered_pool[filtered_pool['cost'] == mana_cost])
            try:
                probability = round(keyword_minions / minions, 2)
            except ZeroDivisionError:
                probability = 0
            finally:
                card_probabilities[mana_cost] = probability
        return card_probabilities

    def avg_stats(self):
        avg_stats = {}
        for mana_cost in CardPool.mana_costs:
            avg_attack = self.card_pool[self.card_pool['cost'] == mana_cost]['attack'].mean()
            avg_health = self.card_pool[self.card_pool['cost'] == mana_cost]['health'].mean()
            if isnan(avg_attack):
                avg_attack = 0
            if isnan(avg_health):
                avg_health = 0
            avg_stats[mana_cost] = {'avg_attack': round(avg_attack, 2),
                                    'avg_health': round(avg_health, 2)}
        return avg_stats

    def highest_attack(self):
        pass

    def highest_health(self):
        pass

    def generate_xlsx_file(self, keyword):
        pool = self.__pool_selection(keyword)
        filename = '{0}_{1}.xlsx'.format(keyword,
                                         self.hs_format)
        pool.to_excel('../Spreadsheets/' + filename, index=False)

    def report(self):
        pass


# TESTING ZONE


if __name__ == '__main__':
    cards = CardPool('standard_format')
    print('Total Minions per Mana Cost: ')
    pprint(cards.total_minion_per_mana_cost)
    print('*' * 50)
    print('Total Taunts per Mana Cost:')
    pprint(cards.total_taunt_per_mana_cost)
    print('*' * 50)
    print('Total Rush per Mana Cost:')
    pprint(cards.total_rush_per_mana_cost)
    print('*' * 50)
    print('Total charge per Mana Cost:')
    pprint(cards.total_charge_per_mana_cost)
    print('*' * 50)


# end of file

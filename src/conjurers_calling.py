import os
import pandas as pd
from json import load
from pprint import pprint
from math import isnan
import functions

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
FILTERS = 'dataset_filters.json'


class ConjCalling:
    KEYWORD_FILTERS = 'dataset_filters.json'
    TAUNT_FILTERS = 'taunt_filters'
    RUSH_FILTERS = 'rush_filters'
    CHARGE_FILTERS = 'charge_filters'
    nan_replacements = {'attack': 0,
                        'text': ' '
                        }
    COLUMN_FILTERS = ['cost',
                      'name',
                      'cardSet',
                      'rarity',
                      'playerClass',
                      'type',
                      'attack',
                      'health',
                      'text',
                      'img']

    def __init__(self, hs_format):
        self.hs_format = hs_format
        self.card_pool = self.__build_dataframe()

    def _import_filters(self, keyword_filter):
        with open(os.path.join(PROJECT_ROOT,
                               '../' + FILTERS)) as json_file:
            file_content = load(json_file)
        value = file_content[keyword_filter]
        return value

    def __build_dataframe(self):
        cards_df = pd.DataFrame()
        dataset = {}
        if self.hs_format == 'Standard':
            dataset = functions.collect_std_sets()
        elif self.hs_format == 'Wild':
            dataset = functions.collect_wild_sets()
        else:
            print('Supported Formats: {0}/{1}'.format('Standard', 'Wild'))
        for key, value in dataset.items():
            cards_df = cards_df.append(pd.DataFrame(data=value),
                                       ignore_index=True,
                                       sort=True)
        cards_df = cards_df[ConjCalling.COLUMN_FILTERS]
        conj_calling_pool = cards_df[cards_df['type'] == 'Minion']
        conj_calling_pool.fillna(value=ConjCalling.nan_replacements, inplace=True)
        return conj_calling_pool

    def _taunt_pool(self):
        # Duplicate to _rush_pool & _charge_pool functions (need refactoring)
        taunt_filters = self._import_filters(ConjCalling.TAUNT_FILTERS)
        taunt_pool = self.card_pool[self.card_pool['text'].str.contains('taunt', case=False)]
        for flt in taunt_filters:
            taunt_pool = taunt_pool[~taunt_pool.name.str.contains(flt, case=False)]
        return taunt_pool

    def avg_stats(self):
        avg_stats = {}
        for mana_cost in range(0, 13):
            avg_attack = self.card_pool[self.card_pool['cost'] == mana_cost]['attack'].mean()
            avg_health = self.card_pool[self.card_pool['cost'] == mana_cost]['health'].mean()
            if isnan(avg_attack):
                avg_attack = 0
            if isnan(avg_health):
                avg_health = 0
            avg_stats[mana_cost] = {'avg_attack': round(avg_attack, 2),
                                    'avg_health': round(avg_health, 2)}
        return avg_stats

    def highest_attack_minion(self):
        pass

    def highest_health_minion(self):
        pass

    def total_taunts(self):
        return len(self._taunt_pool().index)

    def total_rush(self):
        return len(self._rush_pool().index)

    def total_charge(self):
        return len(self._charge_pool().index)

    def taunt_probability(self):
        # Duplicate to rush_probability & charge_probability (needs refactoring)
        taunt_pool = self._taunt_pool()
        taunt_probabilities = {}
        for mana_cost in range(0, 13):
            probability = 0
            minions = len(self.card_pool[self.card_pool['cost'] == mana_cost].index)
            taunt_minions = len(taunt_pool[taunt_pool['cost'] == mana_cost])
            try:
                probability = round(taunt_minions / minions, 2)
            except ZeroDivisionError:
                probability = 0
            finally:
                taunt_probabilities[mana_cost] = probability
        return taunt_probabilities

    def _rush_pool(self):
        # Duplicate to _taunt_pool & _charge_pool (needs refactoring)
        rush_filters = self._import_filters(ConjCalling.RUSH_FILTERS)
        rush_pool = self.card_pool[self.card_pool['text'].str.contains('rush', case=False)]
        for flt in rush_filters:
            rush_pool = rush_pool[~rush_pool.name.str.contains(flt, case=False)]
        return rush_pool

    def rush_probability(self):
        # Duplicate to taunt_probability & charge_probability (needs refactoring)
        rush_pool = self._rush_pool()
        rush_probabilities = {}
        for mana_cost in range(0, 13):
            probability = 0
            minions = len(self.card_pool[self.card_pool['cost'] == mana_cost].index)
            rush_minions = len(rush_pool[rush_pool['cost'] == mana_cost])
            try:
                probability = round(rush_minions / minions, 2)
            except ZeroDivisionError:
                probability = 0
            finally:
                rush_probabilities[mana_cost] = probability
        return rush_probabilities

    def _charge_pool(self):
        # Duplicate to _taunt_pool & _rush_pool (needs refactoring)
        charge_filters = self._import_filters(ConjCalling.CHARGE_FILTERS)
        charge_pool = self.card_pool[self.card_pool['text'].str.contains('charge', case=False)]
        for flt in charge_filters:
            charge_pool = charge_pool[~charge_pool.name.str.contains(flt, case=False)]
        return charge_pool

    def charge_probability(self):
        # Duplicate to taunt_probability & rush_probability (needs refactoring)
        charge_pool = self._charge_pool()
        charge_probabilities = {}
        for mana_cost in range(0, 13):
            probability = 0
            minions = len(self.card_pool[self.card_pool['cost'] == mana_cost].index)
            charge_minions = len(charge_pool[charge_pool['cost'] == mana_cost])
            try:
                probability = round(charge_minions / minions, 2)
            except ZeroDivisionError:
                probability = 0
            finally:
                charge_probabilities[mana_cost] = probability
        return charge_probabilities


if __name__ == '__main__':
    obj = ConjCalling('Standard')
    pprint(obj.rush_probability())
    pprint(obj.charge_probability())
    print('Total Rush: ' + str(obj.total_rush()))
    print('Total Charge: ' + str(obj.total_charge()))

# end of file

from requests import get
from json_handler import read_json


# API Calls to HearthstoneAPI


class Caller:
    def __init__(self, api_host, api_key):
        self.host_key, self.host_value = read_json(target_file=api_host)
        self.api_key, self.api_key_value = read_json(target_file=api_key)
        self.headers = {self.host_key: self.host_value,
                        self.api_key: self.api_key_value}

    def info_call(self):
        response = get("https://omgvamp-hearthstone-v1.p.rapidapi.com/info",
                       headers=self.headers
                       )
        response_data = response.json()
        return response_data

    def card_set_call(self, hearthstone_set,
                      collectibles_only=True):
        ENDPOINT = 'https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/sets/'
        COLLECTIBLES = '?collectible='
        if collectibles_only:
            col_code = '1'
        else:
            col_code = '0'
        response = get(ENDPOINT + hearthstone_set + COLLECTIBLES + col_code,
                       headers=self.headers)
        response_data = response.json()
        return response_data

    def single_card_call(self, hearthstone_card,
                         collectibles_only=True):
        ENDPOINT = 'https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/'
        COLLECTIBLES = '?collectible='
        if collectibles_only:
            col_code = '1'
        else:
            col_code = '0'
        response = get(ENDPOINT + hearthstone_card + COLLECTIBLES + col_code,
                       headers=self.headers)
        response_data = response.json()
        return response_data


# end of file

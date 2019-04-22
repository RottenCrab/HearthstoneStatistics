from requests import get
from credentials import retrieve_credentials


# API Calls to HearthstoneAPI


class Caller:
    def __init__(self, api_host, api_key):
        self.host_key, self.host_value = retrieve_credentials(api_host)
        self.api_key, self.api_key_value = retrieve_credentials(api_key)
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

# end of file

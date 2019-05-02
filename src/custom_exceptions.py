class UnsupportedHearthstoneFormat(Exception):
    def __init__(self, message):
        self.message = message


class UnknownKeyword(Exception):
    def __init__(self, message):
        self.message = message

# end of file

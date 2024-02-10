"""Custom Exception fo inappropriate content in event detection"""


class InappropriateEventException(Exception):
    """ Inappropriate content value (of correct type)"""
    def __init__(self):
        self.error_code = 420
        self.message = "Inappropriate content"
        super().__init__(self.message)

class InappropriateEventException(Exception):
    def __init__(self):
        self.error_code = 420
        self.message = "Inappropriate content"
        super().__init__(self.message)

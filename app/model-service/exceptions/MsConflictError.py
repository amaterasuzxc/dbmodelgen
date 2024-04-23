
class MsConflictError(Exception):
    def __init__(self, name: str = None, message: str = None):
        self.name = name
        self.message = message
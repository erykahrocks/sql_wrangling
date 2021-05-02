class RequiredTableMissingError(Exception):
    """Raised when person or visit occurrence is missed from Note"""
    pass


class DBInsertionError(Exception):
    """DB insertion failed with some fatal issues"""
    pass

class NoteInvalidError(Exception):
    """Parsed note didn't pass validation"""
    def __init__(self, message='Parsed note didn\'t pass validation'):
        self.message = message
        super().__init__(self.message)

class RequiredInfoMissingError(Exception):
    """Raised when required attribute is missed from Note"""

    # provide with missing info in msg
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    pass

class RequiredInfoMissingError(Exception):
    """Raised when person or visit occurrence is missed from Note"""
    pass

class DBInsertionError(Exception):
    """DB insertion failed with some fatal issues"""
    pass

class NoteInvalidError(Exception):
    """Parsed note didn't pass validation"""
    pass
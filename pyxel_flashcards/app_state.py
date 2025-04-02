from enum import Enum, auto

class AppState(Enum):
    """Enumeration of all possible application states."""
    MAIN_MENU = auto()
    VIEW_SETS = auto()
    CREATE_SET = auto()
    VIEW_CARDS = auto()
    PRACTICE_CARDS = auto()
    EDIT_CARD = auto()
    ADD_CARD = auto()
    IMPORT_CARDS = auto()
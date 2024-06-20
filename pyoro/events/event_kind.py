import enum


class EventKind(enum.Enum):
    UNKNOWN = 0
    TICK = 1
    ASSETS_LOADED = 2
    USER_BACK = 3
    USER_DIRECTION = 4
    USER_ACTION = 5
    GUI_BUTTON_CLICK = 6

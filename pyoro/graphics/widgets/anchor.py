import enum


class AnchorX(enum.Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class AnchorY(enum.Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"
    BASELINE = "baseline"


def calculate_x(anchor: AnchorX, x: int, width: int) -> int:
    if anchor == AnchorX.LEFT:
        return x
    elif anchor == AnchorX.CENTER:
        return x - width // 2
    elif anchor == AnchorX.RIGHT:
        return x - width


def calculate_y(anchor: AnchorY, y: int, height: int) -> int:
    if anchor == AnchorY.TOP:
        return y
    elif anchor == AnchorY.CENTER:
        return y - height // 2
    elif anchor == AnchorY.BOTTOM:
        return y - height
    elif anchor == AnchorY.BASELINE:
        return y

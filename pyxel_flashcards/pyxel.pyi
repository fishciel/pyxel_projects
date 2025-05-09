"""Type stub for pyxel library to enable autocomplete in VS Code."""
from typing import Any, Callable, List, Optional, Tuple, Union

# Constants
MOUSE_LEFT: int
MOUSE_MIDDLE: int
MOUSE_RIGHT: int
KEY_0: int
KEY_1: int
# Add more key constants as needed

# Core functions
def init(width: int, height: int, title: str = "", fps: int = 30, quit_key: int = KEY_0) -> None: ...
def run(update: Callable[[], None], draw: Callable[[], None]) -> None: ...
def quit() -> None: ...
def flip() -> None: ...
def show() -> None: ...

# Input functions
def btn(key: int) -> bool: ...
def btnp(key: int, hold: int = 0, period: int = 0) -> bool: ...
def btnr(key: int) -> bool: ...
def mouse_x() -> int: ...
def mouse_y() -> int: ...

# Graphics functions
def cls(col: int) -> None: ...
def pix(x: int, y: int, col: int) -> None: ...
def line(x1: int, y1: int, x2: int, y2: int, col: int) -> None: ...
def rect(x: int, y: int, w: int, h: int, col: int) -> None: ...
def rectb(x: int, y: int, w: int, h: int, col: int) -> None: ...
def circ(x: int, y: int, r: int, col: int) -> None: ...
def circb(x: int, y: int, r: int, col: int) -> None: ...
def text(x: int, y: int, s: str, col: int) -> None: ...
def blt(x: int, y: int, img: int, u: int, v: int, w: int, h: int, colkey: int = -1) -> None: ...

# Sound functions
def sound(snd: int) -> Any: ...
def music(msc: int) -> Any: ...
def play_pos(ch: int) -> Tuple[int, int]: ...
def play(ch: int, snd: int, loop: bool = False) -> None: ...
def playm(msc: int, loop: bool = False) -> None: ...
def stop(ch: int = -1) -> None: ...

# Image class
class Image:
    width: int
    height: int
    
    def __init__(self, width: int, height: int) -> None: ...
    def load(self, filename: str) -> None: ...
    def save(self, filename: str) -> None: ...
    def set(self, x: int, y: int, data: List[str]) -> None: ...
    def load(self, x: int, y: int, filename: str) -> None: ...

# Other functions as needed
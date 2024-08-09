from talon import actions, ctrl, ui
from talon.skia import Path
from talon.types import Point2d
from dataclasses import dataclass

@dataclass
class Option:
    label: str
    function: callable
    size: float = 1.0
    focused: bool = False
    bg_color: str = None
    line_color: str = None
    text_color: str = None
    path: Path = None
    center: Point2d = None
    on_hover: bool = False
    hover_delay: float = 0.005
    on_dwell: bool = False
    dwell_delay: float = 0.35


# ------ Functions for use with Option.function ------ #
# *functions called by Options are currently implemented in the menumanager class!


# def shout(text: str):
#         def shout():
#             print(f"shouting {text}!")
#         return shout
    
# def scroll(x: int = 0, y: int = 0):
#     def scroll():
#         actions.mouse_scroll(y=y, x=x)
#     return scroll

# def insert(text: str):
#     def insert():
#         actions.insert(text)
#     return insert

# def key(key: str):
#     def keypress():
#         actions.key(key=key)
#     return keypress

# Dont use this, need to implement held keys at option level
# def f_key_press_hold(key: str):
#     def keypress():
#         ctrl.key_press(key=key, down=True)
#     return keypress

# def printAppName(self):
#     def printAppName():
#         print(ui.active_app().name)
#     return printAppName

# def macro(*functions):
#     def macro():
#         for function in functions:
#             function()
#     return macro
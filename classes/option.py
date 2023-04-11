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
    on_dwell: bool = False
    dwell_time: float = 0.3
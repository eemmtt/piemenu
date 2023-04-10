# Modified from timo's mouse_grid.py
# courtesy of https://github.com/timo/
#   see https://github.com/timo/talon_scripts
# script has only been tested on Windows 10 on a single monitor
from talon import canvas, ui, ctrl, actions
from talon.skia import Rect, Path, Surface, Paint
from talon.types import Point2d as Point2d
import math, time
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
    dwell_time: float = 0.5
    
class SettingsAndFunctions:
    def __init__(self):
        #Defualt Pie Menu display settings and options, overridden by child classes
        self.bg_color = "3f3fffbb"
        self.line_color = "ffffffff"
        self.text_color = "ffffffff"
        self.menu_radius = 160
        self.deadzone_radius = 30
        self.text_placement_radius = 100
        
        self.options = [
                Option(label = "Print App Name", 
                       function = self.f_printAppName()), 
                Option(label = "Scroll Up",
                       function = self.f_scroll(distance=-30),
                       bg_color="ff3f3fbb",
                       on_hover=True), 
                Option(label = "Inserts",
                       function = self.f_shout("Inserts")), 
                Option(label = "Active Windows",
                       function = self.f_key("win-tab")), 
                Option(label = "Scroll Down",
                       function = self.f_scroll(distance=30),
                       bg_color="1f1fffbb",
                       on_hover=True), 
                Option(label = "Last Window",
                       function = self.f_key("alt-tab"),
                       on_dwell=True),
            ]
    
    #base functions and function factories for the options
    def f_shout(self, text: str):
        def shout():
            print(f"shouting {text}!")
        return shout
    
    def f_scroll(self, distance: int, steps: int = 1, delay: float = 0.02):
        def scroll():
            if steps > 1:
                stepped_dist = distance//steps
                for i in range(steps):
                    actions.mouse_scroll(y=stepped_dist)
                    time.sleep(delay)
            else:
                actions.mouse_scroll(y=distance)
        return scroll
    
    def f_insert(self, text: str):
        def insert():
            actions.insert(text)
        return insert
    
    def f_key(self, key: str):
        def keypress():
            actions.key(key)
        return keypress
    
    def f_printAppName(self):
        def printAppName():
            print(ui.active_app().name)
        return printAppName
    


class FireFox_Nav(SettingsAndFunctions):
    def __init__(self):
        super().__init__()
        self.bg_color = "ff9922bb"
        
        self.options = [
                Option(label = "New Tab", 
                       function = actions.app.tab_open),
                Option(label = "Scroll Up",
                       function = self.f_scroll(distance=-30),
                       bg_color="ff3f3fbb",
                       on_hover=True),
                Option(label = "Back", 
                       function = actions.browser.go_back),
                Option(label = "Active Windows", 
                       function = self.f_key("win-tab")),
                Option(label = "Scroll Down",
                       function = self.f_scroll(distance=30),
                       bg_color="1f1fffbb",
                       on_hover=True),
                Option(label = "Last Window", 
                       function = self.f_key("alt-tab")),
                ]
        
class Slack_Nav(SettingsAndFunctions):
    def __init__(self):
        super().__init__()
        self.bg_color = "999966bb"
        
        self.options = [
                Option(label = "Search", 
                       function = self.f_key("ctrl-k")),
                Option(label = "Scroll Up",
                       function = self.f_scroll(distance=-10),
                       bg_color="ff3f3fbb",
                       on_hover=True),
                Option(label = "Go Back", 
                       function = self.f_key("alt-left")),
                Option(label = "Active Windows", 
                       function = self.f_key("win-tab")),
                Option(label = "Scroll Down",
                       function = self.f_scroll(distance=10),
                       bg_color="1f1fffbb",
                       on_hover=True), 
                Option(label = "Last Window", 
                       function = self.f_key("alt-tab")),
                ]
        
class Outlook_Nav(SettingsAndFunctions):
    def __init__(self):
        super().__init__()
        self.bg_color = "886666bb"
        
        self.options = [
                Option(label = "Calendar", function = self.f_key("ctrl-2")),
                Option(label = "Scroll Up",
                       function = self.f_scroll(distance=-30),
                       bg_color="ff3f3fbb",
                       on_hover=True), 
                Option(label = "Inbox", function = self.f_key("ctrl-1")),
                Option(label = "Active Windows", function = self.f_key("win-tab")),
                Option(label = "Scroll Down",
                       function = self.f_scroll(distance=30),
                       bg_color="1f1fffbb",
                       on_hover=True),
                Option(label = "Last Window", function = self.f_key("alt-tab")),
                ]
class Inserts(SettingsAndFunctions):
    def __init__(self):
        super().__init__()
        self.bg_color = "3f3f3fbb"
        
        self.options = [
                Option(label = "Hello", function = self.f_insert("Hello")),
                Option(label = "Goodbye", function = self.f_insert("Goodbye")),
                Option(label = "Thanks", function = self.f_insert("Thanks")),
                Option(label = "Sorry", function = self.f_insert("Sorry")),
                Option(label = "Please", function = self.f_insert("Please")),
                Option(label = "Thank You", function = self.f_insert("Thank You")),
                ]
    
# The main class for the Pie Menu
# Draws the menu, handles option selection and the resulting function call
class PieMenu:
    def __init__(self):
        self.mcanvas = None
        self.active = False
        self.center = None
        self.variations = None
        
    def setup(self, *, rect: Rect = None, screen_num: int = None, layer: int = 0, app: str = None):
        if self.mcanvas:
            self.mcanvas.close()
            
        mos_x, mos_y = ctrl.mouse_pos()
        self.center = Point2d(mos_x, mos_y)
        self.mcanvas = canvas.Canvas(x=mos_x-300, y=mos_y-300, width=600, height=600)
        
        if self.active:
            self.mcanvas.register("draw", self.draw)
            self.mcanvas.freeze()
        
        #call setup by app, layer. Otherwise, call setup by active app, layer
        if app:
            self.variations = piemenu_variations[app][layer]
            return
        
        if ui.active_app().name in piemenu_variations:
            self.variations = piemenu_variations[ui.active_app().name][layer]
        else:
            self.variations = piemenu_variations["_default"][layer]
        return
        
    def show(self):
        if not self.active:
            self.mcanvas.register("draw", self.draw)
            #self.mcanvas.freeze()
            self.active = True
        else:
            self.mcanvas.show()
        return

    def close(self):
        if self.active:
            self.mcanvas.unregister("draw", self.draw)
            self.mcanvas.close()
            self.mcanvas = None
            self.active = False
        return

    def draw(self, canvas):
        def draw_wedges(self, center: Point2d):
            explode_offset = 15
            radius = self.variations.menu_radius
            dead_radius = self.variations.deadzone_radius
            text_radius = self.variations.text_placement_radius
            text_color = self.variations.text_color
            
            num_options = len(self.variations.options)
            center = self.center
            
            rect_out = Rect( center.x - radius, center.y - radius, radius*2, radius*2)
            rect_in = Rect( center.x - dead_radius, center.y - dead_radius, dead_radius*2, dead_radius*2)
            start_angle = 0
            sweep_angle = -360.0 / num_options
            
            def draw_path(start_angle, sweep_angle, rect_in, rect_out) -> Path:
                # Draw Path
                path = Path()
                start_location = Point2d(center.x + dead_radius*math.cos(math.radians(start_angle)), 
                                        center.y + dead_radius*math.sin(math.radians(start_angle)))
                path.move_to(start_location.x, start_location.y)
                path.arc_to_with_oval(oval=rect_out, start_angle=start_angle, sweep_angle=sweep_angle, force_move_to=False)
                path.arc_to_with_oval(oval=rect_in, start_angle=start_angle+sweep_angle, sweep_angle=-sweep_angle, force_move_to=False)
                path.close()
                return path
            
            for option in self.variations.options:
            
                fill_paint = canvas.paint
                outline_paint = fill_paint.clone()
                text_paint = Paint()
                    
                # Configure the fill paint
                fill_paint.style = fill_paint.Style.FILL
                fill_paint.color = option.bg_color if option.bg_color else self.variations.bg_color

                # Configure the outline paint
                outline_paint.style = outline_paint.Style.STROKE
                outline_paint.stroke_width = 1
                outline_paint.color = option.line_color if option.line_color else self.variations.line_color

                # Configure text
                text_angle = math.radians(start_angle + sweep_angle / 2)
                text_paint.color = option.text_color if option.text_color else text_color
                text_paint.text_align = canvas.paint.TextAlign.CENTER
                text_location = Point2d(center.x + text_radius*math.cos(text_angle), 
                                        center.y + text_radius*math.sin(text_angle))
                
                # Calculate "explode" transform for hover anim TBD
                if option.focused and explode_offset > 0:
                    angle = start_angle + sweep_angle / 2 
                    x = explode_offset * math.cos(math.radians(angle))
                    y = explode_offset * math.sin(math.radians(angle))
                    
                    canvas.save()
                    canvas.translate(x, y)
                else:
                    canvas.save()
                    #canvas.translate(10, 10)
                
                path = draw_path(start_angle=start_angle, 
                            sweep_angle=sweep_angle, 
                            rect_in=rect_in, 
                            rect_out=rect_out)
                
                # Draw Fill, Stroke, Text
                canvas.draw_path(path, fill_paint)
                canvas.draw_path(path, outline_paint)
                canvas.draw_text(option.label, text_location.x, text_location.y, text_paint)
                
                canvas.restore()
                start_angle += sweep_angle
            

        draw_wedges(self, self.center)
   
    def get_option(self) -> Option:
        """Read mouse position and return the option that the mouse is over."""
        mos_x, mos_y = ctrl.mouse_pos()
        mouse = Point2d(mos_x, mos_y)
        center = self.center
        options = self.variations.options
        deadzone_radius = self.variations.deadzone_radius
        
        #check if mouse is in deadzone
        distance_squared = (mouse.x-center.x)**2 + (mouse.y-center.y)**2
        if distance_squared < deadzone_radius**2:
            return Option(label="_none", function= lambda *args, **kwargs: None)
        
        #map angle to option
        angle = math.atan2(float(mouse.y-center.y), float(mouse.x-center.x))
        num_options = len(options) 
        return options[math.ceil((-angle*num_options)/(math.pi*2)) - 1]
        
piemenu_variations = {
    "_default": [SettingsAndFunctions(), Inserts()],
    "Firefox": [FireFox_Nav()],
    "Slack": [Slack_Nav()],
    "Microsoft Outlook": [Outlook_Nav()],
}
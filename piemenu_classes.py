# Modified from timo's mouse_grid.py
# courtesy of https://github.com/timo/
#   see https://github.com/timo/talon_scripts
# script has only been tested on Windows 10 on a single monitor
from talon import canvas, ui, ctrl, actions
from talon.skia import Rect
import math


class SettingsAndFunctions:
    def __init__(self):
        #Defualt Pie Menu settings and options, overridden by child classes
        self.bg_color = "3f3fffbb"
        self.deadzone_color = "999999aa"
        self.line_color = "ffffffff"
        self.text_color = "ffffffff"
        self.menu_radius = 160
        self.deadzone_radius = 30
        self.text_placement_radius = 100
        
        self.options = [
                ("The Option ZERO",     self.f_shout("zero")), 
                ("Scroll Up",           self.f_scroll(-400)), 
                ("two",                 self.f_shout("two")), 
                ("three",               self.f_shout("three")), 
                ("Scroll Down",         self.f_scroll(400)), 
                ("five",                self.f_shout("five")),
            ]
    
    #base functions and function factories for the options
    def f_shout(self, text: str):
        def shout():
            print(f"shouting {text}!")
        return shout
    
    def f_scroll(self, num: int):
        def scroll():
            actions.mouse_scroll(y=num)
        return scroll
    
    def f_insert(self, text: str):
        def insert():
            actions.insert(text)
        return insert
    
    def f_key(self, key: str):
        def keypress():
            actions.key(key)
        return keypress

class FireFox_0(SettingsAndFunctions):
    def __init__(self):
        super().__init__()
        self.bg_color = "ff9922bb"
        
        self.options = [
                ("New Tab",             self.f_shout("def")),
                ("Scroll Up",           self.f_scroll(-400)),
                ("Close Tab",           self.f_shout("def")),
                ("Back",                self.f_shout("def")),
                ("Scroll Down",         self.f_scroll(400)),
                ("Focus Search Bar",    self.f_shout("def")),
                ]

class FireFox_1(SettingsAndFunctions):
    def __init__(self):
        super().__init__()
        self.bg_color = "00ffffbb"
        
        self.options = [
                ("New Tab",             self.f_shout("def")),
                ("Close Tab",           self.f_shout("def")),
                ("Back",                self.f_shout("def")),
                ("Focus Search Bar",    self.f_shout("def")),
                ]

# The main class for the Pie Menu
# Draws the menu, handles option selection and the resulting function call
class PieMenu:
    def __init__(self):
        self.screen = None
        self.rect = None
        self.mcanvas = None
        self.active = False
        self.center = None
        self.variations = None

    def setup(self, *, rect: Rect = None, screen_num: int = None, layer: int = 0):
        screens = ui.screens()
        mos_x, mos_y = ctrl.mouse_pos()
        # each if block here might set the rect to None to indicate failure
        if rect is not None:
            try:
                screen = ui.screen_containing(*rect.center)
            except Exception:
                rect = None
        if rect is None and screen_num is not None:
            screen = screens[screen_num % len(screens)]
            rect = screen.rect
        if rect is None:
            screen = screens[0]
            rect = screen.rect
        self.screen = screen
        self.rect = rect.copy()
        if self.mcanvas is not None:
            self.mcanvas.close()
        self.mcanvas = canvas.Canvas.from_screen(screen)
        if self.active:
            self.mcanvas.register("draw", self.draw)
            self.mcanvas.freeze()
        self.center = (mos_x, mos_y)
        self.variations = piemenu_variations[ui.active_app().name][layer] if ui.active_app().name in piemenu_variations else piemenu_variations["_default"][layer]
        return
        
    def show(self):
        if self.active:
            return
        self.mcanvas.register("draw", self.draw)
        self.mcanvas.freeze()
        self.active = True
        return

    def close(self):
        if not self.active:
            return
        self.mcanvas.unregister("draw", self.draw)
        self.mcanvas.close()
        self.mcanvas = None
        self.active = False
        return

    def draw(self, canvas):
        paint = canvas.paint
        
        def draw_piemenu(c_x, c_y):
            """ Draws the pie menu at the given coordinates """
            #read attributes from the variations class
            rad = self.variations.menu_radius
            dead_rad = self.variations.deadzone_radius
            t_rad = self.variations.text_placement_radius
            options = self.variations.options
            num_options = len(options)
            bg_color = self.variations.bg_color
            deadzone_color = self.variations.deadzone_color
            line_color = self.variations.line_color
            text_color = self.variations.text_color
            
            #draw the pie menu background
            paint.color = bg_color
            canvas.draw_circle(c_x, c_y, rad, paint)
            
            paint.color = deadzone_color
            canvas.draw_circle(c_x, c_y, dead_rad, paint)
            
            #draw the segment lines and option labels
            slice = (2*math.pi)  / num_options
            for id, o in enumerate(options):
                angle = -(slice * id)
                t_angle = angle - slice/2
                cos_angle = math.cos(angle)
                sin_angle = math.sin(angle)
                
                paint.color = line_color
                paint.stroke_width = 1
                canvas.draw_line(dead_rad*cos_angle + c_x, dead_rad*sin_angle + c_y, rad*cos_angle + c_x, rad*sin_angle + c_y)
                
                paint.color = text_color
                canvas.paint.text_align = canvas.paint.TextAlign.CENTER
                canvas.draw_text(o[0], c_x + t_rad*math.cos(t_angle), c_y + t_rad*math.sin(t_angle))

        draw_piemenu(self.center[0], self.center[1])
   
    def call_selection(self):
        """ Calls the function associated with the selected pie menu option"""
        mos_x, mos_y = ctrl.mouse_pos()
        options = self.variations.options
        dead_rad = self.variations.deadzone_radius
        num_options = len(options)
        
        #check if mouse is in the deadzone, if so return with no action
        dist_sqrd = (mos_x-self.center[0])**2 + (mos_y-self.center[1])**2
        if dist_sqrd < dead_rad**2:
            return
        
        #get angle of vector of mouse->center, counting ccw from 3 o'clock
        angle = math.atan2(float(mos_y-self.center[1]), float(mos_x-self.center[0]))
        if angle > 0:
            angle -= math.pi*2
        
        #check each slice to see which option is selected, call the associated action
        #options index of range is 0->num_options-1
        slice = (2*math.pi)  / num_options
        for i in range(num_options):
            bound = -slice*(i+1)
            if angle > bound:
                options[i][1]() #passing the index of the option to the function, likely will remove this
                return
        options[num_options][1]()
        return 
        
piemenu_variations = {
    "_default": [SettingsAndFunctions()],
    "Firefox": [FireFox_0(), FireFox_1()],
}
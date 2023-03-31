# Modified from timo's mouse_grid.py
# courtesy of https://github.com/timo/
#   see https://github.com/timo/talon_scripts
# script has only been tested on Windows 10 on a single monitor
from talon import canvas, ui, ctrl, actions
from talon.skia import Rect, Path, Surface, Paint
from talon.types import Point2d as Point2d
import math, time


class SettingsAndFunctions:
    def __init__(self):
        self.center = None #center of the pie menu, set by PieMenu.setup()
        
        #Defualt Pie Menu settings and options, overridden by child classes
        self.bg_color = "3f3fffbb"
        self.deadzone_color = "999999aa"
        self.line_color = "ffffffff"
        self.text_color = "ffffffff"
        self.menu_radius = 160
        self.deadzone_radius = 30
        self.text_placement_radius = 100
        
        self.options = [
                ("Print App Name",      self.f_printAppName()), 
                ("Scroll Up",           self.f_scroll(-800,12,0.02)), 
                ("three",               self.f_shout("three")), 
                ("Active Windows",      self.f_key("win-tab")), 
                ("Scroll Down",         self.f_scroll(800,12,0.03)), 
                ("Last Window",         self.f_key("alt-tab")),
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
                ("New Tab",             actions.app.tab_open),
                ("Scroll Up",           self.f_scroll(-1000,steps=12,delay=0.03)),
                ("Back",                actions.browser.go_back),
                ("Active Windows",      self.f_key("win-tab")),
                ("Scroll Down",         self.f_scroll(1000,steps=12,delay=0.03)),
                ("Last Window",         self.f_key("alt-tab")),
                ]
        
class Slack_Nav(SettingsAndFunctions):
    def __init__(self):
        super().__init__()
        self.bg_color = "999966bb"
        
        self.options = [
                ("Search",              self.f_key("ctrl-k")),
                ("Scroll Up",           self.f_scroll(-600,12)), 
                ("Go Back",             self.f_key("alt-left")),
                ("Active Windows",      self.f_key("win-tab")),
                ("Scroll Down",         self.f_scroll(600,12)), 
                ("Last Window",         self.f_key("alt-tab")),
                ]
        
class Outlook_Nav(SettingsAndFunctions):
    def __init__(self):
        super().__init__()
        self.bg_color = "886666bb"
        
        self.options = [
                ("Calendar",            self.f_key("ctrl-2")),
                ("Scroll Up",           self.f_scroll(-600,12)), 
                ("Inbox",               self.f_key("ctrl-1")),
                ("Active Windows",      self.f_key("win-tab")),
                ("Scroll Down",         self.f_scroll(600,12)), 
                ("Last Window",         self.f_key("alt-tab")),
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
            
        self.center = Point2d(mos_x, mos_y)
        if ui.active_app().name in piemenu_variations:
            self.variations = piemenu_variations[ui.active_app().name][layer]
        else:
            self.variations = piemenu_variations["_default"][layer]
        self.variations.center = self.center
        
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

        def draw_paths(center: Point2d):
            rad = self.variations.menu_radius
            dead_rad = self.variations.deadzone_radius
            length = 100
            points = [Point2d(center.x + dead_rad, center.y), Point2d(center.x + rad, center.y), Point2d(center.x, center.y + rad), Point2d(center.x, center.y + dead_rad)]
            colors = ["ff0000FF", "00ff00FF", "0000ffFF", "ffff00FF"]
            path = Path()
            last_point = points[0]
            path.move_to(last_point.x, last_point.y)
            canvas.paint.color = colors[1]
            path.line_to(points[1].x, points[1].y)
            path.arc_to_with_points(center.x, center.y, points[2].x, points[2].y, rad)
            path.line_to(points[3].x, points[3].y)
            path.arc_to_with_points(center.x, center.y, points[0].x, points[0].y, dead_rad)
            path.close()
            
            canvas.draw_path(path, paint)
            # path.close()
            # canvas.draw_path(path, paint)
        
        def draw_wedges(self, center: Point2d):
            explode_offset = 0
            radius = self.variations.menu_radius
            dead_radius = self.variations.deadzone_radius

            total_values = len(self.variations.options)
            #print(total_values)
            center = self.center
            
            
            rect = Rect( center.x - radius, center.y - radius, radius*2, radius*2)
            rect2 = Rect( center.x - dead_radius, center.y - dead_radius, dead_radius*2, dead_radius*2)
            
            colors = ["ff0000FF", "00ff00FF", "0000ffFF", "ffff00FF", "ff00ffff", "00ffffff", "ff0000ff"]
            start_angle = 0
            
            for i, option in enumerate(self.variations.options):
                sweep_angle = -360.0 / total_values
                
                path = Path()
                fill_paint = paint
                outline_paint = Paint()

                path.move_to(center.x, center.y)
                path.arc_to_with_oval(oval=rect, start_angle=start_angle, sweep_angle=sweep_angle, force_move_to=False)
                path.arc_to_with_oval(oval=rect2, start_angle=start_angle+sweep_angle, sweep_angle=-sweep_angle, force_move_to=False)
                path.close()

                fill_paint.style = fill_paint.Style.FILL
                fill_paint.color = colors[i]

                # outline_paint.style = outline_paint.Style.STROKE
                # outline_paint.stroke_width = 5
                # outline_paint.color = "000000ff"

                # Calculate "explode" transform
                angle = start_angle + sweep_angle / 2 
                x = explode_offset * math.cos(math.radians(angle))
                y = explode_offset * math.sin(math.radians(angle))
                canvas.save()
                canvas.translate(x, y)

                # Fill and stroke the path
                canvas.draw_path(path, fill_paint)
                #canvas.draw_path(path, outline_paint)
                canvas.restore()

                start_angle += sweep_angle

            
                
        draw_piemenu(self.center.x, self.center.y)
        #draw_paths(self.center)
        #draw_wedges(self, self.center)
   
    def call_selection(self):
        """ Calls the function associated with the selected pie menu option"""
        mos_x, mos_y = ctrl.mouse_pos()
        options = self.variations.options
        dead_rad = self.variations.deadzone_radius
        num_options = len(options)
        
        #check if mouse is in the deadzone, if so return with no action
        dist_sqrd = (mos_x-self.center.x)**2 + (mos_y-self.center.y)**2
        if dist_sqrd < dead_rad**2:
            return
        
        #get angle of vector of mouse->center, counting ccw from 3 o'clock
        angle = math.atan2(float(mos_y-self.center.y), float(mos_x-self.center.x))
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
    "Firefox": [FireFox_Nav()],
    "Slack": [Slack_Nav()],
    "Microsoft Outlook": [Outlook_Nav()],
}
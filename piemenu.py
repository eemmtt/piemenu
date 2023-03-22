# Modified from timo's mouse_grid.py
# courtesy of https://github.com/timo/
#   see https://github.com/timo/talon_scripts
# script has only been tested on Windows 10 on a single monitor
from talon import Module, Context, canvas, ui, ctrl
from talon.skia import Rect
import math

mod = Module()
mod.tag("pm_showing", desc="Tag indicates whether the Pie Menu is showing")
ctx = Context()


class PieMenu:
    def __init__(self):
        self.screen = None
        self.rect = None
        self.mcanvas = None
        self.active = False
        self.center = None
        
        #Appeareance settings, overridden by child classes
        self.bg_color = "3f3fffbb"
        self.deadzone_color = "999999aa"
        self.line_color = "ffffffff"
        self.text_color = "ffffffff"
        self.menu_radius = 160
        self.deadzone_radius = 60
        self.text_placement_radius = 100

    def setup(self, *, rect: Rect = None, screen_num: int = None):
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
            
        #Define your Pie Menu options here, each option is a tuple of (label: str, action: function)
        #Labels will be displayed on the pie menu, actions will be called when the option is selected
        option_lists = {
            "Firefox": [
                ("New Tab", self.shout),
                ("Close Tab", self.shout),
                ("Back", self.shout),
                ("Focus Search Bar", self.shout),
                ],
        }
        
        active_app = ui.active_app().name
        if active_app in option_lists:
            self.options = option_lists[active_app]
        else:
            self.options = [
                ("The Option ZERO", self.shout), 
                ("one", self.shout), 
                ("two", self.shout), 
                ("three", self.shout), 
                ("four", self.shout), 
                ("five", self.shout),
            ]
        
        
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

    def draw(self, canvas):
        paint = canvas.paint
        
        def draw_piemenu(c_x, c_y):
            rad = self.menu_radius
            dead_rad = self.deadzone_radius
            t_rad = self.text_placement_radius
            num_options = len(self.options)
            
            #draw the pie menu background
            paint.color = self.bg_color
            canvas.draw_circle(c_x, c_y, rad, paint)
            paint.color = self.deadzone_color
            canvas.draw_circle(c_x, c_y, dead_rad, paint)
            
            #draw the segment lines and option labels
            slice = (2*math.pi)  / num_options
            for id, o in enumerate(self.options):
                angle = -(slice * id)
                t_angle = angle - slice/2
                
                paint.color = self.line_color
                paint.stroke_width = 1
                canvas.draw_line(dead_rad*math.cos(angle) + c_x, dead_rad*math.sin(angle) + c_y, rad*math.cos(angle) + c_x, rad*math.sin(angle) + c_y)
                
                paint.color = self.text_color
                canvas.paint.text_align = canvas.paint.TextAlign.CENTER
                canvas.draw_text(o[0], c_x + t_rad*math.cos(t_angle), c_y + t_rad*math.sin(t_angle))

        draw_piemenu(self.center[0], self.center[1])
   
    def call_selection(self):
        """ Calls the function associated with the selected pie menu option"""
        mos_x, mos_y = ctrl.mouse_pos()
        num_options = len(self.options)
        
        #check if mouse is in the deadzone, if so return with no action
        dead_rad_squared = 60**2
        dis_squared = (mos_x-self.center[0])**2 + (mos_y-self.center[1])**2
        if dis_squared < dead_rad_squared:
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
                self.options[i][1](i)
                return
        self.options[num_options][1](num_options)
        return 

    def shout(self, num: int):
        print(f"shouting {num}")
        print(ui.active_app().name)
        
pm = PieMenu()

@mod.action_class
class PieMenuActions:
    def pimenu_activate():
        """Show pie menu"""
        if not pm.mcanvas:
            pm.setup()
        pm.show()
        ctx.tags = ["user.pm_showing"]

    def pimenu_reset():
        """Resets the menu to fill the whole screen again"""
        if pm.active:
            pm.setup()

    def pimenu_select_screen(screen: int):
        """Brings up mouse menu"""
        pm.setup(screen_num=screen - 1)
        pm.show()

    def pimenu_close():
        """Close the active menu"""
        ctx.tags = []
        pm.close()
        
    def pimenu_call_option():
        """Runs the option under the cursor"""
        pm.close()
        pm.call_selection()


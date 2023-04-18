# Modified from timo's mouse_grid.py
# courtesy of https://github.com/timo/
#   see https://github.com/timo/talon_scripts
# script has only been tested on Windows 10 on a single monitor
from talon import canvas, ui, ctrl, actions
from talon.skia import Rect, Path, Paint
from talon.types import Point2d
from .option import Option
import math


class PieMenu:
    def __init__(self,):
        self.mcanvas = None
        self.active = False
        self.center = None
        
        self.app = ""
        self.name = ""
        self.fill = True
        self.bg_color = "3f3fffbb"
        self.lines = True
        self.line_color = "ffffffff"
        self.text = True
        self.text_color = "ffffffff"
        self.menu_radius = 140
        self.deadzone_radius = 30
        self.text_placement_radius = 90
        self.rect_out: Rect = None
        self.rect_in: Rect = None
        self.explode_offset = 15
        self.start_angle_offset = 0 # degrees
        
        self.options = []
        
    def setup(self,):
        if self.mcanvas:
            self.mcanvas.close()
            
        mos_x, mos_y = ctrl.mouse_pos()
        self.center = Point2d(mos_x, mos_y)
        self.mcanvas = canvas.Canvas(x=mos_x-180, y=mos_y-180, width=360, height=360)
        
        self.rect_out = Rect( self.center.x - self.menu_radius, self.center.y - self.menu_radius, self.menu_radius*2, self.menu_radius*2)
        self.rect_in = Rect( self.center.x - self.deadzone_radius, self.center.y - self.deadzone_radius, self.deadzone_radius*2, self.deadzone_radius*2)
        
        if self.active:
            self.mcanvas.register("draw", self.draw)
            self.mcanvas.freeze()
        return
        
    def show(self):
        if not self.active:
            self.mcanvas.register("draw", self.draw)
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
            explode_offset = self.explode_offset
            dead_radius = self.deadzone_radius
            text_radius = self.text_placement_radius
            text_color = self.text_color
            
            num_options = len(self.options)
            center = self.center
            
            start_angle = self.start_angle_offset
            sweep_angle = -360.0 / num_options
            
            def draw_path(start_angle, sweep_angle, rect_in, rect_out) -> Path:
                path = Path()
                start_location = Point2d(center.x + dead_radius*math.cos(math.radians(start_angle)), 
                                        center.y + dead_radius*math.sin(math.radians(start_angle)))
                path.move_to(start_location.x, start_location.y)
                path.arc_to_with_oval(oval=rect_out, start_angle=start_angle, sweep_angle=sweep_angle, force_move_to=False)
                path.arc_to_with_oval(oval=rect_in, start_angle=start_angle+sweep_angle, sweep_angle=-sweep_angle, force_move_to=False)
                path.close()
                return path
            
            for option in self.options:
                fill_paint = canvas.paint
                outline_paint = fill_paint.clone()
                text_paint = Paint()
                    
                # Configure the fill paint
                fill_paint.style = fill_paint.Style.FILL
                fill_paint.color = option.bg_color if option.bg_color else self.bg_color

                # Configure the outline paint
                outline_paint.style = outline_paint.Style.STROKE
                outline_paint.stroke_width = 1
                outline_paint.color = option.line_color if option.line_color else self.line_color

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
                            rect_in=self.rect_in, 
                            rect_out=self.rect_out)
                
                # Draw Fill, Stroke, Text
                if self.fill: canvas.draw_path(path, fill_paint)
                if self.lines: canvas.draw_path(path, outline_paint)
                if self.text: canvas.draw_text(option.label, text_location.x, text_location.y, text_paint)
                canvas.restore()
                start_angle += sweep_angle
        
        draw_wedges(self, self.center)
   
    def get_option(self) -> Option:
        """Read mouse position and return the option that the mouse is over."""
        mos_x, mos_y = ctrl.mouse_pos()
        mouse = Point2d(mos_x, mos_y)
        center = self.center
        options = self.options
        deadzone_radius = self.deadzone_radius
        
        #check if mouse is in deadzone
        distance_squared = (mouse.x-center.x)**2 + (mouse.y-center.y)**2
        if distance_squared < deadzone_radius**2:
            return Option(label="_none", function= lambda *args, **kwargs: None)
        
        #map angle to option
        start_angle = math.radians(self.start_angle_offset)
        angle = math.atan2(float(mouse.y-center.y), float(mouse.x-center.x))
        return options[math.ceil(((start_angle-angle)*len(options))/(math.pi*2)) - 1]
    
# Modified from timo's mouse_grid.py
# courtesy of https://github.com/timo/
#   see https://github.com/timo/talon_scripts
# script has only been tested on Windows 10 on a single monitor
from talon import Module, Context
from .piemenu_classes import *


mod = Module()
mod.tag("pm_showing", desc="Tag indicates whether the Pie Menu is showing")
ctx = Context()
pm = PieMenu()

@mod.action_class
class PieMenuActions:     
    def piemenu_call_and_close():
        """Runs the selected function and closes the menu"""
        pm.close()
        pm.call_selection()
        
    def piemenu_launch(screen: int, layer: int = 0):
        """Launches Pie Menu"""
        #toggle_mode = True if toggle == 1 else False
        pm.setup(screen_num=screen - 1, layer=layer)
        if not pm.mcanvas:
            pm.setup(layer=layer)
        pm.show()
        ctx.tags = ["user.pm_showing"]
    
    def piemenu_toggle(screen: int, layer: int = 0):
        """Toggles Pie Menu"""
        if "user.pm_showing" in ctx.tags:
            pm.close()
            pm.call_selection()
            ctx.tags = []
        else:
            pm.setup(screen_num=screen - 1, layer=layer)
            if not pm.mcanvas:
                pm.setup(layer=layer)
            pm.show()
            ctx.tags = ["user.pm_showing"]


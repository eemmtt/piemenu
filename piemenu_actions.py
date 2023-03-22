# Modified from timo's mouse_grid.py
# courtesy of https://github.com/timo/
#   see https://github.com/timo/talon_scripts
# script has only been tested on Windows 10 on a single monitor
from talon import Module, Context
from .piemenu_classes import *


mod = Module()
mod.tag("pm_showing", desc="Tag indicates whether the Pie Menu is showing")
ctx = Context()
active_app = ui.active_app().name

#pm = piemenu_variations[active_app]() if active_app in piemenu_variations else PieMenu()
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


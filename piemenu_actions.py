# Modified from timo's mouse_grid.py
# courtesy of https://github.com/timo/
#   see https://github.com/timo/talon_scripts
# script has only been tested on Windows 10 on a single monitor
from talon import Module, Context, cron
from .piemenu_classes import PieMenu, Option

mod = Module()
mod.tag("pm_showing", desc="Tag indicates whether the Pie Menu is showing")
ctx = Context()
pm = PieMenu()

last_option: Option = None
pieMenu_job = None

def on_interval():
    global last_option
    o = pm.get_option()
    if o and last_option: 
        if o.label != last_option.label:
            last_option.focused = False
            last_option = o
            o.focused = True
        if o.on_hover: o.function()
    if o and not last_option:
        last_option = o
        o.focused = True
    if last_option and not o:
        last_option.focused = False
        last_option = None
    

@mod.action_class
class PieMenuActions:     
    def piemenu_call_and_close():
        """Calls the selected function and closes the menu"""
        global pieMenu_job, last_option
        cron.cancel(pieMenu_job)
        pm.close()
        option = pm.get_option()
        if option: option.function()
        option.focused = False
        last_option = None
        
    def piemenu_launch(screen: int, layer: int = 0):
        """Launches Pie Menu"""
        pm.setup(screen_num=screen - 1, layer=layer)
        if not pm.mcanvas:
            pm.setup(layer=layer)
        pm.show()
        ctx.tags = ["user.pm_showing"]
        global pieMenu_job
        pieMenu_job = cron.interval("16ms", on_interval)
    
    def piemenu_toggle(screen: int, layer: int = 0):
        """Toggles Pie Menu"""
        global pieMenu_job, last_option
        if "user.pm_showing" in ctx.tags:
            cron.cancel(pieMenu_job)
            pm.close()
            ctx.tags = []
            option = pm.get_option()
            if option: option.function()
            option.focused = False
            last_option = None
        else:
            pm.setup(screen_num=screen - 1, layer=layer)
            if not pm.mcanvas:
                pm.setup(layer=layer)
            pm.show()
            ctx.tags = ["user.pm_showing"]
            pieMenu_job = cron.interval("16ms", on_interval)


# Modified from timo's mouse_grid.py
# courtesy of https://github.com/timo/
#   see https://github.com/timo/talon_scripts
# script has only been tested on Windows 10 on a single monitor
from talon import Module, Context, cron, ui
from .piemenu_classes import *
import time

mod = Module()
mod.tag("pm_showing", desc="Tag indicates whether the Pie Menu is showing")
ctx = Context()
piemenu_manager = Manager(menus={
            "_default": [PieMenu(), Inserts()],
            "Firefox": [FireFox_Nav()],
            "Slack": [Slack_Nav()],
            "Microsoft Outlook": [Outlook_Nav()],
        })


none_option = Option(label="_none", function=lambda: None)
last_option = none_option
pieMenu_job = None
timestamp: float = 0

def on_interval():
    global last_option, timestamp, pieMenu_job
    option = piemenu_manager.get_menu_option()
    if option.label != last_option.label:
        last_option.focused = False
        last_option = option
        option.focused = True
        timestamp = time.perf_counter()
    if option.on_hover: 
        option.function()
        return
    if option.on_dwell and time.perf_counter() - timestamp > option.dwell_time:
        PieMenuActions.piemenu_call_and_close(option)



@mod.action_class
class PieMenuActions:     
    def piemenu_call_and_close(option: Option = none_option):
        """Calls the selected function and closes the menu"""
        if not "user.pm_showing" in ctx.tags:
            return
        global pieMenu_job, last_option
        cron.cancel(pieMenu_job)
        piemenu_manager.close_menu()
        ctx.tags = []
        
        option = piemenu_manager.get_menu_option()
        option.function()
        option.focused = False
        last_option = none_option
        
    def piemenu_launch(screen: int, layer: int = 0):
        """Launches Pie Menu"""
        piemenu_manager.set_menu(layer)
        ctx.tags = ["user.pm_showing"]
        
        global pieMenu_job
        pieMenu_job = cron.interval("16ms", on_interval)
    
    def piemenu_toggle(screen: int, layer: int = 0):
        """Toggles Pie Menu"""
        global pieMenu_job, last_option
        if "user.pm_showing" in ctx.tags:
            cron.cancel(pieMenu_job)
            piemenu_manager.close_menu()
            ctx.tags = []
            
            option = piemenu_manager.get_menu_option()
            option.function()
            option.focused = False
            last_option = none_option
        else:
            piemenu_manager.set_menu(layer)
            ctx.tags = ["user.pm_showing"]
            pieMenu_job = cron.interval("16ms", on_interval)


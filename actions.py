# Modified from timo's mouse_grid.py
# courtesy of https://github.com/timo/
#   see https://github.com/timo/talon_scripts
# script has only been tested on Windows 10 on a single monitor
from talon import Module, Context, cron, imgui, actions
from .classes.piemenu import PieMenu
from .classes.option import Option
from .classes.menumanager import manager
import time

mod = Module()
mod.tag("pm_showing", desc="Tag indicates whether the Pie Menu is showing")
ctx = Context()

@imgui.open(w=100, h=100)
def gui_test(gui: imgui.GUI):
    gui.text(f"Hello World!")
    gui.line()
    gui.spacer()
    if gui.button("Close"):
        actions.user.piemenu_editor_close()

@mod.action_class
class PieMenuActions:     
    def piemenu_call_and_close():
        """Calls the selected function and closes the menu"""
        if not "user.pm_showing" in ctx.tags:
            return
        ctx.tags = []
        manager.close_menu()
        
    def piemenu_launch(app_name: str = None, menu_name: str = None):
        """Launches Pie Menu"""
        if "user.pm_showing" in ctx.tags:
            return
        ctx.tags = ["user.pm_showing"]
        
        manager.launch_menu(app_name=app_name, menu_name=menu_name)
    
    def piemenu_toggle(app_name: str = None, menu_name: str = None):
        """Toggles Pie Menu"""
        global pieMenu_job, last_option
        if "user.pm_showing" in ctx.tags:
            ctx.tags = []
            manager.close_menu()
        else:
            ctx.tags = ["user.pm_showing"]
            manager.launch_menu(app_name=app_name, menu_name=menu_name)
            
    def piemenu_editor_show():
        """Show Pie Menu Editor"""
        print("Showing Pie Menu Editor")
        gui_test.show()
        pass
    
    def piemenu_editor_close():
        """Close Pie Menu Editor"""
        print("Closing Pie Menu Editor")
        gui_test.hide()
        pass
        


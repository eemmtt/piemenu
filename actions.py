# Modified from timo's mouse_grid.py
# courtesy of https://github.com/timo/
#   see https://github.com/timo/talon_scripts
# script has only been tested on Windows 10 on a single monitor
from talon import Module, Context, ui
from .classes.piemenu import PieMenu
from .classes.option import Option
from .classes.menumanager import manager
import time

mod = Module()
mod.tag("pm_showing", desc="Tag indicates whether a Pie Menu is showing")
ctx = Context()

# @imgui.open(w=100, h=100)
# def gui_test(gui: imgui.GUI):
#     gui.text(f"Hello World!")
#     gui.line()
#     gui.spacer()
#     if gui.button("Close"):
#         actions.user.piemenu_editor_close()

@mod.action_class
class PieMenuActions:
    def piemenu(state: str):
        """
        Opens, Closes, or Toggles a PieMenu.
        state (str): 
            Must be OPEN, CLOSE, or TOGGLE (case insensitive)
        """
        #need to rethink layer system
        app_name: str = None
        menu_name: str = None
        
        
        def close(app_name: str = None, menu_name: str = None):
            """Calls the selected function and closes the menu"""
            if not "user.pm_showing" in ctx.tags:
                return
            ctx.tags = []
            manager.close_menu()
            
        def launch(app_name: str = None, menu_name: str = None):
            """Launches Pie Menu"""
            if "user.pm_showing" in ctx.tags:
                return
            ctx.tags = ["user.pm_showing"]
            app_name = ui.active_app().name
            manager.launch_menu(app_name=app_name, menu_name=menu_name)
        
        def toggle(app_name: str = None, menu_name: str = None):
            """Toggles Pie Menu"""
            if "user.pm_showing" in ctx.tags:
                ctx.tags = []
                manager.close_menu()
            else:
                ctx.tags = ["user.pm_showing"]
                manager.launch_menu(app_name=app_name, menu_name=menu_name)
        
        states = {
            "OPEN": launch,
            "CLOSE": close,
            "TOGGLE": toggle,
        }
        
        try:
            states[state.upper()](app_name=app_name, menu_name=menu_name)
        except KeyError:
            print(f"'{state}' is not a valid state for piemenu()-")
            print(f"\tValid states are: {list(states.keys())}")
        
            
    def piemenu_editor(state: str):
        """Open or Close Pie Menu Editor"""
    
        def launch():
            """Launch Pie Menu Editor"""
            print("Launching Pie Menu Editor")
            #gui_test.show()
            pass
        
        def close():
            """Close Pie Menu Editor"""
            print("Closing Pie Menu Editor")
            #gui_test.hide()
            pass
        
        states = {
            "OPEN": launch,
            "CLOSE": close,
        }
        
        try:
            states[state.upper()]()
        except KeyError:
            print(f"'{state}' is not a valid state for piemenu_editor()-")
            print(f"\tValid states are: {list(states.keys())}")


from talon import ui, actions, ctrl, cron
from talon.types.point import Point2d
from .piemenu import PieMenu
from .option import Option
import time

class MenuManager:
    def __init__(self) -> None:
       self.menus: dict = {}
       self.active_menu: PieMenu = None
       self.last_menu: PieMenu = None
       self.key_held: bool = False
       
       self.none_option = Option(label="_none", function=lambda: None)
       self.last_option = self.none_option
       self.pieMenu_job = None
       self.timestamp: float = 0
       self.held_keys = []

    def on_interval(self):
       """Called every 16ms to check for user interaction with PieMenu"""
       option = self.active_menu.get_option()
       if option.label != self.last_option.label:
              self.last_option.focused = False
              self.last_option = option
              option.focused = True
              self.timestamp = time.perf_counter()
              self.clear_held_keys()
       if option.on_hover: 
              option.function()
              return
       if option.on_dwell and time.perf_counter() - self.timestamp > option.dwell_time:
              self.timestamp = time.perf_counter()
              option.function()
              return
    
    def create_menu(self, app: str = "_default", options: list[Option] = [], settings: dict = {}) -> None:
       class Menu(PieMenu):
              def __init__(self):
                     super().__init__()
                     for key, value in settings.items():
                            if hasattr(self, key): setattr(self, key, value)
                            else: print(f"Invalid setting: {key}")
                     self.options = options
                     if len(self.options) % 4 == 0:
                            self.start_angle_offset = 0.5 * (360 / len(self.options))

       new_menu = Menu()
       if app in self.menus:
            self.menus[app].append(new_menu)
       else:
              self.menus[app] = [new_menu] 
        
    def switch_to(self, app_name: str, app_layer: int = 0):
       """Switch to a menu by name and layer"""
       def switch():
              if app_name in self.menus.keys():
                     self.active_menu.close()
                     self.last_menu = self.active_menu

                     self.active_menu = self.menus[app_name][app_layer]
                     self.active_menu.setup()
                     self.active_menu.show()
       return switch

    def switch_back(self):
       """Switch back to the last active menu"""
       def switch():
              if self.last_menu:
                     self.active_menu.close()
                     self.active_menu = self.last_menu
                     
                     self.active_menu.setup()
                     self.active_menu.show()
              else:
                     self.active_menu.close()
       return switch
       
    def launch_menu(self, app: str = None, layer: int = 0) -> PieMenu:
       """Set the active menu to a specific menu and display it"""
       if self.active_menu:
              self.active_menu.close()
       self.last_menu = self.active_menu
       
       if app:
              self.active_menu = self.menus[app][layer]
       elif ui.active_app().name in self.menus:
              self.active_menu = self.menus[ui.active_app().name][layer]
       else:
              self.active_menu = self.menus["_default"][layer]
       
       self.active_menu.setup()
       self.active_menu.show()
       
       self.pieMenu_job = cron.interval("16ms", self.on_interval)
    
    def close_menu(self):
       if self.active_menu:
              self.active_menu.close()
       
       cron.cancel(self.pieMenu_job)
       
       option = self.active_menu.get_option()
       option.function()
       self.clear_held_keys()
       
       option.focused = False
       self.last_option = self.none_option

    def clear_held_keys(self):
       if self.held_keys:
              for key in self.held_keys:
                     ctrl.key_press(key=key, down=False)
              self.held_keys = []
       return
                     
    
    #------ option functions ------
    
    def f_shout(self, text: str):
        def shout():
            print(f"shouting {text}!")
        return shout
    
    def f_scroll(self, x: int = 0, y: int = 0, steps: int = 1, delay: float = 0.02):
        def scroll():
            if steps > 1:
                stepped_dist = Point2D(x//steps, y//steps)
                for i in range(steps):
                    actions.mouse_scroll(y=stepped_dist.y, x=stepped_dist.x)
                    time.sleep(delay)
            else:
                actions.mouse_scroll(y=y, x=x)
        return scroll
    
    def f_insert(self, text: str):
        def insert():
            actions.insert(text)
        return insert
    
    def f_key(self, key: str):
        def keypress():
            actions.key(key=key)
        return keypress
 
    def f_key_press_hold(self, key: str):
       def keypress():
              if key not in self.held_keys:
                     self.held_keys.append(key)
                     ctrl.key_press(key=key, down=True)
       return keypress
    
    def f_printAppName(self):
        def printAppName():
            print(ui.active_app().name)
        return printAppName

    def f_macro(self, *functions):
        def macro():
            for function in functions:
                function()
        return macro
 
    
       

#------ Initialize the Menu Manager ------

manager = MenuManager()
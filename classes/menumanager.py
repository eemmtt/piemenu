from talon import ui, actions, ctrl, cron
from talon.types import Point2d
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

    def on_interval(self):
       """Called every 16ms to check for user interaction with PieMenu"""
       option = self.active_menu.get_option()
       if option.label != self.last_option.label:
              self.last_option.focused = False
              self.last_option = option
              option.focused = True
              self.timestamp = time.perf_counter()
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
       
       option.focused = False
       self.last_option = self.none_option
    
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
 
    def f_key_press(self, key: str, hold: int = 0):
        def keypress():
            ctrl.key_press(key=key, hold=hold)
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
manager.create_menu(app="_default",
                    settings={"name": "Default",},
                    options=[
                            Option(label = "Print App Name", 
                                   function = manager.f_printAppName()), 
                            Option(label = "Scroll Up",
                                   function = manager.f_scroll(y=-30),
                                   bg_color="ff3f3fbb",
                                   on_hover=True), 
                            Option(label = "Inserts",
                                   function = manager.switch_to(app_name="_default",app_layer=1),
                                   on_dwell=True,
                                   bg_color="ddaa00bb"), 
                            Option(label = "Active Windows",
                                   function = manager.f_key("win-tab")), 
                            Option(label = "Scroll Down",
                                   function = manager.f_scroll(y=30),
                                   bg_color="1f1fffbb",
                                   on_hover=True), 
                            Option(label = "Last Window",
                                   function = manager.f_key("alt-tab"),),
                     ]
                     )

manager.create_menu(app="_default",
                    settings={"name": "Inserts",
                              "bg_color": "3f3f3fbb",},
                     options= [
                            Option(label = "Close Ticket", 
                                   function = manager.f_macro(
                                          manager.f_insert("Complete"),
                                          manager.f_key("tab"),
                                          manager.f_insert("This ticket will now be closed!\nReply to this message at anytime to reopen the ticket."))),
                            Option(label = "DISM & SFC", function = manager.f_insert("dism /online /cleanup-image /restorehealth & sfc /scannow\n")),
                            Option(label = "Group Update", function = manager.f_insert("gpupdate /force\n")),
                            Option(label = "Sorry", function = manager.f_insert("Sorry")),
                            Option(label = "Please", function = manager.f_insert("Please")),
                            Option(label = "Back to Nav",
                                   function = manager.switch_back(),
                                   on_dwell=True,
                                   bg_color="ddaa00bb"),
                     ]
)  

manager.create_menu(app="Microsoft Edge",
                    settings={"name": "Edge", "bg_color": "ff9922bb"},
                    options=[
                            Option(label = "New Tab", function = actions.app.tab_open),
                            Option(label = "Scroll Up",
                                   function = manager.f_scroll(y=-30),
                                   bg_color="ff3f3fbb",
                                   on_hover=True),
                            Option(label = "Back", 
                                   function = actions.browser.go_back),
                            Option(label = "Active Windows", 
                                   function = manager.f_key("win-tab")),
                            Option(label = "Scroll Down",
                                   function = manager.f_scroll(y=30),
                                   bg_color="1f1fffbb",
                                   on_hover=True,),
                            Option(label = "Last Window", 
                                   function = manager.f_key("alt-tab")),
                    ]
 )

manager.create_menu(app="Firefox",
                    settings={"name": "Firefox Navigation", "bg_color": "ff9922bb"},
                    options=[
                            Option(label = "Back", 
                                   function = actions.browser.go_back),
                            Option(label = "Scroll Up",
                                   function = manager.f_scroll(y=-30),
                                   bg_color="ff3f3fbb",
                                   on_hover=True),
                            Option(label = "Inserts",
                                   function = manager.switch_to(app_name="_default",app_layer=1),
                                   on_dwell=True,
                                   bg_color="ddaa00bb"),
                            Option(label = "Active Windows", 
                                   function = manager.f_key("win-tab")),
                            Option(label = "Scroll Down",
                                   function = manager.f_scroll(y=30),
                                   bg_color="1f1fffbb",
                                   on_hover=True),
                            Option(label = "Last Window", 
                                   function = manager.f_key("alt-tab")),
                ]
                )

manager.create_menu(app="Slack",
              settings={"name": "Slack", "bg_color": "999966bb"},
              options=[
                     Option(label = "Search", 
                            function = manager.f_key("ctrl-k")),
                     Option(label = "Scroll Up",
                            function = manager.f_scroll(y=-10),
                            bg_color="ff3f3fbb",
                            on_hover=True),
                     Option(label = "Go Back", 
                            function = manager.f_key("alt-left")),
                     Option(label = "Active Windows", 
                            function = manager.f_key("win-tab")),
                     Option(label = "Scroll Down",
                            function = manager.f_scroll(y=10),
                            bg_color="1f1fffbb",
                            on_hover=True), 
                     Option(label = "Last Window", 
                            function = manager.f_key("alt-tab")),
                     ]
                     )

manager.create_menu(app="Microsoft Outlook",
                     settings={"name": "Outlook", "bg_color": "886666bb"},
                     options=[
                            Option(label = "Calendar", function = manager.f_key("ctrl-2")),
                            Option(label = "Scroll Up",
                                   function = manager.f_scroll(y=-30),
                                   bg_color="ff3f3fbb",
                                   on_hover=True), 
                            Option(label = "Inbox", function = manager.f_key("ctrl-1")),
                            Option(label = "Active Windows", function = manager.f_key("win-tab")),
                            Option(label = "Scroll Down",
                                   function = manager.f_scroll(y=30),
                                   bg_color="1f1fffbb",
                                   on_hover=True),
                            Option(label = "Last Window", function = manager.f_key("alt-tab")),
                            ]
                            )

manager.create_menu(app="Notion",
                    settings={"name": "Notion",},
                    options=[
                            Option(label = "Print App Name", 
                                   function = manager.f_printAppName()), 
                            Option(label = "Scroll Up",
                                   function = manager.f_scroll(y=-10),
                                   bg_color="ff3f3fbb",
                                   on_hover=True), 
                            Option(label = "Inserts",
                                   function = manager.switch_to(app_name="_default",app_layer=1),
                                   on_dwell=True,
                                   bg_color="ddaa00bb"), 
                            Option(label = "Active Windows",
                                   function = manager.f_key("win-tab")), 
                            Option(label = "Scroll Down",
                                   function = manager.f_scroll(y=10),
                                   bg_color="1f1fffbb",
                                   on_hover=True), 
                            Option(label = "Last Window",
                                   function = manager.f_key("alt-tab"),),
                     ]
                     )

manager.create_menu(app="Miro",
                    settings={"name": "Miro",},
                    options=[
                            Option(label = "Print App Name", 
                                   function = manager.f_printAppName()), 
                            Option(label = "Pan Up",
                                   function = manager.f_shout("pan up"),
                                   bg_color="ff3f3fbb",
                                   on_hover=True), 
                            Option(label = "Inserts",
                                   function = manager.switch_to(app_name="_default",app_layer=1),
                                   on_dwell=True,
                                   bg_color="ddaa00bb"),
                            Option(label = "Active Windows",
                                   function = manager.f_key("win-tab")), 
                            Option(label = "Pan Down",
                                   function = manager.f_shout("pan down"),
                                   bg_color="1f1fffbb",
                                   on_hover=True), 
                            Option(label = "Last Window",
                                   function = manager.f_key("alt-tab"),),
                     ]
                     )
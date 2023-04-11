from talon import ui, actions
from .piemenu import PieMenu
from .option import Option
import time

class MenuManager:
    def __init__(self) -> None:
        self.menus: dict = {}
        self.active_menu: PieMenu = None
        self.last_menu: PieMenu = None
    
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
        
    def switch_menu(self, app_name: str, app_layer: int = 0):
       def switch():
              if app_name in self.menus.keys():
                     self.active_menu.close()
                     self.last_menu = self.active_menu

                     self.active_menu = self.menus[app_name][app_layer]
                     self.active_menu.setup()
                     self.active_menu.show()
       return switch
       
    def set_menu(self, app: str = None, layer: int = 0) -> PieMenu:
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
    
    def close_menu(self):
       if self.active_menu:
              self.active_menu.close()
        
    def get_menu_option(self) -> Option:
        return self.active_menu.get_option()
    
    #------ option functions ------
    
    def f_shout(self, text: str):
        def shout():
            print(f"shouting {text}!")
        return shout
    
    def f_scroll(self, distance: int, steps: int = 1, delay: float = 0.02):
        def scroll():
            if steps > 1:
                stepped_dist = distance//steps
                for i in range(steps):
                    actions.mouse_scroll(y=stepped_dist)
                    time.sleep(delay)
            else:
                actions.mouse_scroll(y=distance)
        return scroll
    
    def f_insert(self, text: str):
        def insert():
            actions.insert(text)
        return insert
    
    def f_key(self, key: str):
        def keypress():
            actions.key(key)
        return keypress
    
    def f_printAppName(self):
        def printAppName():
            print(ui.active_app().name)
        return printAppName

#------ Initialize the Menu Manager ------

manager = MenuManager()
manager.create_menu(app="_default",
                    settings={"name": "Default",},
                    options=[
                            Option(label = "Print App Name", 
                                   function = manager.f_printAppName()), 
                            Option(label = "Scroll Up",
                                   function = manager.f_scroll(distance=-10),
                                   bg_color="ff3f3fbb",
                                   on_hover=True), 
                            Option(label = "Inserts",
                                   function = manager.switch_menu(app_name="_default",app_layer=1),
                                   on_dwell=True,
                                   bg_color="ddaa00bb"), 
                            Option(label = "Active Windows",
                                   function = manager.f_key("win-tab")), 
                            Option(label = "Scroll Down",
                                   function = manager.f_scroll(distance=10),
                                   bg_color="1f1fffbb",
                                   on_hover=True), 
                            Option(label = "Last Window",
                                   function = manager.f_key("alt-tab"),),
                     ]
                     )

manager.create_menu(app="_default",
                    settings={"name": "Inserts",
                              "bg_color": "3f3f3fbb"},
                     options=[
                            Option(label = "Hello", function = manager.f_insert("Hello")),
                            Option(label = "Goodbye", function = manager.f_insert("Goodbye")),
                            Option(label = "Thanks", function = manager.f_insert("Thanks")),
                            Option(label = "Sorry", function = manager.f_insert("Sorry")),
                            Option(label = "Please", function = manager.f_insert("Please")),
                            Option(label = "Back to Nav",
                                   function = manager.switch_menu(app_name="_default",app_layer=0),
                                   on_dwell=True,
                                   bg_color="ddaa00bb"),
                     ]
)  

manager.create_menu(app="Microsoft Edge",
                    settings={"name": "Edge", "bg_color": "ff9922bb"},
                    options=[
                            Option(label = "New Tab", function = actions.app.tab_open),
                            Option(label = "Scroll Up",
                                   function = manager.f_scroll(distance=-30),
                                   bg_color="ff3f3fbb",
                                   on_hover=True),
                            Option(label = "Back", 
                                   function = actions.browser.go_back),
                            Option(label = "Active Windows", 
                                   function = manager.f_key("win-tab")),
                            Option(label = "Scroll Down",
                                   function = manager.f_scroll(distance=30),
                                   bg_color="1f1fffbb",
                                   on_hover=True,),
                            Option(label = "Last Window", 
                                   function = manager.f_key("alt-tab")),
                    ]
 )

manager.create_menu(app="Firefox",
                    settings={"name": "Firefox Navigation", "bg_color": "ff9922bb"},
                    options=[
                            Option(label = "New Tab", 
                                   function = actions.app.tab_open),
                            Option(label = "Scroll Up",
                                   function = manager.f_scroll(distance=-30),
                                   bg_color="ff3f3fbb",
                                   on_hover=True),
                            Option(label = "Back", 
                                   function = actions.browser.go_back),
                            Option(label = "Active Windows", 
                                   function = manager.f_key("win-tab")),
                            Option(label = "Scroll Down",
                                   function = manager.f_scroll(distance=30),
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
                            function = manager.f_scroll(distance=-10),
                            bg_color="ff3f3fbb",
                            on_hover=True),
                     Option(label = "Go Back", 
                            function = manager.f_key("alt-left")),
                     Option(label = "Active Windows", 
                            function = manager.f_key("win-tab")),
                     Option(label = "Scroll Down",
                            function = manager.f_scroll(distance=10),
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
                                   function = manager.f_scroll(distance=-30),
                                   bg_color="ff3f3fbb",
                                   on_hover=True), 
                            Option(label = "Inbox", function = manager.f_key("ctrl-1")),
                            Option(label = "Active Windows", function = manager.f_key("win-tab")),
                            Option(label = "Scroll Down",
                                   function = manager.f_scroll(distance=30),
                                   bg_color="1f1fffbb",
                                   on_hover=True),
                            Option(label = "Last Window", function = manager.f_key("alt-tab")),
                            ]
                            )
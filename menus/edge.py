from talon import actions
from ..classes.option import Option
from ..classes.menumanager import manager

manager.create_menu(app_name="Microsoft Edge",
                    menu_name="Main",
                    settings={"bg_color": "ff9922bb"},
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
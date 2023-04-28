from talon import actions
from ..classes.option import *
from ..classes.menumanager import manager

manager.create_menu(app_name="Firefox",
                    menu_name="Main",
                    settings={"bg_color": "ff9922bb"},
                    options=[
                            Option(label = "Back", 
                                   function = actions.browser.go_back),
                            Option(label = "Scroll Up",
                                   function = scroll(y=-30),
                                   bg_color="ff3f3fbb",
                                   on_hover=True),
                            Option(label = "Inserts",
                                   function = manager.switch_to(app_name="_default",menu_name="Inserts"),
                                   on_dwell=True,
                                   bg_color="ddaa00bb"),
                            Option(label = "Active Windows", 
                                   function = key("win-tab")),
                            Option(label = "Scroll Down",
                                   function = scroll(y=30),
                                   bg_color="1f1fffbb",
                                   on_hover=True),
                            Option(label = "Last Window", 
                                   function = key("alt-tab")),
                ]
                )
from ..classes.option import Option
from ..classes.menumanager import manager

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
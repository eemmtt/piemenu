from ..classes.option import Option
from ..classes.menumanager import manager

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
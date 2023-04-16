from ..classes.option import Option
from ..classes.menumanager import manager

manager.create_menu(app="Miro",
                    settings={"name": "Miro",},
                    options=[
                            Option(label = "Print App Name", 
                                   function = manager.f_printAppName()), 
                            Option(label = "Navigation",
                                   function = manager.switch_to(app_name="Miro",app_layer=1),
                                   on_dwell=True,
                                   bg_color="ddaa00bb"),
                            Option(label = "Active Windows",
                                   function = manager.f_key("win-tab")), 
                            Option(label = "Last Window",
                                   function = manager.f_key("alt-tab"),),
                     ]
                     )

manager.create_menu(app="Miro",
                    settings={"name": "Miro Nav",},
                    options=[
                            Option(label = "Pan Right",
                                   function = manager.f_key_press_hold("right"),
                                   bg_color="ff3f3fbb",
                                   on_hover=True),
                            Option(label = "Pan Up",
                                   function = manager.f_key_press_hold("up"),
                                   bg_color="ff3f3fbb",
                                   on_hover=True),
                            Option(label = "Pan Left",
                                   function = manager.f_key_press_hold("left"),
                                   bg_color="ff3f3fbb",
                                   on_hover=True),
                            Option(label = "Pan Down",
                                   function = manager.f_key_press_hold("down"),
                                   bg_color="1f1fffbb",
                                   on_hover=True),
                     ]
                     )
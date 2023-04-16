from ..classes.option import Option
from ..classes.menumanager import manager

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
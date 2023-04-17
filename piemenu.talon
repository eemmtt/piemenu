#Commands used to control the PieMenu
-
#user.piemenu_launch(app_name: str = "_default", menu_name: str = "Main")
deck(pedal_right:down): user.piemenu_launch()
deck(pedal_right:up): user.piemenu_call_and_close()

#user.piemenu_toggle(app_name: str = "_default", menu_name: str = "Main")
#key(f24): user.piemenu_toggle()
#key(f24): user.piemenu_editor_show()
key(f24:down): user.piemenu_launch()
key(f24:up): user.piemenu_call_and_close()
key(ctrl-alt-a:down): user.piemenu_launch()
key(ctrl-alt-a:up): user.piemenu_call_and_close()
#Commands used to control the PieMenu
-
#user.piemenu_launch(screen_number:int = 1, piemenu_layer:int = 0)
deck(pedal_right:down): user.piemenu_launch(1,0)
deck(pedal_right:up): user.piemenu_call_and_close()

#user.piemenu_toggle(screen_number:int = 1, piemenu_layer:int = 0)
key(ctrl-alt-a): user.piemenu_toggle(1,0)
#deck(pedal_right): user.piemenu_toggle(1,0)

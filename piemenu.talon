#Commands used to control the PieMenu
-
#user.piemenu_launch(screen_number:int = 1, menu_layer:int = 0)
deck(pedal_right:down): user.piemenu_launch(1,0,0)
deck(pedal_right:up): user.piemenu_call_and_close()

deck(button_5:down): user.piemenu_launch(1,1,0)
deck(button_5:up): user.piemenu_call_and_close()

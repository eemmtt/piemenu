#Commands used to control the PieMenu
-
deck(pedal_right:down): user.piemenu("open")
deck(pedal_right:up): user.piemenu("close")

#key(f24): user.piemenu("toggle")
#key(f24): user.piemenu_editor("open")
key(f24:down): user.piemenu("open")
key(f24:up): user.piemenu("close")
key(ctrl-alt-a:down): user.piemenu("open")
key(ctrl-alt-a:up): user.piemenu("close")
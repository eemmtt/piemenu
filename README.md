# PieMenu for Talon  
PieMenu is a contextual menu for use with a mouse (or Talon's "Control Mouse"), inspired by Blender's useful Pie Menus.  
PieMenu has only been tested on Windows 10 with Talon Rust.  
PieMenu is a WIP and was originally modified from timo's mouse_grid.py, see:  
https://github.com/timo/  
https://github.com/timo/talon_scripts 
  
Talon:  
https://talonvoice.com/  
https://talonvoice.slack.com/

## Installation  
Clone the repo to [talon home]\user  
[Talon Home] can be found by navigating to Talon's Options>Scripting>"Talon Home"

## Using Pie Menu
Edit piemenu.talon to use your desired hotkeys.
> By default, Pie Menu is triggered using the Right Streamdeck Foot Pedal  

Press and hold the hotkey to display the Pie Menu at your cursor.  
Move your cursor outward to the 'slice' of the Pie Menu with your desired action.
> Slices extend outwards, beyond the drawn Pie Menu to the active screen's limits.  

Release the hotkey to trigger the indicated action.  

## Customizing Pie Menu

1. Add the settings and functions for your custom Pie Menu to a class inheriting from 'App_Specific_Vars' in 'piemenu_classes.py'
> At the time of writing, functions called by PieMenu should take no parameters (other than self)
2. Add your custom class to the dict 'piemenu_variations' located at the bottom of 'piemenu_classes.py' 
- key = The name of the app where your Pie Menu should display (the result of talon.ui.active_app().name)  
- value = Your_Custom_Class()
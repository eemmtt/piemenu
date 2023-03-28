# PieMenu for Talon  
PieMenu is a contextual menu for use with a mouse.  
At this time, PieMenu has only been tested on Windows 10 with Talon Rust, on a single monitor.  

## Installation  
Clone (download) the repo to "[Talon Home]/user"  
[Talon Home] can be found by navigating to Scripting>"Talon Home" in Talon.

## Using Pie Menu
Edit piemenu.talon to use your desired hotkeys.  

PieMenu has two modes of interaction:
1. Press and Hold, Release
2. Toggle

### Press and hold, Release  
1. Press and hold the assigned hotkey to display the Pie Menu at your cursor location.  
2. Move your cursor outward to the 'slice' of the Pie Menu with your desired action.  
    > Slices extend outwards, beyond the drawn Pie Menu to the active screen's limits.  

3. Release the hotkey to trigger the indicated action and close the Pie Menu.

### Toggle
1. Tap the hotkey to display the Pie Menu at your cursor location.
2. Tap the hotkey again to trigger the selected action and close the Pie Menu.

## Customizing Pie Menu
Pie Menus are displayed based on the active application and the triggered Pie Menu layer.  
A Pie Menu's appearence and actions are defined in the class ```SettingsAndFunctions``` in ```piemenu_classes.py```  
Custom Pie Menus are defined in their own class inheriting from ```SettingsAndFunctions```.

### Create a Custom Pie Menu:

1. Create a class for your custom pie menu in ```piemenu_classes.py``` inheriting from ```SettingsAndFunctions```:
```python
class CustomPieMenu(SettingsAndFunctions):
    def __init__(self):
        super().__init__()
        #settings you want to overwrite from SettingsAndFunctions
        self.bg_color = "ff00ffff" #hexadecimal RR-GG-BB-AA
        
        #the options you want to appear on your Custom PieMenu
        #self.options takes an array of tuples (string, function object)
        self.options = [
                ("New Tab",             actions.app.tab_open),
                ("Scroll Up",           self.f_scroll(-400)),
                ("Close Tab",           actions.app.tab_close),
                ("Back",                actions.browser.go_back),
                ("Scroll Down",         self.f_scroll(400)),
                ("Focus Search Bar",    actions.browser.focus_address),
                ]
```
2. Add your custom class to the dictionary ```piemenu_variations``` located at the bottom of ```piemenu_classes.py```. The key must match the result of ```ui.active_app().name``` to trigger within an active app. If you want your PieMenu to trigger when the active app is unspecified, add it to ```piemenu_variations["_default"]```.
```python
piemenu_variations = {
    "_default": [SettingsAndFunctions()],
    "AppName": [CustomPieMenu_Layer0(), CustomPieMenu_Layer1()],
}
```
  

3. In your .talon file, the 2nd paramenter in ```user.piemenu_launch``` and ```user.piemenu_toggle``` is the layer number. In the following example, ```deck(pedal_right:down)``` triggers the 0th layer in the active context, ```key(ctrl-alt-a)``` triggers the 1st layer. 
```talon
    deck(pedal_right:down): user.piemenu_launch(1,0)
    key(ctrl-alt-a): user.piemenu_toggle(1,1)
```


## Acknowledgement
PieMenu was inspired by Blender's useful custom Pie Menus.  
> https://github.com/scorpion81/blender-addons/blob/master/ui_pie_menus_official.py

PieMenu was originally modified from Timo's mouse_grid.py, see:  
>https://github.com/timo/talon_scripts   

I ♥ Talon:  
>https://talonvoice.com/  
>https://talonvoice.slack.com/
# PieMenu for Talon  
![image](https://user-images.githubusercontent.com/52972088/227623461-fd36b39d-0487-4d29-ae0a-10962a343c05.png)

PieMenu is a contextual menu for use with a mouse.  
At this time, PieMenu has only been tested on Windows 10 with Talon Rust.

## Installation  
Clone (download) the repo to "[Talon Home]/user"  
[Talon Home] can be found by navigating to Scripting>"Talon Home" in Talon.

## Using Pie Menu
Edit ```piemenu.talon``` to use your desired hotkey or command.  
If using a hotkey, it's recommended to use one without modifier keys (eg. ctrl, alt, shift).

### PieMenu has two modes of interaction:
1. Press and Hold, Release
2. Toggle

#### Press and Hold, Release  
1. Press and hold the assigned hotkey to display the Pie Menu at your cursor location.  
2. Move your cursor outward to the 'slice' of the Pie Menu with your desired action.  
    > Slices extend outwards, beyond the drawn Pie Menu to the active screen's limits.  

3. Release the same hotkey to trigger the indicated action and close the Pie Menu.
    > Releasing the assigned hotkey while your cursor is within the innermost circle of the PieMenu ("Dead Zone") will close the Pie Menu without triggering an action.  
    
#### Toggle
1. Tap the hotkey to display the Pie Menu at your cursor location.
2. Tap the hotkey again to trigger the selected action and close the Pie Menu.

## Customizing Pie Menu
The ```MenuManager``` class contains many Pie Menus.  
Each Pie Menu inherits from ```PieMenu``` and contains many ```Options```, which are the slices of the pie.  
Pie Menus are displayed based on the active application and the specified layer.
A custom Pie Menu's settings and ```Options``` are specified when it is added to the ```MenuManager```.

### Create a Custom Pie Menu:

1. Custom Pie Menus are added to the ```MenuManager``` at the bottom of ```classes/menumanager.py```.   
```MenuManager.create_menu()``` takes:
    1. An app name, matching the result of ```talon.ui.active_app()```.  
    Menus with app name ```_default``` will trigger in any app that is unspecified in the ```MenuManager```, 
    2. A dict of ```PieMenu``` attributes to override, 
    3. A list of ```Option``` objects.  

    ```Options``` take a minimum of a ```label``` to be displayed, and a ```function``` object to be triggered.  
    ```Options``` can also be specified to trigger ```on_hover``` and ```on_dwell```! 

    ```python
    manager = MenuManager()
    manager.create_menu(app="_default",
                        settings={"name": "Default",},
                        options=[
                            Option(label = "Print App Name", 
                                   function = manager.f_printAppName()), 
                            Option(label = "Scroll Up",
                                   function = manager.f_scroll(distance=-10),
                                   bg_color="ff3f3fbb",
                                   on_hover=True), 
                            Option(label = "Inserts",
                                   function = manager.switch_menu(app_name="_default",app_layer=1),
                                   on_dwell=True,
                                   bg_color="ddaa00bb"), 
                            Option(label = "Active Windows",
                                   function = manager.f_key("win-tab")), 
                            Option(label = "Scroll Down",
                                   function = manager.f_scroll(distance=10),
                                   bg_color="1f1fffbb",
                                   on_hover=True), 
                            Option(label = "Last Window",
                                   function = manager.f_key("alt-tab"),),
                        ]
                     )
    ```
  

2. In ```piemenu.talon```, the 2nd paramenter in ```user.piemenu_launch``` and ```user.piemenu_toggle``` is the layer number.   
In the following example, ```deck(pedal_right:down)``` triggers the 0th layer in the active context, ```key(f24)``` triggers the 1st layer. 
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

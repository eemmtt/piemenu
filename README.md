# PieMenu for Talon  
<<<<<<< HEAD
![image](https://user-images.githubusercontent.com/52972088/232621242-b1d1f4b7-c09a-4c5a-9a01-02add9d72c37.png)
=======
![image](https://user-images.githubusercontent.com/52972088/232621066-6bf41e05-018a-442d-ae2f-6cfa1e66142d.png)
>>>>>>> b249a4d4049b120eab000a7e5d78288be7e31652

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
    2. A menu name, unique to menus within that app.  
    The primary menu for each app should be named *"Main"*.
    2. An optional dict of ```PieMenu``` attributes to override, 
    3. A list of 1 or more ```Option``` objects.  

    ```Options``` take a minimum of a ```label``` to be displayed, and a ```function``` object to be triggered.  
    ```Options``` can also be specified to trigger ```on_hover``` and ```on_dwell```! 

    ```python
    manager = MenuManager()
    manager.create_menu(app_name="_default", 
                        menu_name="Main",
                        settings={"fill": False,
                                  "explode_offset": 10,},
                        options=[
                            Option(label = "Print App Name", 
                                   function = manager.f_printAppName()), 
                            Option(label = "Scroll Up",
                                   function = manager.f_scroll(distance=-10),
                                   bg_color="ff3f3fbb",
                                   on_hover=True), 
                            Option(label = "Inserts",
                                   function = manager.switch_menu(app_name="_default",menu_name="Inserts"),
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
  

2. In ```piemenu.talon```, ```user.piemenu_launch()``` and ```user.piemenu_toggle()``` will launch the Pie Menu with ```menu_name="Main"``` of the active application.   
The optional arguments ```app_name``` and ```menu_name``` can be used together to trigger a specific Pie Menu. 
    ```talon
    deck(pedal_right:down): user.piemenu_launch(app_name="_default", menu_name="CustomMenu")
    key(ctrl-alt-a): user.piemenu_toggle(app_name="Firefox", menu_name="Navigation")
    ```


## Acknowledgement
PieMenu was inspired by Blender's useful custom Pie Menus.  
> https://github.com/scorpion81/blender-addons/blob/master/ui_pie_menus_official.py

PieMenu was originally modified from Timo's mouse_grid.py, see:  
>https://github.com/timo/talon_scripts   

I ♥ Talon:  
>https://talonvoice.com/  
>https://talonvoice.slack.com/

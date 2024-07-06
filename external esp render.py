from pyMeow import *
import os
import json
import time
from win32api import GetSystemMetrics
import random
import string
import tkinter as tk
import threading

print("Width =", GetSystemMetrics(0))
print("Height =", GetSystemMetrics(1))


def EXTERNALUI():
    import dearpygui.dearpygui as dpg
    import ctypes
    import random
    import string
    import os
    import json

    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "drawingdata", "settings.json")

    def generate_random_string(length=10):
        characters = string.ascii_letters + string.digits + string.punctuation
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    def windows_popup(title, message):
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

    width = 700
    height = 700
    drag_zone_height = 5
    title_bar_drag = False

    def exit():
        dpg.destroy_context()

    dpg.create_context()
    viewport = dpg.create_viewport(title=generate_random_string(15), width=width, height=height, decorated=True, resizable=False, always_on_top=True)
    dpg.setup_dearpygui()

    id_to_name = {}
    defaultsettingsDONOTCHANGE = {
        "Enable_render": True,
        "Render_teammates": False,
        "Enable_tracers": True,
        "Enable_names": True,
        "Tracer_line_thickness": 1.0,
        "Tracer_line_color": [255.0, 0.0, 0.0, 255.0],
        "Enable_compatibility": False,
        "Enable_distance": True,
        "Tracer_line_offset": 0
    }

    def load_settings():

        with open(json_file_path, 'r') as f:
            return json.load(f)


    def save_settings():
        while True:
            time.sleep(.05)
            with open(json_file_path, 'w') as f:
                json.dump(settings, f, indent=4)
    threading.Thread(target=save_settings).start()
    global settings
    settings = load_settings()
    
    id_to_name = {}

    def button_callback(sender):

        print(f"Button clicked! Sender: {id_to_name[sender]}")
        if id_to_name[sender] == "Revert_all_changes": #NOT WORKING
            settings = defaultsettingsDONOTCHANGE.copy()


            for item_id, item_name in id_to_name.items():
                if item_name in defaultsettingsDONOTCHANGE:
                    value = defaultsettingsDONOTCHANGE[item_name]
                    dpg.set_value(item_id, value)
                    print(f"Reverted {item_name} to {value}")
                    

        else:
            settings[id_to_name[sender]] = True


    def checkbox_callback(sender):
        value = dpg.get_value(sender)
        print(f"Checkbox value: {value}, Sender: {id_to_name[sender]}")
        settings[id_to_name[sender]] = value


    def slider_callback(sender):
        value = dpg.get_value(sender)
        print(f"Slider value: {value}, Sender: {id_to_name[sender]}")
        settings[id_to_name[sender]] = value


    def color_picker_callback(sender):
        color = dpg.get_value(sender)
        print(f"Selected color: {color}, Sender: {id_to_name[sender]}")
        settings[id_to_name[sender]] = color


    with dpg.window(label="coldsnow external rendering settings", width=700, height=700, no_collapse=True, no_move=True, no_resize=True) as win:
        with dpg.tab_bar():
            with dpg.tab(label="Main"):
                dpg.add_text("Hello, World!")
                #btn_id = dpg.add_button(label="Revert all changes", callback=button_callback)
                #id_to_name[btn_id] = "Revert_all_changes"

                chk_id = dpg.add_checkbox(label="Compatibility mode (only enable if you encounter freezing issues)", callback=checkbox_callback)
                dpg.set_value(chk_id, settings.get("Enable_compatibility", False))
                id_to_name[chk_id] = "Enable_compatibility"

                chk_id = dpg.add_checkbox(label="Render", callback=checkbox_callback)
                dpg.set_value(chk_id, settings.get("Enable_render", True))
                id_to_name[chk_id] = "Enable_render"

                chk_id = dpg.add_checkbox(label="Render teammates", callback=checkbox_callback)
                dpg.set_value(chk_id, settings.get("Render_teammates", False))
                id_to_name[chk_id] = "Render_teammates"

                chk_id = dpg.add_checkbox(label="Enable names", callback=checkbox_callback)
                dpg.set_value(chk_id, settings.get("Enable_names", True))
                id_to_name[chk_id] = "Enable_names"

                chk_id = dpg.add_checkbox(label="Enable distance", callback=checkbox_callback)
                dpg.set_value(chk_id, settings.get("Enable_distance", True))
                id_to_name[chk_id] = "Enable_distance"
            
                chk_id = dpg.add_checkbox(label="Enable tracers", callback=checkbox_callback)
                dpg.set_value(chk_id, settings.get("Enable_tracers", True))
                id_to_name[chk_id] = "Enable_tracers"

                sld_id = dpg.add_slider_float(label="Tracer line Y axis offset", default_value=settings.get("Tracer_line_offset", 0), min_value=-70, max_value=70.0, format="%.0f", callback=slider_callback)
                id_to_name[sld_id] = "Tracer_line_offset"

                sld_id = dpg.add_slider_float(label="Tracer line thickness", default_value=settings.get("Tracer_line_thickness", 2), max_value=5.0, format="%.0f", callback=slider_callback)
                id_to_name[sld_id] = "Tracer_line_thickness"
                
                clr_id = dpg.add_color_picker(label="Tracer line color", default_value=settings.get("Tracer_line_color", [255, 0, 0, 255]), callback=color_picker_callback, height=155, width=155)
                id_to_name[clr_id] = "Tracer_line_color"

    def cal_dow(sender, data):
        global title_bar_drag
        if dpg.is_mouse_button_down(0):
            if dpg.get_mouse_pos()[1] <= drag_zone_height:
                pass
        else:
            title_bar_drag = False

    def cal(sender, data):
        global title_bar_drag
        if title_bar_drag:
            pos = dpg.get_viewport_pos()
            x = data[1]
            y = data[2]
            final_x = pos[0] + x
            final_y = pos[1] + y
            dpg.configure_viewport(viewport, x_pos=final_x, y_pos=final_y)

    with dpg.handler_registry():
        dpg.add_mouse_drag_handler(0, callback=cal)
        dpg.add_mouse_move_handler(callback=cal_dow)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
#end of external ui
threading.Thread(target=EXTERNALUI).start()



current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, "drawingdata", "data.json")
settings_file_path = os.path.join(current_dir, "drawingdata", "settings.json")
screenx = GetSystemMetrics(0) #https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics
screeny = GetSystemMetrics(1)
print(screenx)
# Initialize overlay
def run_calibrating():
    global renderoffsetX, renderoffsetY
    
    # Create a root window
    root2 = tk.Tk()

    # Function to get window size after it's maximized
    def get_window_size():
        global renderoffsetX, renderoffsetY
        renderoffsetX = root2.winfo_width()
        renderoffsetY = root2.winfo_height()
        print(f"Width: {renderoffsetX}, Height: {renderoffsetY}")
    
    # Set the window to be maximized
    root2.state('zoomed')
    
    # Call get_window_size after a short delay to ensure window is maximized
    root2.after(100, get_window_size)

    # Set the window transparency to 30%
    root2.attributes('-alpha', 0.3)

    # Create a label with large text
    label = tk.Label(root2, text="Calibrating render offsets", font=("Helvetica", 48))
    label.pack(expand=True)

    # Close the window
    root2.after(1000, root2.destroy)

    # Run the main loop
    root2.mainloop()
run_calibrating()
def generate_random_string(length=10):
    # Define the characters to choose from: letters, digits, and punctuation
    characters = string.ascii_letters + string.digits + string.punctuation
    # Randomly select characters from the defined set
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return f"{random_string}"

overlay_init("Full",1000000,generate_random_string(length=10))
tracercolor = new_color(255, 0, 0, 255)
textcolor = new_color(0, 0, 0, 255)
textstrokecolor = new_color(255, 255, 255, 255)

def create_stroked_text(text,x, y, font_size, fill_color, stroke_width=1):
    if text == "  ":
        none1 = 0
    else:
        
        for dx in range(-stroke_width, stroke_width + 1, stroke_width):
            for dy in range(-stroke_width, stroke_width + 1, stroke_width):
                if dx != 0 or dy != 0:  # Skip the center to avoid duplicate, saves little performance.
                    draw_text(text,x+dx,y+dy-30,font_size,textstrokecolor)
        draw_text(text,x,y-30,font_size,textcolor)


offset = -10

while overlay_loop():
    draw_fps(screenx-100,0+50)
    try:
        # Read JSON data from file
        with open(json_file_path, 'r') as f:
            jsondata = json.load(f)

        with open(settings_file_path, 'r') as f:
            settingdata = json.load(f)
        
        if settingdata["Enable_render"] == True:
            # Begin drawing
            begin_drawing()

            # Draw the line based on JSON data
            for data in jsondata:
                startPosX = data["X"]
                startPosY = data["Y"]
                endPosX = data["X"]
                endPosY = data["Y"]
                if settingdata["Enable_names"]:
                    name = data["name"]
                else:
                    name=""
                if settingdata["Enable_distance"]:
                    distance = data["Distance"]
                else:
                    distance=""

                #name
                print(settingdata["Tracer_line_color"][1])
                print(tracercolor)
                create_stroked_text(f"{name}  {distance}",endPosX,endPosY-20,10,textcolor)
                draw_line(screenx/2, 0, endPosX, endPosY+((screeny-renderoffsetY)/2)-offset-settingdata["Tracer_line_offset"], new_color(round(settingdata["Tracer_line_color"][0]),round(settingdata["Tracer_line_color"][1]),round(settingdata["Tracer_line_color"][2]),round(settingdata["Tracer_line_color"][3])),settingdata["Tracer_line_thickness"])

            # End drawing
            end_drawing()
        else:
            end_drawing()
    except json.JSONDecodeError as e:
        # Handle the error (e.g., wait for the file to be readable again)
        time.sleep(.001)  # Wait for 1 second before retrying

# Close overlay
overlay_close()

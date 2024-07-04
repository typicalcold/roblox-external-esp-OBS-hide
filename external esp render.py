import tkinter as tk
import win32gui
import win32con
import ctypes
from tkinter import font
import threading
import time
import os
import json
print("starting external esp")


current_dir = os.path.dirname(os.path.abspath(__file__))

# Function to make the window transparent and click-through
def make_window_transparent_and_clickthrough(hwnd):
    styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
    win32gui.SetLayeredWindowAttributes(hwnd, 0x00ffffff, 0, win32con.LWA_COLORKEY)

# Function to handle closing the window
def close_window():
    root.destroy()

# Create the main window
root = tk.Tk()
root.attributes('-fullscreen', True)  # Set fullscreen, obv

# Ensure the window is created before trying to get its handle!
root.update_idletasks()
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())

# Set window texts
win32gui.SetWindowText(hwnd, "Coldsnow's drawing thing, very pasted!, very skidded!, Not a virus!")

# Make the window topmost (as yopu can see)
root.attributes('-topmost', True)

# Create a canvas for drawing/rendering lines
canvas = tk.Canvas(root, bg='white', highlightthickness=0, bd=4)
canvas.pack(fill=tk.BOTH, expand=True)

# Function to draw a line!
def draw_line(x1, y1, x2, y2, color):
    return canvas.create_line(x1, y1, x2, y2, fill=color)

# Function to draw stroked text
def create_stroked_text(x, y, text, stroke_color, fill_color, stroke_width=1, font_size=10):
    text_font = font.Font(family="Helvetica", size=font_size, weight="bold")
    text_objects = []
    for dx in range(-stroke_width, stroke_width + 1, stroke_width):
        for dy in range(-stroke_width, stroke_width + 1, stroke_width):
            if dx != 0 or dy != 0:  # Skip the center to avoid duplicate, saves little performance.
                text_objects.append(canvas.create_text(x + dx, y + dy, text=text, font=text_font, fill=stroke_color))
    text_objects.append(canvas.create_text(x, y, text=text, font=text_font, fill=fill_color))
    return text_objects

# Make the window transparent and click-through
make_window_transparent_and_clickthrough(hwnd)

# Bind closing event to the window
root.protocol("WM_DELETE_WINDOW", close_window)

json_file_path = os.path.join(current_dir, "drawingdata", "data.json")

data_lock = threading.Lock()
data = []

# Function to load JSON data from file with retries until successful
def load_json_data():
    while True:
        try:
            with open(json_file_path, 'r') as file:
                new_data = json.load(file)
            with data_lock:
                global data
                data = new_data
            time.sleep(0.0001)  

        except json.JSONDecodeError:
            print("json error")
            time.sleep(0.01)  

# Start the JSON loading in a separate thread
threading.Thread(target=load_json_data, daemon=True).start()


# Global variables to store window size
renderoffsetX = 0
renderoffsetY = 0

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

# Create a new thread to run the tkinter main loop
calibratingthread = threading.Thread(target=run_calibrating)
calibratingthread.start()

# Wait for the calibratingthread to finish
calibratingthread.join()

# Now print the final window size after it has been maximized
print(f"Final Width: {renderoffsetX}, Final Height: {renderoffsetY}")

#root.winfo_screenheight()-renderoffsetY



# Function to update canvas
def update_canvas():
    with data_lock:
        current_data = data
    # Clear previous lines and texts, to draw new ones next frame

    canvas.delete("all")
    
    if len(current_data) == 0:
        pass

    # Draw new lines and texts for every item in the json file
    for entry in current_data: # for every peice of data within the json file
        x_value = entry["X"]
        y_value = entry["Y"]
        username = entry["name"]
        distance = entry["Distance"] #capitilzied D for no reasionn!
        print(f'{username} moved to (X:{x_value}, Y: {y_value})')
        draw_line(root.winfo_screenwidth() / 2,0, x_value, y_value+((root.winfo_screenheight()-renderoffsetY)/2), "blue")
        create_stroked_text(x_value, y_value - 50, text=f"{username}  {round(distance)}", stroke_color='#fcfcfb', fill_color='black')


# Function to update canvas looped
def update_periodically():
    update_canvas()
    root.after(1, update_periodically)  # Update approximately 60 times per second (i think)

# Start updating canvas in a loop
update_periodically()

# Run the drawing
root.mainloop()

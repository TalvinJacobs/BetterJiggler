import ctypes
import tkinter as tk
import time
import threading

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def queryMousePosition():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def moveMouse(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

mouse_moving = False

def jiggle_mouse():
    while True:
        if mouse_moving:
            x, y = queryMousePosition()
            moveMouse(x+1, y+1)
            time.sleep(1)
            x, y = queryMousePosition()
            moveMouse(x-1, y-1)
            time.sleep(1)

def toggle_mouse_moving():
    global mouse_moving
    mouse_moving = not mouse_moving
    button_text.set("Stop" if mouse_moving else "Start")

def start_gui():
    global button_text
    root = tk.Tk()
    root.title("Better Jiggler by TJ")
    root.geometry('300x35')
    button_text = tk.StringVar()
    button_text.set("Start")
    button = tk.Button(root, textvariable=button_text, command=toggle_mouse_moving)
    button.pack()
    root.mainloop()

t = threading.Thread(target=jiggle_mouse)
t.start()

start_gui()

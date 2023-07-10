import ctypes
import tkinter as tk
import time
import threading
import subprocess
 
LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort
 
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", LONG),
                ("dy", LONG),
                ("mouseData", DWORD),
                ("dwFlags", DWORD),
                ("time", DWORD),
                ("dwExtraInfo", ULONG_PTR))
 
class INPUT(ctypes.Structure):
    _fields_ = (("type", DWORD),
                ("mi", MOUSEINPUT))
 
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
 
def move_mouse(dx, dy):
    x = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(dx=dx, dy=dy, mouseData=0, dwFlags=MOUSEEVENTF_MOVE, time=0))
    ctypes.windll.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
 
mouse_moving = False
 
def jiggle_mouse():
    global stop_thread
    while not stop_thread: 
        if mouse_moving: 
            move_mouse(10, 10) 
            time.sleep(1) 
            move_mouse(-10, -10) 
            time.sleep(0.5)
        else:
            time.sleep(1)
 
def toggle_mouse_moving():
    global mouse_moving
    mouse_moving = not mouse_moving
    button_text.set("Stop" if mouse_moving else "Start")

def on_closing(root):
    global stop_thread
    stop_thread = True
    root.destroy()

def start_gui():
    global button_text, stop_thread
    root = tk.Tk()
    root.title("Better Jiggler by TJ")
    root.geometry('300x35')
    button_text = tk.StringVar()
    button_text.set("Start")
    button = tk.Button(root, textvariable=button_text, command=toggle_mouse_moving)
    button.pack()
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()


if __name__ == '__main__':
    stop_thread = False
    t = threading.Thread(target=jiggle_mouse)
    t.start()
    start_gui()

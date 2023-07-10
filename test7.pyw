import ctypes
import time
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt

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
    while True: 
        if mouse_moving: 
            move_mouse(10, 10) 
            time.sleep(1) 
            move_mouse(-10, -10) 
            time.sleep(0.5)

class ColorWidget(QWidget):
    def __init__(self, parent=None):
        super(ColorWidget, self).__init__(parent)
        self.setWindowTitle('BetterJiggler by TJ')
        self.setFixedSize(265, 100)

    def paintEvent(self, event):
        painter = QPainter(self)
        color = QColor("#04A777") if mouse_moving else QColor("#D90368")
        painter.fillRect(self.rect(), color)

    def mousePressEvent(self, event):
        global mouse_moving
        mouse_moving = not mouse_moving
        self.update()

if __name__ == '__main__':
    import sys
    t = threading.Thread(target=jiggle_mouse)
    t.start()

    app = QApplication(sys.argv)
    ex = ColorWidget()
    ex.show()
    sys.exit(app.exec_())

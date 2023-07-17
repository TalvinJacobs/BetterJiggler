import sys
import ctypes
import time
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", LONG),
                ("dy", LONG),
                ("mouseData", DWORD),
                ("dwFlags", DWORD),
                ("time", DWORD),
                ("dwExtraInfo", ULONG_PTR)]

class INPUT(ctypes.Structure):
    _fields_ = [("type", DWORD),
                ("mi", MOUSEINPUT)]

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

def move_mouse(dx, dy):
    x = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(dx=dx, dy=dy, mouseData=0, dwFlags=MOUSEEVENTF_MOVE, time=0))
    ctypes.windll.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

class MouseJiggler(QThread):
    updated = pyqtSignal()
    
    def __init__(self):
        super(MouseJiggler, self).__init__()
        self.mouse_moving = False
        self.stop_thread = False
    
    def run(self):
        while not self.stop_thread: 
            if self.mouse_moving: 
                move_mouse(10, 10) 
                time.sleep(1) 
                move_mouse(-10, -10) 
                time.sleep(0.5)
                self.updated.emit()
            else:
                time.sleep(1)
    
    def toggle_mouse_moving(self):
        self.mouse_moving = not self.mouse_moving
        self.updated.emit()

class ColorWidget(QWidget):
    def __init__(self, jiggler, parent=None):
        super(ColorWidget, self).__init__(parent)
        self.setWindowTitle('BetterJiggler by TJ')
        self.setFixedSize(265, 100)
        self.jiggler = jiggler
        self.jiggler.updated.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)
        color = QColor("#04A777") if self.jiggler.mouse_moving else QColor("#D90368")
        painter.fillRect(self.rect(), color)

    def mousePressEvent(self, event):
        self.jiggler.toggle_mouse_moving()
        self.update()

def run_app():
    app = QApplication(sys.argv)
    jiggler = MouseJiggler()
    jiggler.start()
    ex = ColorWidget(jiggler)
    ex.show()
    return_code = app.exec_()
    jiggler.stop_thread = True
    sys.exit(return_code)

if __name__ == '__main__':
    run_app()

# # from threading import Thread
# import keyboard
# import time
# import psutil
#
#
# def action():
#     exe = [psutil.Process(p) for p in psutil.pids()]
#     proceed = False
#     for i in exe:
#         try:
#             if i.status() == "running" and i.name() == "MinecraftLauncher.exe":
#                 proceed = True
#                 break
#         except:
#             pass
#     if proceed:
#         time.sleep(1)
#         keyboard.press_and_release('t')
#         time.sleep(1)
#         keyboard.write("/wild")
#         time.sleep(.5)
#         keyboard.press_and_release('enter')
#     else:
#         print("Minecraft Launcher is not running.")
#
#
# if __name__ == '__main__':
#     keyboard.add_hotkey('`', callback=action)
#     keyboard.wait(']')
#

from g import Ui_MinecraftAutoCommand
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import sys
from uiConfig import *


class StartUtility(QtWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.utility = Window()
        self.utility.show()


class Window(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MinecraftAutoCommand()
        self.ui.setupUi(self)
        self.ui.dragFrame.mouseMoveEvent = self.mouseMoveEvent
        self.dragPos = QtCore.QPoint()
        self.setWindowIcon(QIcon('images/logo.png'))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        Action.init_ui(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()


if __name__ == "__main__":
    app = StartUtility(sys.argv)
    sys.exit(app.exec_())
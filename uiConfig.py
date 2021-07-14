from PyQt5.QtCore import QTimer, QTime
from PyQt5 import QtGui
import keyboard
# from threading import Timer
from datetime import datetime
import os
import random
import json
import psutil
import time


def current_time():
    t = QTime.currentTime().toString()
    am_pm = "pm" if 12 < int(t[:2]) < 23 else "am"
    return t + " " + am_pm


def current_time2():
    return QTime.currentTime().toString()


def read_file():
    try:
        with open('hotkeys.json', 'r') as openfile:
            json_object = json.load(openfile)
    except:
        json_object = {"hotkey": []}
    return json_object


def write_file(hotkey, cmd):
    try:
        if not os.path.exists('hotkeys.json'):
            with open('hotkeys.json', 'w'):
                pass
            dictionary = [{"key": hotkey, "cmd": cmd}]
        else:
            data = read_file()
            dictionary = data['hotkeys'] + [{"key": hotkey, "cmd": cmd}]

        with open("hotkeys.json", "w") as outfile:
            outfile.write(json.dumps({"hotkeys": dictionary}, indent=4))
    except:
        os.remove("hotkeys.json")
        with open('hotkeys.json', 'w'):
            pass
        dictionary = [{"key": hotkey, "cmd": cmd}]
        with open("hotkeys.json", "w") as outfile:
            outfile.write(json.dumps({"hotkeys": dictionary}, indent=4))


class Action:
    """
    System / Ui
    """
    def ui_log(self, message):
        t, c = current_time2(), self.ui.log.count()
        self.ui.log.setCurrentRow(c - 1)
        if c > 100:
            self.ui.log.clear()
            self.ui.log.addItem("{} [CLEARED LOG]".format(t))
        self.ui.log.takeItem(c - 1)
        self.ui.log.addItem("{} {}".format(t, message))
        self.ui.log.addItem("")

    def update_time(self):
        msg = random.choice((["Event Log"] * 150) + ["CHRIST_1S_KING"])
        self.ui.eventLogLabel.setText(msg)
        self.ui.lastUpdate.setText(current_time())

    def init_ui(self):
        self.setFixedWidth(630)
        self.setFixedHeight(630)
        self.ui.lastUpdate.setText(current_time())
        self.ui.close.clicked.connect(lambda: self.close())
        self.ui.minimize.clicked.connect(lambda: self.showMinimized())
        self.ui.startBtn.clicked.connect(lambda: Action.start(self))
        self.ui.stopBtn.clicked.connect(lambda: Action.stop(self))
        self.ui.addBtn.clicked.connect(lambda: Action.add(self))
        self.ui.hotkeyEdit.returnPressed.connect(lambda: Action.add(self))
        self.ui.cmdEdit.returnPressed.connect(lambda: Action.add(self))
        self.ui.pressEnter.stateChanged.connect(lambda: Action.stop(self))
        write_file("shift + b", "Romans 5:8")
        self.ui.startBtn.show()
        self.ui.stopBtn.hide()
        self.ui.timer = QTimer()
        self.ui.timer.timeout.connect(lambda: Action.update_time(self))
        self.ui.timer.start(1000)

    def keyboard_act(self, key, cmd):
        exe = [psutil.Process(p) for p in psutil.pids()]
        proceed = False
        for i in exe:
            try:
                if i.status() == "running" and i.name() == "MinecraftLauncher.exe":
                    proceed = True
                    break
            except:
                pass
        if proceed:
            Action.ui_log(self, f"Executing [ {key}  {cmd} ]")
            time.sleep(1)
            keyboard.press_and_release('t')
            time.sleep(1)
            keyboard.write(cmd)
            if self.ui.pressEnter.isChecked():
                time.sleep(.5)
                keyboard.press_and_release('enter')
        else:
            Action.ui_log(self, "Minecraft Launcher is not running. :)")

    """
    Logger
    """
    def start(self):
        self.ui.log.clear()
        self.ui.log.addItem("{} [CLEARED LOG]".format(current_time2()))
        try:
            data = read_file()['hotkeys']
        except:
            data = []

        if data:
            Action.ui_log(self, "Starting Hot Key Recognition!")
            keyboard.add_hotkey(self.ui.emergencyKey.text(), callback=Action.stop, args=(self,))
            commands, count = "", 1
            for i in data:
                commands += f"\n{count}. [ {i['key']}  {i['cmd']} ]"
                count += 1
                keyboard.add_hotkey(i['key'], callback=Action.keyboard_act, args=(self, i['key'], i['cmd']))
            Action.ui_log(self, f"Adding keys:{commands}\nInserted into hotkeys.json")
            self.ui.startBtn.hide()
            self.ui.stopBtn.show()
        else:
            Action.ui_log(self, "Add a hot key and command. :)")

    def stop(self):
        try:
            Action.ui_log(self, "Stopping Hot Key Recognition!")
            keyboard.unhook_all_hotkeys()
        except:
            pass
        self.ui.startBtn.show()
        self.ui.stopBtn.hide()

    def add(self):
        if self.ui.hotkeyEdit.text() != "" and self.ui.cmdEdit.text() != "":
            data = read_file()
            if self.ui.hotkeyEdit.text() in [i['key'] for i in data['hotkeys']]:
                Action.ui_log(self, f"The {self.ui.hotkeyEdit.text()} hot key already exists.")
            else:
                self.ui.log.clear()
                self.ui.log.addItem("{} [CLEARED LOG]".format(current_time2()))
                Action.ui_log(self, f"Adding: [ {self.ui.hotkeyEdit.text()}  {self.ui.cmdEdit.text()} ]")
                write_file(self.ui.hotkeyEdit.text(), self.ui.cmdEdit.text())
                self.ui.hotkeyEdit.setText("")
                self.ui.cmdEdit.setText("")
                Action.stop(self)

        else:
            Action.ui_log(self, "WARNING! Enter inputs. :)")


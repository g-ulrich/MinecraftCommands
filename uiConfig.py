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
HOTKEYS_FILE = "hotkeys.json"


def current_time():
    t = QTime.currentTime().toString()
    am_pm = "pm" if 12 < int(t[:2]) < 23 else "am"
    return t + " " + am_pm


def current_time2():
    return QTime.currentTime().toString()


def file_exist():
    return os.path.exists(HOTKEYS_FILE)


def create_file():
    with open(HOTKEYS_FILE, 'w'):
        pass
    with open(HOTKEYS_FILE, "w") as outfile:
        outfile.write(json.dumps({"hotkeys": []}, indent=4))


def read_file():
    if file_exist():
        with open(HOTKEYS_FILE, 'r') as openfile:
            json_object = json.load(openfile)
        return json_object['hotkeys']
    else:
        create_file()
        return []


def write_file(hotkey, cmd):
    dictionary = read_file() + [{"key": hotkey, "cmd": cmd}]
    with open("hotkeys.json", "w") as outfile:
        outfile.write(json.dumps({"hotkeys": dictionary}, indent=4))


def is_minecraft_running():
    exe = [psutil.Process(p) for p in psutil.pids()]
    proceed = False
    for i in exe:
        try:
            if i.status() == "running" and i.name() == "MinecraftLauncher.exe":
                proceed = True
                break
        except:
            pass
    return proceed


class Action:
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
        self.ui.pressEnter.stateChanged.connect(lambda: Action.stop(self, emergency=True))
        self.ui.cmdEdit.returnPressed.connect(lambda: Action.add(self))
        self.ui.pressEnter.stateChanged.connect(lambda: Action.stop(self))
        Action.ui_log(self, f"There are currently {len(read_file())} hotkeys...")
        if read_file():
            commands, count = "", 1
            for i in read_file():
                commands += f"\n{count}. [ {i['key']}  {i['cmd']} ]"
                count += 1
            Action.ui_log(self, f"Available keys:{commands}")
        self.ui.startBtn.show()
        self.ui.stopBtn.hide()
        self.ui.timer = QTimer()
        self.ui.timer.timeout.connect(lambda: Action.update_time(self))
        self.ui.timer.start(1000)

    def keyboard_act(self, key, cmd):
        if is_minecraft_running():
            Action.ui_log(self, f"Executing [ {key}  {cmd} ]")
            keyboard.press_and_release('t')
            time.sleep(.5)
            keyboard.write(cmd)
            if self.ui.pressEnter.isChecked():
                # time.sleep(.5)
                keyboard.press_and_release('enter')
        else:
            Action.stop(self)
            Action.ui_log(self, "Minecraft Launcher is not running. :)")

    def add(self):
        if file_exist():
            key = self.ui.hotkeyEdit.text()
            cmd = self.ui.cmdEdit.text()
            if key != "" and cmd != "":
                hotkeys_list = read_file()
                if key in [i['key'] for i in hotkeys_list]:
                    Action.ui_log(self, f"The [ {key} ] hot key already exists.")
                else:
                    self.ui.log.clear()
                    write_file(key, cmd)
                    Action.ui_log(self, f"Added: [ {key}  {cmd} ]")
                    self.ui.cmdEdit.setText("")
                    self.ui.hotkeyEdit.setText("")
            else:
                Action.ui_log(self, "WARNING! Enter inputs. :)")
        else:
            create_file()
            Action.ui_log(self, f"{HOTKEYS_FILE} created.")
            Action.add(self)

    def start(self):
        if is_minecraft_running():
            if read_file():
                self.ui.log.clear()
                Action.ui_log(self, "Started! :)")
                keyboard.add_hotkey(self.ui.emergencyKey.text(), callback=Action.stop, args=(self,))
                commands, count = "", 1
                for i in read_file():
                    commands += f"\n{count}. [ {i['key']}  {i['cmd']} ]"
                    count += 1
                    keyboard.add_hotkey(i['key'], callback=Action.keyboard_act, args=(self, i['key'], i['cmd']))
                Action.ui_log(self, f"Available keys:{commands}")
                self.ui.startBtn.hide()
                self.ui.stopBtn.show()
                self.ui.addBtn.setEnabled(False)
                self.ui.hotkeyEdit.setEnabled(False)
                self.ui.cmdEdit.setEnabled(False)
                self.ui.pressEnter.setEnabled(False)
                self.ui.emergencyKey.setEnabled(False)
            else:
                Action.ui_log(self, "Add some hotkeys! :)")
        else:
            Action.stop(self)
            self.ui.log.clear()
            Action.ui_log(self, "Minecraft Launcher is not running. :)")

    def stop(self, emergency=False):
        if not emergency:
            Action.ui_log(self, "Stopped all hotkeys!")
            try:
                keyboard.unhook_all_hotkeys()
            except:
                pass
        else:
            if read_file():
                Action.ui_log(self, "Stopping relevant functions!")
                try:
                    keyboard.unhook_all_hotkeys()
                    Action.ui_log(self, "Unhooking all hotkeys...")
                except:
                    pass
        self.ui.startBtn.show()
        self.ui.stopBtn.hide()
        self.ui.addBtn.setEnabled(True)
        self.ui.hotkeyEdit.setEnabled(True)
        self.ui.cmdEdit.setEnabled(True)
        self.ui.pressEnter.setEnabled(True)
        self.ui.emergencyKey.setEnabled(True)

from script import Script
from ui import Roxui
import pygetwindow as gw

def searchroxwindow(window_list, window_title):
    for w in window_list:
        if w.title == window_title:
            # print(w.title)
            return w

    raise Exception('No ROX window found !')

roxui = Roxui()

title = roxui.getEntry()
# print(title)
# roxui.destroy()

window = searchroxwindow(gw.getWindowsWithTitle(title), title)

script = Script(title, window)
script.script_action()
# print(roxui.getEntry())



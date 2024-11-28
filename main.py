from script import Script
from ui import Roxui
import pygetwindow as gw
import ctypes

def searchroxwindow(window_list, window_title):
    for w in window_list:
        if w.title == window_title:
            # print(w.title)
            return w

    raise Exception('No ROX window found !')


def get_screen_resolution():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()  # 解決高 DPI 環境下的縮放問題
    width = user32.GetSystemMetrics(0)  # 螢幕寬度
    height = user32.GetSystemMetrics(1)  # 螢幕高度
    return width, height

w, h = get_screen_resolution()
print(f'螢幕解析度為 {w} X {h}')
roxui = Roxui()

title, counts = roxui.getEntry()
if title != '':
    window = searchroxwindow(gw.getWindowsWithTitle(title), title)
    script = Script(title, window, counts)
    script.script_action()

else:
    raise Exception('No title !')




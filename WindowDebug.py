import pygetwindow as gw
from PIL import ImageGrab

def searchroxwindow(window_list, window_title):
    for w in window_list:
        if w.title == window_title:
            # print(w.title)
            return w

    raise Exception('No ROX window found !')

def screenshot_window(rox_window):
    # 擷取視窗範圍
    bbox = (rox_window.left, rox_window.top, rox_window.left + rox_window.width, rox_window.top + rox_window.height)
    screenshot = ImageGrab.grab(bbox)

    # 儲存圖片
    screenshot.save("screenshot.png")
    print("視窗截圖已儲存為 screenshot.png")


title = 'ROX-2002'

# 截圖
window = searchroxwindow(gw.getWindowsWithTitle(title), title)
screenshot_window(window)

print(window.height, window.width)


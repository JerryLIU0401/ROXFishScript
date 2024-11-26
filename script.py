import pyautogui
import pygetwindow as gw
import time
from PIL import ImageGrab
import keyboard
import time
import numpy as np
import cv2


PIXEL_THRESHOLD = '#abe368'
SCRIPT_INTERVAL = 0.1
SECOND_CLICK_INTERVAL = 2


class Script():
    def __init__(self, title, rox_window):
        self.window_title = title
        self.rox_window = rox_window

    def searchroxwindow(self, window_list):
        for w in window_list:
            if w.title == self.window_title:
                return w

        raise Exception('No ROX window found !')

    def rgb_to_hex(self, rgb):
        """將 RGB 格式顏色轉為 HEX"""
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

    def hex_to_bgr(self, hex_color):
        """將 HEX 顏色轉為 BGR 格式（OpenCV 使用 BGR）"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        return rgb[::-1]  # 轉為 BGR

    def is_color_close(self, pixel_color, target_color, threshold=50):
        """
        判斷像素顏色是否接近目標顏色
        :param pixel_color: (B, G, R) 格式的像素顏色
        :param target_color: (B, G, R) 格式的目標顏色
        :param threshold: 顏色接近的距離閾值
        :return: True if the pixel color is close to the target color, else False
        """
        pixel = np.array(pixel_color, dtype=np.int16)
        target = np.array(target_color, dtype=np.int16)
        distance = np.sqrt(np.sum((pixel - target) ** 2))  # 計算歐幾里得距離
        print(f'distance: {distance}')
        return distance <= threshold

    def press_z_stop(self):
        if keyboard.is_pressed('z'):
            return True

    def script_action(self):
        # window_w, window_h = self.rox_window.width, self.rox_window.height
        # print(f'width: {window_w} \nheight: {window_h}')
        self.rox_window.resizeTo(995, 600)
        window_x, window_y = self.rox_window.left, self.rox_window.top
        # print(window_x, window_y)
        offset_x, offset_y = 802, 465  # 視窗內相對座標
        target_x, target_y = window_x + offset_x, window_y + offset_y
        # print(target_x, target_y)
        last_time = time.time()
        pyautogui.click(x=target_x, y=target_y)
        print(f'THRESHOLD: {self.hex_to_bgr(PIXEL_THRESHOLD)}')

        # 擷取整個螢幕並獲取像素
        while True:
            if self.press_z_stop():
                return

            if time.time() - last_time > SCRIPT_INTERVAL:
                last_time = time.time()
                screenshot = ImageGrab.grab()
                pixel_color = screenshot.getpixel((target_x, target_y))[::-1]  # bgr
                print(f"視窗內相對座標 ({offset_x}, {offset_y}) 的像素顏色為：{pixel_color}")
                if self.is_color_close(pixel_color, self.hex_to_bgr(PIXEL_THRESHOLD)):
                    print('click')
                    pyautogui.click(x=target_x, y=target_y)
                    click_last_time = time.time()

                    while not self.press_z_stop():
                        if time.time() - click_last_time > SECOND_CLICK_INTERVAL:
                            pyautogui.click(x=target_x, y=target_y)
                            break


    # 獲取目標視窗
    # window_title = "ROX"  # 修改為目標視窗的標題
    # window = gw.getWindowsWithTitle(window_title)
    # rox_window = ''
    # for w in window:
    #     if w.title == window_title:
    #         rox_window = w

    # if rox_window == '':
    #     # print('No ROX window found')
    #     raise Exception('No ROX window found !')
    # 獲取視窗位置
    # window_w, window_h = rox_window.width, rox_window.height
    # print(f'width: {window_w} \nheight: {window_h}')
    # rox_window.resizeTo(944, 572)
    # window_x, window_y = rox_window.left, rox_window.top
    # print(window_x, window_y)
    # offset_x, offset_y = 775, 398  # 視窗內相對座標
    # target_x, target_y = window_x + offset_x, window_y + offset_y
    # print(target_x, target_y)
    #
    # # 擷取視窗範圍
    # bbox = (rox_window.left, rox_window.top, rox_window.left + rox_window.width, rox_window.top + rox_window.height)
    # screenshot = ImageGrab.grab(bbox)

    # 儲存圖片
    # screenshot.save("screenshot.png")
    # print("視窗截圖已儲存為 screenshot.png")

    # pixel_threshold = '#cbf76f'
    # interval = 0.1
    # last_time = time.time()
    # pyautogui.click(x=target_x, y=target_y)
    # # 擷取整個螢幕並獲取像素
    # while True:
    #     if keyboard.is_pressed('z'):
    #         break
    #
    #     if time.time() - last_time > interval:
    #         last_time = time.time()
    #         screenshot = ImageGrab.grab()
    #         pixel_color = screenshot.getpixel((target_x, target_y))[::-1] # bgr
    #         print(f"視窗內相對座標 ({offset_x}, {offset_y}) 的像素顏色為：{pixel_color}")
    #         if is_color_close(pixel_color, hex_to_bgr( pixel_threshold)):
    #             print('click')
    #             pyautogui.click(x=target_x, y=target_y, clicks=2, interval=4)

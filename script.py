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
SECOND_CLICK_INTERVAL = 4
RESIZE_WIDTH = 995
RESIZE_HEIGHT = 600
INITIAL_OFFSET_X = 802 # 視窗內相對座標X
INITIAL_OFFSET_Y = 465 # 視窗內相對座標Y



class Script():
    def __init__(self, title, rox_window, counts=100):
        self.window_title = title
        self.rox_window = rox_window
        self.counts = counts
        self.last_distance = 0

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
        distance = int(np.sqrt(np.sum((pixel - target) ** 2)))  # 計算歐幾里得距離

        if self.last_distance != distance:
            print(f'distance: {distance}')
            self.last_distance = distance

        return distance <= threshold

    def press_z_stop(self):
        if keyboard.is_pressed('z'):
            print('--- 停止程式 ---')
            return True

    # def calculate_position(self, x1, y1, W1, H1, W2, H2):
    #     x2 = x1 * (W2 / W1)
    #     y2 = y1 * (H2 / H1)
    #     return x2, y2

    def script_action(self):
        # window_w, window_h = self.rox_window.width, self.rox_window.height
        # print(f'width: {window_w} \nheight: {window_h}')
        self.rox_window.resizeTo(RESIZE_WIDTH, RESIZE_HEIGHT)
        window_x, window_y = self.rox_window.left, self.rox_window.top
        # print(window_x, window_y)
        offset_x, offset_y = 802, 465  # 視窗內相對座標
        target_x, target_y = window_x + offset_x, window_y + offset_y
        # print(target_x, target_y)
        last_time = time.time()
        last_pixel_color = None
        pyautogui.click(x=target_x, y=target_y)
        # print(f'THRESHOLD: {self.hex_to_bgr(PIXEL_THRESHOLD)}')

        fish_counts = 0

        # 擷取整個螢幕並獲取像素
        while True:
            if self.press_z_stop():
                return

            if time.time() - last_time > SCRIPT_INTERVAL and fish_counts < self.counts:
                last_time = time.time()
                screenshot = ImageGrab.grab()
                pixel_color = screenshot.getpixel((target_x, target_y))[::-1]  # bgr

                if pixel_color != last_pixel_color:
                    print(f"視窗內絕對座標 ({target_x}, {target_y})")
                    print(f"視窗內相對座標 ({offset_x}, {offset_y})")
                    print(f"像素顏色為：{pixel_color}")
                    print('========================================')

                last_pixel_color = pixel_color

                if self.is_color_close(pixel_color, self.hex_to_bgr(PIXEL_THRESHOLD)):
                    print('click')
                    pyautogui.click(x=target_x, y=target_y)
                    time.sleep(0.1)
                    pyautogui.click(x=target_x, y=target_y)
                    click_last_time = time.time()

                    while True:
                        if self.press_z_stop() or fish_counts >= self.counts:
                            return

                        if time.time() - click_last_time > SECOND_CLICK_INTERVAL:
                            pyautogui.click(x=target_x, y=target_y)
                            time.sleep(0.1)
                            pyautogui.click(x=target_x, y=target_y)
                            fish_counts += 1
                            print(f'fish_counts = {fish_counts}')
                            break



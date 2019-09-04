import random
import time

from win32 import win32gui, win32print, win32api
import win32con
from PIL import ImageGrab
import numpy as np
import cv2
from ctypes import windll

from image import Image
import adb

user32 = windll.user32
user32.SetProcessDPIAware()

def get_all_windows():
    hwndList = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwndList)
    return hwndList

def get_windows_name(hwndList):
    nameList = list(map(lambda x: win32gui.GetWindowText(x), hwndList))
    return nameList

def get_windows_class(hwndList):
    classList = list(map(lambda x: win32gui.GetClassName(x), hwndList))
    return classList

def get_hwnds_name_like(name):
    hwnds = []
    hwndAll = get_all_windows()
    nameList = get_windows_name(hwndAll)
    for i in range(len(nameList)):
        if name in nameList[i]:
            hwnds.append(hwndAll[i])
    return hwnds

class Device(object):
    # device param
    device_name = ""
    device_index = 0
    device_left = 0
    device_top = 0
    device_width = 0
    device_height = 0
    device_support = ['emu', 'android']
    device_resize = 1
    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type
        if device_type == 'emu':
            self.init_emu()

    def create_device(device_name, device_type, device_index=0):
        if (device_type == 'emu'):
            hwnds = get_hwnds_name_like(device_name)
            if (device_index >= 0 and device_index < len(hwnds)):
                device = Device(hwnds[device_index], 'emu')
                device.device_name = device_name
                device.device_index = device_index
                return device
            return None
        elif (device_type == 'android'):
            device = Device(0, 'android')
            return device
        else:
            return None

    def init_emu(self):
        hwnd = self.device_id
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        self.device_left = left
        self.device_top = top
        self.device_width = (right - left)
        self.device_height = (bot - top)

    def screenshot(self):
        img = None
        if (self.device_type == 'emu'):
            hwnd = self.device_id
            left = self.device_left
            top = self.device_top
            width = self.device_width
            height = self.device_height

            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(hwnd)
            img = np.array(ImageGrab.grab(bbox=(left, top, left+width, top+height)))
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        elif (self.device_type == 'android'):
            img = adb.screenshot()
            
        return Image(img)

    def realclick(self, p1, p2):
        # p1 is left-top, p2 is right-bottom
        min_x = min(p1[0], p2[0])
        min_y = min(p1[1], p2[1])
        max_x = max(p1[0], p2[0])
        max_y = max(p1[1], p2[1])
        offset_x = int(0.2 * abs(p1[0] - p2[0]))
        offset_y = int(0.2 * abs(p1[1] - p2[1]))
        x = random.randint(min_x+offset_x, max_x-offset_x)
        y = random.randint(min_y+offset_y, max_y-offset_y)
        self.click(x, y)
        return       

    def click(self, x, y):
        if (self.device_type == 'emu'):
            win32gui.ShowWindow(self.device_id, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(self.device_id)
            win32api.SetCursorPos([self.device_left+x, self.device_top+y])      
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.5)
        elif (self.device_type == 'android'):
            adb.click(x, y)
            time.sleep(0.5)
        return


if __name__ == '__main__':
    # device = Device.create_device("模拟器", 'emu')
    device = Device.create_device("安卓", 'android')
    img = device.screenshot()
    select = img.select()
    select.save("device_test.jpg")
    select = Image.read("device_test.jpg")
    p1, p2 = img.match(select)
    device.realclick(p1, p2)
    
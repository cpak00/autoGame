import subprocess

import cv2
import numpy as np

adb_path = 'bin\\adb'

def screenshot():
    adb = subprocess.Popen([adb_path, 'shell', 'screencap', '-p'], stdout=subprocess.PIPE)
    content = adb.stdout.read()
    content = content.replace(b'\r\n', b'\n')
    image = np.asarray(bytearray(content), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def click(x, y):
    adb = subprocess.Popen([adb_path, 'shell', 'input', 'tap', str(x), str(y)])

if __name__ == '__main__':
    image = screenshot()
    cv2.imshow('screenshot', image)
    cv2.waitKey(0)
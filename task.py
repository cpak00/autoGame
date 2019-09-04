import os
import time
import ctypes

from device import Device
from image import Image

player = ctypes.windll.kernel32

def mkdir(name):
    folder = os.path.exists(name)
    if not folder:
        os.makedirs(name)            

class Task(object):
    def __init__(self, device, name):
        self.device = device
        self.name = name
        return

    def wait(self, num):
        time.sleep(num)

    def beep(self):
        player.Beep(2000, 200)

    def exist(self, num):
        p1 = None
        p2 = None
        flag = 0
        while (p1 is None or p2 is None):
            image = Image.read(self.name+"/"+str(num)+".jpg")
            p1, p2 = self.device.screenshot().match(image, self.device.device_resize)
            flag = flag+1
            if (flag > 10):
                return False
        print("exist "+str(num))
        return True

    def find(self, num):
        p1 = None
        p2 = None
        flag = 0
        while (p1 is None or p2 is None):
            image = Image.read(self.name+"/"+str(num)+".jpg")
            p1, p2 = self.device.screenshot().match(image, self.device.device_resize)
            flag = flag+1
            if (flag > 1e8):
                raise Exception("timeout")
        print("find "+str(num))
        return

    def clickuntil(self, num):
        p1 = True
        p2 = True
        while (p1 is not None or p2 is not None):
            image = Image.read(self.name+"/"+str(num)+".jpg")
            p1, p2 = self.device.screenshot().match(image, self.device.device_resize)
            if (p1 is not None and p2 is not None):
                self.device.realclick(p1, p2)
        print("click until "+str(num))
        return

    def clickifexist(self, num):
        image = Image.read(self.name+"/"+str(num)+".jpg")
        p1, p2 = self.device.screenshot().match(image, self.device.device_resize)
        if (p1 is None or p2 is None):
            return
        self.device.realclick(p1, p2)
        print("click "+str(num))
        return

    def click(self, num):
        p1 = None
        p2 = None
        flag = 0
        while (p1 is None or p2 is None):
            image = Image.read(self.name+"/"+str(num)+".jpg")
            p1, p2 = self.device.screenshot().match(image, self.device.device_resize)
            flag = flag+1
            if (flag > 1e8):
                raise Exception("timeout")
        self.device.realclick(p1, p2)
        print("click "+str(num))
        return

    def create_task(device, name):
        mkdir(name)
        script_text = "from task import Task\nfrom device import Device\n"
        script_text=script_text+'device=Device.create_device(\"'+device.device_name+'","'+device.device_type+'",'+str(device.device_index)+')\n'
        script_text=script_text+"task=Task(device"+",\""+name+"\")\n"
        step_num = int(input("从步骤（）开始录制"))
        while(True):
            step = Task.create_step(device, name+"/"+str(step_num))
            if step is None:
                break
            else:
                script_text=script_text+"task."+step+"("+str(step_num)+")\n"
                step_num = step_num + 1

        fid = open(name+'.py', 'a+')
        fid.write(script_text)
        return

    def create_step(device, step_name):
        command = input("请输入下一个步骤: ")
        if command == 'end':
            return None
        else:
            img = device.screenshot()
            select = img.select()
            select.save(str(step_name)+".jpg")
            return command




if __name__ == '__main__':
    device = Device.create_device("MuMu", 'emu')
    fireblue = Task.create_task(device, "hlzx_sb")

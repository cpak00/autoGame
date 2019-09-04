from task import Task
from device import Device
device=Device.create_device("MuMu","android")
device.device_resize = 3.32/2.65
task=Task(device,"hlzx_sb")
#task.click(0)
#task.click(1)
#task.click(2)
task.clickifexist(10)
task.click(3)
task.click(4)
task.click(5)
task.click(6)
for i in range(10):
    assistant = task.exist(11)
    if (not assistant):
        print("assistant fight")
        task.click(12)
    task.click(7)
    task.wait(0.5)
    success = task.exist(8)
    if (not success):
        task.beep()
        break
    task.click(8)
    task.find(9)
    task.clickuntil(9)


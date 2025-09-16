from village.devices.sound_device import sound_device
from village.manager import get_task, manager

task = get_task()

def function1():
    # stop sound
    sound_device.stop()


def function2():
    # load the sound loaded in manager
    sound_device.load(left=manager.task.crescendo_sound, right=manager.task.crescendo_sound)


def function3():
    # play the sound
    sound_device.play()

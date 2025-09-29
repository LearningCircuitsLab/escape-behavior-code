from village.devices.sound_device_new import sound_device
from sound_functions import crescendo_looming_sound
from village.manager import manager
import time


def function1():
    # stop sound
    sound_device.stop()


def function2():
    # load the sound loaded in manager
    sound_device.load(left=manager.task.crescendo_sound, right=manager.task.crescendo_sound)


def function3():
    # play the sound
    sound_device.play()


def function5():
    amp_for_70dB = 0.05  # ~75 dB SPL
    amp_for_20dB = 0.0001  # ?? dB SPL
    # create a crescendo sound
    crescendo_sound = crescendo_looming_sound(
        amp_start=amp_for_20dB,
        amp_end=amp_for_70dB,
        ramp_duration=0.4,
        ramp_down_duration=0.005,
        hold_duration=0.595,
        n_repeats=4,
    )
    # load the sound loaded in manager
    sound_device.stop()
    sound_device.load(right=crescendo_sound, left=crescendo_sound)
    # play the sound
    sound_device.play()
    time.sleep(3)
    sound_device.stop()

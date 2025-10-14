from village.classes.abstract_classes import CameraBase
from village.custom_classes.camera_trigger_base import CameraTriggerBase
from village.manager import manager


class CameraTrigger(CameraTriggerBase):
    def __init__(self) -> None:
        self.name = "Camera Trigger"

    def trigger(self, cam: CameraBase) -> None:

        # the camera automatically returns a True value if the subject is detected
        # within any of the predefined trigger areas.
        # then we can assign a function to be executed when the area is triggered

        # get the area number from the settings
        #area_number = int(manager.task.settings.trigger_area)
        area_number = 2
        # assign the area to a variable
        if area_number == 1:
            variable_to_check = cam.area1_is_triggered
        elif area_number == 2:
            variable_to_check = cam.area2_is_triggered
        elif area_number == 3:
            variable_to_check = cam.area3_is_triggered
        elif area_number == 4:
            variable_to_check = cam.area4_is_triggered

        if variable_to_check:
            cam.write_text(f"Animal in Area {area_number}")
            manager.task.animal_in_trigger_zone = True
        else:
            cam.write_text(f"Animal outside Area {area_number}")
            manager.task.animal_in_trigger_zone = False

        # # you can check the position of the animal manually, for example
        # # if it is inside a circle send a message to the bpod
        # center_x, center_y = 100, 250
        # radius = 50
        # val = (cam.x_position - center_x) ** 2 + (cam.y_position - center_y) ** 2
        # inside_circle = val <= radius ** 2

        # if inside_circle:
        #     cam.write_text("Inside circle")
        #     manager.task.bpod.receive_softcode(1)

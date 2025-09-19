from village.classes.task import Task
import random
from sound_functions import crescendo_looming_sound
from village.manager import manager
import time
import softcode_functions
import numpy as np


class EscapeBehavior(Task):
    def __init__(self):
        super().__init__()

        self.info = """

        Escape Behavior Task
        -------------------

        Animals are placed in an open arena with a shelter located in one side.
        There is a trigger zone defined by the user. When the animal enters this zone,
        there is a chance that a looming sound is played, prompting the animal to escape to the shelter.
        """

        # create a list to hold the states
        self.states_visited = []
        # states are tupples of (START,END,MSG)

    def start(self):
        # open the raw file
        with self.raw_session_path.open("a") as self.raw_file:
            self.raw_file.write("TRIAL;START;END;MSG;VALUE\n")
        
        # create a crescendo sound
        self.crescendo_sound = crescendo_looming_sound(
            amp_start=self.settings.starting_amplitude,
            amp_end=self.settings.ending_amplitude,
            ramp_duration=self.settings.ramp_duration,
            ramp_down_duration=self.settings.ramp_down_duration,
            hold_duration=self.settings.hold_duration,
            n_repeats=self.settings.n_repeats,
        )


    def create_trial(self):
        # stop any sound that might be playing
        softcode_functions.function1()
        # innitiate grace period state
        self.current_state = (self.chrono.now() , np.nan , "grace_period")
        # reset the timer for triggering attempts
        self.triggering_time_reset = self.chrono.now() - np.timedelta64(int(self.settings.time_between_sound_triggering_attempts * 1000), 'ms')
        # load the sound
        softcode_functions.function2()
        # get the current camera frame
        self.last_camera_frame = manager.cam.frame_number

        # while loop to go through states
        while True:
            time.sleep(0.001)
            # if the frame of the camera has not changed, skip the rest of the loop
            if manager.cam.frame_number == self.last_camera_frame:
                continue
            # if the frame has changed, update the last camera frame
            self.last_camera_frame = manager.cam.frame_number

            match self.current_state[2]:
                case "grace_period":
                    if (self.chrono.now() - self.current_state[0]).total_seconds() > self.settings.grace_period:
                        if self.is_animal_in_trigger_zone():
                            self.change_state_to("animal_inside_trigger_zone")
                        else:
                            self.change_state_to("animal_outside_trigger_zone")

                case "animal_outside_trigger_zone":
                    # check if the animal is in the trigger zone
                    if self.is_animal_in_trigger_zone():
                        self.register_event("animal_entered_trigger_zone")
                        self.change_state_to("animal_inside_trigger_zone")

                case "animal_inside_trigger_zone":
                    # check if the animal is still in the trigger zone
                    if not self.is_animal_in_trigger_zone():
                        self.register_event("animal_exited_trigger_zone")
                        self.change_state_to("animal_outside_trigger_zone")
                        continue
                    # check if the time between triggering attempts has passed
                    if (self.chrono.now() - self.triggering_time_reset).total_seconds() < self.settings.time_between_sound_triggering_attempts:
                        continue
                    # if the time has passed, decide whether to play the sound or not
                    # check if we play the looming sound
                    if random.random() < self.settings.looming_sound_probability:
                        # play the sound
                        softcode_functions.function3()
                        # register the event in the raw file
                        self.register_event("sound_played")
                        self.change_state_to("sound_triggered")
                    else:
                        self.register_event("sound_not_played")
                        # set a timer to wait before trying to trigger the sound again
                        self.triggering_time_reset = self.chrono.now()
                
                case "sound_triggered":
                    # wait for some time to let the animal escape and stuff
                    time.sleep(self.settings.time_to_wait_after_sound)
                    # finish the trial TODO: Is this enough?
                    return


    def after_trial(self):
        # write the end time of the ending state
        self.current_state[1] = self.chrono.now()
        # append the current state to the list of states visited
        self.states_visited.append(self.current_state)
        # write the states visited to the raw file
        with self.raw_session_path.open("a") as self.raw_file:
            for state in self.states_visited:
                self.raw_file.write(f"{self.current_trial};{state[0]};{state[1]};STATE_{state[2]};\n")
        # reset the list of states visited
        self.states_visited = []
        # reset the current state
        self.current_state = (np.nan, np.nan, "none")


    def close(self):
        # close the file
        self.raw_file.close()


    def change_state_to(self, new_state: str):
        # update the current state ending time
        self.current_state[1] = self.chrono.now()
        # Register the state change event
        self.register_event(f"_Transition_to_{new_state}")
        # append the current state to the list of states visited
        self.states_visited.append(self.current_state)
        # update the current state to the new state
        self.current_state = (self.chrono.now(), np.nan, new_state)
        return


    def is_animal_in_trigger_zone(self) -> bool:
        # get the animal position
        animal_position = [manager.cam.mean_x_value, manager.cam.mean_y_value]
        if animal_position is None:
            return False
        # check if the animal is in the trigger zone
        if (self.settings.trigger_zone_x[0] <= animal_position[0] <= self.settings.trigger_zone_x[1]) and \
           (self.settings.trigger_zone_y[0] <= animal_position[1] <= self.settings.trigger_zone_y[1]):
            return True
        return False


    def register_event(self, msg: str, value: float = np.nan):
        self.raw_file.write(f"{self.current_trial};{self.chrono.now()};{np.nan};{msg};{value}\n")
        return
    

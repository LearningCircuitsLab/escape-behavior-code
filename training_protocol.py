from village.custom_classes.training_protocol_base import TrainingProtocolBase


class TrainingProtocol(TrainingProtocolBase):
    """
    This class defines the training protocol for animal behavior experiments.
    The training protocol is run every time a task is finished and it determines:
    1. Which new task is scheduled for the subject
    2. How training variables change based on performance metrics

    Required methods to implement:
    - __init__: Initialize the training protocol
    - default_training_settings: Define initial parameters. It is called when creating a new subject.
    - update_training_settings: Update parameters after each session.

    Optional method:
    - gui_tabs: Organize the variables in custom GUI tabs
    """


    def __init__(self) -> None:
        """Initialize the training protocol."""
        super().__init__()


    def default_training_settings(self) -> None:
        """
        Define all initial training parameters for new subjects.

        This method is called when creating a new subject, and these parameters
        are saved as the initial values for that subject.

        Required parameters:
        - next_task (str): Name of the next task to run
        - refractory_period (int): Waiting time in seconds between sessions
        - minimum_duration (int): Minimum time in seconds for the task before door2 opens
        - maximum_duration (int): Maximum time in seconds before task stops automatically

        Additional parameters:
        You can define any additional parameters needed for your specific tasks.
        These can be modified between sessions based on subject performance.
        """

        # Required parameters for any training protocol
        self.settings.next_task = "Escape"  # Next task to run
        self.settings.refractory_period = 3600 * 4  # 4 hours between sessions of the same subject
        self.settings.minimum_duration = 1  # Minimum duration of 1 second
        self.settings.maximum_duration = 10*60*60  # Maximum duration of 10 hours

        ## Task-specific parameters

        # sound parameters
        self.settings.starting_amplitude = 0.0001  # ?? dB SPL
        self.settings.ending_amplitude = 0.2  # ~75 dB SPL
        self.settings.ramp_duration = 0.4
        self.settings.ramp_down_duration = 0.005
        self.settings.hold_duration = 0.595
        self.settings.n_repeats = 10

        # probability of looming sound being played
        self.settings.looming_sound_probability = 0.5  # 50% chance
        # grace period duration
        self.settings.grace_period = 5  # seconds
        # time to wait before deciding to trigger the sound again
        self.settings.time_between_sound_triggering_attempts = 2  # seconds
        # time to wait after sound is played before starting a new trial
        self.settings.time_to_wait_after_sound = 5  # seconds
        # trigger zone coordinates TODO
        self.settings.trigger_zone_index = 1  # index of the area in the cam_box to use as trigger zone



    def update_training_settings(self) -> None:
        pass


    def define_gui_tabs(self):
        """
        Define the organization of the settings in the GUI.

        Whatever that is not defined here will be placed in the "General" tab.
        They need to have the same name as your settings variables.
        You can use the 'Hide' tab to hide a setting from the GUI.
        Items in the lists need to have the same name as your settings variables.
        You can also restrict the possible values for each setting.
        """
        self.gui_tabs = {
            "SoundParameters": [
                "starting_amplitude",
                "ending_amplitude",
                "ramp_duration",
                "ramp_down_duration",
                "hold_duration",
                "n_repeats",
            ],
        }

        # Define possible values for each variable
        self.gui_tabs_restricted = {
            "trigger_zone_index": [0, 1, 2, 3],
        }

import numpy as np

class MessageMock():
    def __init__(self, message: str):
        self.content = message

class BpodMock():
    def __init__(self):
        self.reset_trial()
    
    def reset_trial(self):
        self.current_trial = {
            "Trial start timestamp": np.nan,
            "Events timestamps": {},
            "States timestamps": {},
        }
        self.events_occurrences = []
        return
    
    def record_message(self, message: str):
        self.events_occurrences.append(MessageMock(message))
        return
    
    def record_event(self, event_name: str, timestamp: float):
        if event_name not in self.current_trial["Events timestamps"].keys():
            self.current_trial["Events timestamps"][event_name] = [timestamp]
        else:
            self.current_trial["Events timestamps"][event_name].append(timestamp)
        return
    
    def record_state(self, state_name: str, interval: list[float]):
        if state_name not in self.current_trial["States timestamps"].keys():
            self.current_trial["States timestamps"][state_name] = [interval]
        else:
            self.current_trial["States timestamps"][state_name].append(interval)
        return
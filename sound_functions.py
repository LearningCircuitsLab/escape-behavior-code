import numpy as np
import pandas as pd
from village.settings import settings


# auditory looming sounds
def crescendo_looming_sound(
        amp_start: float,
        amp_end: float,
        ramp_duration: float = 0.4,
        ramp_down_duration: float = 0.005,
        hold_duration: float = 0.595,
        n_repeats: int = 10,
                            ) -> np.ndarray:
    # convert n_repeats to an int
    n_repeats = int(n_repeats)
    fs = settings.get("SAMPLERATE")  # Sampling frequency
    # Generate ramp + rampdown + hold for one repetition
    n_ramp = int(fs * ramp_duration)
    n_hold = int(fs * hold_duration)
    n_ramp_down = int(fs * ramp_down_duration)
    # convert amplitudes to dB
    db_start = 20 * np.log10(amp_start)
    db_end = 20 * np.log10(amp_end)
    # Linear amplitude ramp (in dB scale)
    db_ramp = np.linspace(db_start, db_end, n_ramp)
    db_ramp_down = np.linspace(db_end, db_start, n_ramp_down)
    # Convert back to amplitudes (exponential in linear scale)
    ramp_amplitudes = 10 ** (db_ramp / 20)
    ramp_down_amplitudes = 10 ** (db_ramp_down / 20)
    hold_amplitudes = np.ones(n_hold) * amp_start
    # Create one cycle of noise
    noise_ramp = np.random.randn(n_ramp) * ramp_amplitudes
    noise_hold = np.random.randn(n_hold) * hold_amplitudes
    noise_ramp_down = np.random.randn(n_ramp_down) * ramp_down_amplitudes
    cycle = np.concatenate([noise_ramp, noise_ramp_down, noise_hold])
    # Repeat 10 times
    stimulus = np.tile(cycle, n_repeats)
    # # Normalize to the 99.5th quantile to avoid clipping when saving
    # stimulus /= np.quantile(np.abs(stimulus), 0.995)

    return stimulus


def white_noise(duration: float, gain: float) -> np.ndarray:
    fs = settings.get("SAMPLERATE")  # Sampling frequency
    n_samples = int(fs * duration)
    noise = np.random.randn(n_samples) * gain
    return noise


sound_calibration_functions = [
    white_noise,
]



if __name__ == "__main__":
    loom = crescendo_looming_sound(amp_start=0.0001, amp_end=0.05, n_repeats=3)
    print(loom.shape)

    # # play it
    import time

    from village.devices.sound_device import SoundDevice

    sd = SoundDevice()

    sd.load(right=loom, left=loom)
    sd.play()

    # plot a spectrogram

    import matplotlib.pyplot as plt
    from scipy.signal import spectrogram

    f, t, Sxx = spectrogram(loom, 192000)
    plt.pcolormesh(t, f, 10 * np.log10(Sxx))
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [sec]")
    # y axis log
    plt.show()
    
    sd.close()
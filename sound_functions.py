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
    
    fs = settings.get("SAMPLERATE")  # Sampling frequency
    # Generate ramp + hold for one repetition
    n_ramp = int(fs * ramp_duration)
    n_hold = int(fs * hold_duration)
    n_ramp_down = int(fs * ramp_down_duration)
    # Linear amplitude ramp (in dB scale)
    ramp_amplitudes = np.linspace(amp_start, amp_end, n_ramp)
    hold_amplitudes = np.ones(n_hold) * amp_start
    ramp_down_amplitudes = np.linspace(amp_end, amp_start, n_ramp_down)
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


def white_noise(duration: float, amplitude: float) -> np.ndarray:
    fs = settings.get("SAMPLERATE")  # Sampling frequency
    n_samples = int(fs * duration)
    noise = np.random.randn(n_samples) * amplitude
    return noise


sound_calibration_functions = [
    white_noise,
]



if __name__ == "__main__":
    # # Define frequencies
    lowest_freq = 5000
    highest_freq = 20000
    freqs_log_spaced = np.round(np.logspace(np.log10(lowest_freq), np.log10(highest_freq), 18)).tolist()
    low_freq_list = freqs_log_spaced[:6]
    high_freq_list = freqs_log_spaced[-6:]
    # Define sound properties
    sound_properties = {
        "sample_rate": 48000,
        "duration": 1,
        "ramp_time": 0.005,
        "high_amplitude_mean": 70,
        "low_amplitude_mean": 60,
        "amplitude_std": 2,
        "high_freq_list": high_freq_list,
        "low_freq_list": low_freq_list,
        "subduration": 0.03,
        "suboverlap": 0.01,
    }


    # # Generate a cloud of tones
    cot, _, _ = cloud_of_tones(**sound_properties, high_prob=.7, low_prob=.3)
    print(cot.shape)

    # # play it
    import time

    from village.devices.sound_device import SoundDevice

    sd = SoundDevice(sound_properties["sample_rate"])

    sd.load(cot)
    sd.play()

    # time.sleep(2)

    # # # print the percentage of high and low tones
    # print("High tones: ", np.sum(frequencies[1] > 0) / len(frequencies[1]) * 100)
    # # # print all frequencies different from 0
    # # h_t = frequencies[1][frequencies[1] > 0]
    # # print(h_t)
    # print("Low tones: ", np.sum(frequencies[0] > 0) / len(frequencies[0]) * 100)
    # # l_t = frequencies[0][frequencies[0] > 0]
    # # print(l_t)

    # plot a spectrogram

    import matplotlib.pyplot as plt
    from scipy.signal import spectrogram



    f, t, Sxx = spectrogram(cot, sound_properties["sample_rate"])
    plt.pcolormesh(t, f, 10 * np.log10(Sxx))
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [sec]")
    plt.ylim(0, 20000)  # limit the y axis to 20 kHz
    # y axis log
    plt.show()
    
    sd.close()
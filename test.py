import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import hilbert
from pydub import AudioSegment

encryption_key = 0xA5
audio = AudioSegment.from_wav('sound.wav')
samples = np.array(audio.get_array_of_samples())
frequency_data = fft(samples)

magnitude = np.abs(frequency_data)  # Magnitude of the frequency components
phase = np.angle(frequency_data)    # Phase of the frequency components

for i in range(len(frequency_data)):
    if i > len(frequency_data) * 0:  # Select higher frequencies
        encrypted_phase = phase[i] + encryption_key / 100.0  # Add a small perturbation to the phase
        frequency_data[i] = magnitude[i] * np.exp(1j * encrypted_phase)  # Rebuild with encrypted phase

modified_samples = ifft(frequency_data).real

modified_audio = AudioSegment(
    data=modified_samples.astype(np.int16).tobytes(),
    sample_width=audio.sample_width,
    frame_rate=audio.frame_rate,
    channels=audio.channels
)

modified_audio.export("encrypted_audio.wav", format="wav")

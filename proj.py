import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import hilbert
from pydub import AudioSegment
import matplotlib.pyplot as plt

# Load the audio file
audio = AudioSegment.from_mp3('sound.mp3')
# Convert audio to numpy array
samples = np.array(audio.get_array_of_samples())
# Perform FFT
frequency_data = fft(samples)

# Get the number of samples
n = len(samples)
# Calculate the frequency bins
frequencies = np.fft.fftfreq(n, d=1/audio.frame_rate)

# Take the absolute value of the FFT and normalize
magnitude = np.abs(frequency_data)[:n//2]  # Take the positive half of the FFT
frequencies = frequencies[:n//2]  # Corresponding frequencies

# Normalize the magnitude for better visualization
magnitude = magnitude / np.max(magnitude)

# Plot the frequency data
plt.figure(figsize=(12, 6))
plt.plot(frequencies, magnitude)
plt.xscale('log')  # Use logarithmic scale for the x-axis
plt.xlim(20, 20000)  # Focus on audible frequencies (20 Hz to 20 kHz)
plt.title('Frequency Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Normalized Amplitude')
plt.grid(True)
plt.tight_layout()
plt.show()

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
    if i > len(frequency_data) * 0.3:  # Select higher frequencies
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
encrypted_audio = AudioSegment.from_wav('encrypted_audio.wav')
encrypted_samples = np.array(encrypted_audio.get_array_of_samples())

# Perform FFT on the encrypted samples
encrypted_frequency_data = fft(encrypted_samples)

# Extract magnitude and encrypted phase
encrypted_magnitude = np.abs(encrypted_frequency_data)
encrypted_phase = np.angle(encrypted_frequency_data)

# Decrypt the phase
for i in range(len(encrypted_frequency_data)):
    if i > len(encrypted_frequency_data) * 0.3:  # Adjust for higher frequencies
        decrypted_phase = encrypted_phase[i] - encryption_key / 100.0  # Subtract the perturbation
        encrypted_frequency_data[i] = encrypted_magnitude[i] * np.exp(1j * decrypted_phase)

# Perform IFFT to get the original signal
decrypted_samples = ifft(encrypted_frequency_data).real

# Create the decrypted audio
decrypted_audio = AudioSegment(
    data=decrypted_samples.astype(np.int16).tobytes(),
    sample_width=encrypted_audio.sample_width,
    frame_rate=encrypted_audio.frame_rate,
    channels=encrypted_audio.channels
)

# Export the decrypted audio to a file
decrypted_audio.export("decrypted_audio.wav", format="wav")

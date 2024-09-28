import numpy as np
import wave
import random

def read_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        params = wav_file.getparams()
        frames = wav_file.readframes(params.nframes)
        return frames, params

def write_wav(file_path, audio_data, params):
    with wave.open(file_path, 'wb') as wav_file:
        wav_file.setparams(params)
        wav_file.writeframes(audio_data)

def xor_encrypt_decrypt(data, key):
    return bytes([b ^ key for b in data])

rawdata, params = read_wav("sound.wav")

num_bytes_to_encrypt = len(rawdata) // 5
print("Number of bytes to encrypt:", num_bytes_to_encrypt)

positions_to_change = random.sample(range(len(rawdata)), num_bytes_to_encrypt)
print("Number of positions to change:", len(positions_to_change))

key = 0x42
encrypted_data = bytearray(rawdata)  

for i in positions_to_change:
    encrypted_data[i] = encrypted_data[i] ^ key  
write_wav("encrypted_sound.wav", bytes(encrypted_data), params)

decrypted_data = bytearray(encrypted_data)  
for i in positions_to_change:
    decrypted_data[i] = decrypted_data[i] ^ key  

write_wav("decrypted_sound.wav", bytes(decrypted_data), params)

    
'''
import numpy as np
import pywt
import wave

def read_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        params = wav_file.getparams()
        frames = wav_file.readframes(params.nframes)
        audio_data = np.frombuffer(frames, dtype=np.int16)
        return audio_data, params

def write_wav(file_path, audio_data, params):
    with wave.open(file_path, 'wb') as wav_file:
        wav_file.setparams(params)
        wav_file.writeframes(audio_data.tobytes())

def encrypt(data, key):
    return np.bitwise_xor(data, key)  # Ensure we're using numpy's bitwise_xor

def selective_encryption(audio_data, wavelet='haar'):
    # Perform DWT
    coeffs = pywt.wavedec(audio_data, wavelet)
    
    # Select high-frequency sub-bands for encryption (typically the last few)
    for i in range(1, len(coeffs)):
        coeffs[i] = encrypt(coeffs[i].astype(np.int32), 0xFF)  # Convert to int32 before XOR
    
    # Reconstruct the signal
    encrypted_audio = pywt.waverec(coeffs, wavelet)
    return np.clip(encrypted_audio, -32768, 32767).astype(np.int16)  # Clip values to int16 range

# Example usage
input_file = 'sound.wav'
output_file = 'encrypted_output.wav'

# Read WAV file
audio_data, params = read_wav(input_file)

# Perform selective encryption
encrypted_audio = selective_encryption(audio_data)

# Write the encrypted audio to a new WAV file
write_wav(output_file, encrypted_audio, params)

print("Selective encryption completed and saved to:", output_file)
'''
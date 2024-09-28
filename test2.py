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

    

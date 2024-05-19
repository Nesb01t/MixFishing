import modules.mic_device_logger as logger
import threading

# print("--- get all devices ---")
logger.get_device_info()

print("--- find mix sound device ---")
mixDevices = logger.get_mix_devices()
device_idx = -1
for device in mixDevices:
    if device['defaultSampleRate'] == 48000:
        device_idx = device['index']
        break


def record_audio(dev_idx):
    import pyaudio
    import wave
    import os

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 48000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index=dev_idx,
                        frames_per_buffer=CHUNK)

    print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("finished recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    os.system("aplay " + WAVE_OUTPUT_FILENAME)

import pyaudio

audioLib = pyaudio.PyAudio()


def get_device_info():
    for i in range(audioLib.get_device_count()):
        print(audioLib.get_device_info_by_index(i))


def get_mix_devices():
    mix_devices = []
    for i in range(audioLib.get_device_count()):
        device = audioLib.get_device_info_by_index(i)
        if "mix" in device['name'].lower():
            mix_devices.append(device)
    return mix_devices


def get_mix_device_index():
    mixDevices = get_mix_devices()
    device_idx = -1
    for device in mixDevices:
        if device['defaultSampleRate'] == 48000:
            device_idx = device['index']
            break
    return device_idx

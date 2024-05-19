import threading
import time
import pyaudio
import audioop

import win32con
import win32gui

import modules.mic_device_logger as logger
import modules.get_hwnd as gw
import modules.ingame_interact as ig

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000

# 初始化 window
hwnd = gw.get_hwnd_by_window_name("魔兽世界")

# 初始化 audio
audio = pyaudio.PyAudio()
dev_idx = logger.get_mix_device_index()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    input_device_index=dev_idx,
                    frames_per_buffer=CHUNK)

# 初始化变量
maxValue = 100
fishing = False
lastFishTime = time.time()

# 第一次放线
ig.pressKey(hwnd, ig.VK_ZERO)  # 放
time.sleep(3)
fishing = True


def checkFishing():
    global fishing
    global lastFishTime
    time.sleep(3)
    while True:
        if percent > 3 and fishing:
            fishing = False
            ig.pressKey(hwnd, ig.VK_SLASH)  # loot
            time.sleep(1)
            ig.pressKey(hwnd, ig.VK_ZERO)  # release
            lastFishTime = time.time()
            time.sleep(3)
            fishing = True
        if time.time() - lastFishTime > 20:  # dead zone checking
            ig.pressKey(hwnd, ig.VK_ZERO)
            time.sleep(3)
            lastFishTime = time.time()


threading.Thread(target=checkFishing).start()

while True:
    # get RMS
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)

    if rms > maxValue:
        maxValue = rms

    print("\033c", end="")
    print(f"Hwnd: {hwnd}")
    print(f"Max Value: {maxValue}")
    percent = rms / maxValue * 10
    print(f"Percent: {percent}")
    for i in range(10):
        if i < percent:
            print("#", end="")
        else:
            print(" ", end="")

    # end of while
    time.sleep(0.2)

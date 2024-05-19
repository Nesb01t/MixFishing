import pkg_resources
import pyaudio
import audioop
import modules.mic_device_logger as logger
import matplotlib.pyplot as plt

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000

# 初始化 audio
audio = pyaudio.PyAudio()
dev_idx = logger.get_mix_device_index()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    input_device_index=dev_idx,
                    frames_per_buffer=CHUNK)

# 创建一个新的图表窗口
plt.ion()
fig, ax = plt.subplots()

x = []
y = []

while True:
    # 计算 RMS
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)
    print(rms)

    # 添加新的数据到x和y的列表
    if len(x) == 0:
        x.append(0)
    else:
        x.append(x[-1] + 1)
    y.append(rms)

    # 清除之前的图表
    ax.clear()

    # 绘制新的图表
    ax.plot(x, y)

    # 更新图表
    plt.pause(0.1)
    plt.show()

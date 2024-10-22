import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

if __name__ == '__main__':
    # 设置采样率和时间序列
    sample_rate = 1000
    t = np.linspace(0, 1, sample_rate, endpoint=False)

    # 生成复合正弦波信号
    in_signal = np.sin(2 * np.pi * 5 * t) + np.sin(2 * np.pi * 10 * t) + np.sin(2 * np.pi * 20 * t)

    # 创建巴特沃兹低通滤波器，截止频率为 15 Hz
    b, a = signal.butter(N=4, Wn=15, btype='low', fs=sample_rate)

    # 对信号进行滤波
    out_signal = signal.lfilter(b, a, in_signal)

    # 输出滤波器系数
    print("Filter coefficients:")
    print("b:", b)
    print("a:", a)

    # 绘制输入信号和滤波后的信号
    plt.figure(figsize=(10, 4))
    plt.subplot(2, 1, 1)
    plt.plot(t, in_signal)
    plt.title('Input Signal (Composite Sine Waves)')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(t, out_signal, color='red')
    plt.title('Filtered Signal (Butterworth Low-pass)')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid()

    plt.tight_layout()
    plt.show()
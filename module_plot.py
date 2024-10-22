import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

def plot_signals(input_signal, filter_response, output_signal, sample_rate):

    # 设置中文字体
    font_path = "C:/Windows/Fonts/simsun.ttc"  # Windows中的常用字体路径
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()

    fig, axs = plt.subplots(3, 3, figsize=(15, 10))
    t = np.arange(len(input_signal)) / sample_rate
    max_time = t[-1]

    # 设置时域范围一致
    time_xlim = (-500, 500)
    time_ylim = (-500, 500)

    # 时域图
    axs[0, 0].plot(t, input_signal)
    axs[0, 0].set_title('输入信号时域图')
    axs[1, 0].plot(t, filter_response)
    axs[1, 0].set_title('滤波器冲激响应')
    axs[2, 0].plot(t, output_signal)
    axs[2, 0].set_title('输出信号时域图')

    # 频域图 (FFT)
    input_fft = np.fft.fft(input_signal)
    filter_fft = np.fft.fft(filter_response)
    output_fft = np.fft.fft(output_signal)
    freqs = np.fft.fftfreq(len(input_signal), 1/sample_rate)

    # 幅频响应
    axs[0, 1].plot(freqs[:len(freqs)//2], np.abs(input_fft)[:len(freqs)//2])
    axs[0, 1].set_title('输入信号幅频响应')
    axs[1, 1].plot(freqs[:len(freqs)//2], np.abs(filter_fft)[:len(freqs)//2])
    axs[1, 1].set_title('滤波器幅频响应')
    axs[2, 1].plot(freqs[:len(freqs)//2], np.abs(output_fft)[:len(freqs)//2])
    axs[2, 1].set_title('输出信号幅频响应')

    # 相频响应
    axs[0, 2].plot(freqs[:len(freqs)//2], np.angle(input_fft)[:len(freqs)//2])
    axs[0, 2].set_title('输入信号相频响应')
    axs[1, 2].plot(freqs[:len(freqs)//2], np.angle(filter_fft)[:len(freqs)//2])
    axs[1, 2].set_title('滤波器相频响应')
    axs[2, 2].plot(freqs[:len(freqs)//2], np.angle(output_fft)[:len(freqs)//2])
    axs[2, 2].set_title('输出信号相频响应')

    plt.tight_layout()
    return fig, axs

def generate_convolved_output(input_signal, filter_response):
    output_signal = np.convolve(input_signal, filter_response, mode='same')
    return output_signal

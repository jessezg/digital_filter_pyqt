import numpy as np
import matplotlib.pyplot as plt

def plot_signals(input_signal, filter_response, output_signal, sample_rate):
    fig, axs = plt.subplots(3, 3, figsize=(15, 10))

    # 时间轴
    t = np.arange(len(input_signal)) / sample_rate

    # 时域图
    axs[0, 0].plot(t, input_signal)
    axs[0, 0].set_title('输入信号时域图')
    axs[1, 0].plot(t, filter_response)
    axs[1, 0].set_title('滤波器时域响应')
    axs[2, 0].plot(t, output_signal)
    axs[2, 0].set_title('输出信号时域图')

    # 计算幅频响应和相频响应 (FFT)
    input_fft = np.fft.fft(input_signal)
    filter_fft = np.fft.fft(filter_response)
    output_fft = np.fft.fft(output_signal)
    freqs = np.fft.fftfreq(len(input_signal), 1/sample_rate)

    # 幅频响应
    axs[0, 1].plot(freqs, np.abs(input_fft))
    axs[0, 1].set_title('输入信号幅频响应')
    axs[1, 1].plot(freqs, np.abs(filter_fft))
    axs[1, 1].set_title('滤波器幅频响应')
    axs[2, 1].plot(freqs, np.abs(output_fft))
    axs[2, 1].set_title('输出信号幅频响应')

    # 相频响应
    axs[0, 2].plot(freqs, np.angle(input_fft))
    axs[0, 2].set_title('输入信号相频响应')
    axs[1, 2].plot(freqs, np.angle(filter_fft))
    axs[1, 2].set_title('滤波器相频响应')
    axs[2, 2].plot(freqs, np.angle(output_fft))
    axs[2, 2].set_title('输出信号相频响应')

    # 调整布局
    plt.tight_layout()
    plt.show()

def generate_convolved_output(input_signal, filter_response):
    # 使用卷积计算输出信号
    output_signal = np.convolve(input_signal, filter_response, mode='same')
    return output_signal

def apply_filter(input_signal, filter_type, filter_params, sample_rate):
    # 根据滤波器类型和参数生成滤波器响应
    if filter_type == 'Butterworth':
        from scipy.signal import butter, lfilter
        b, a = butter(filter_params['order'], filter_params['cutoff'], btype=filter_params['type'], fs=sample_rate)
        filter_response = lfilter(b, a, [1] * len(input_signal))  # 获取滤波器响应
    elif filter_type == 'Chebyshev':
        from scipy.signal import cheby1, lfilter
        b, a = cheby1(filter_params['order'], filter_params['ripple'], filter_params['cutoff'], btype=filter_params['type'], fs=sample_rate)
        filter_response = lfilter(b, a, [1] * len(input_signal))
    # 添加其他滤波器类型
    else:
        raise ValueError("未知滤波器类型")
    
    return filter_response

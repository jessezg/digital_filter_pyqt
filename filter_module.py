from scipy import signal

def apply_filter(signals):
    # 假设一个低通滤波器为例
    b, a = signal.butter(3, 0.05)
    filtered_signals = {name: signal.filtfilt(b, a, s) for name, s in signals.items()}
    return filtered_signals

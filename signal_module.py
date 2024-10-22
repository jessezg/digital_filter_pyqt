import numpy as np
from scipy import signal

def generate_signals(entries):
    t = np.linspace(0, 1, 1000)
    combined_signal = np.zeros_like(t)
    
    for signal_type, amplitude, frequency in entries:
        if signal_type == '正弦波':
            combined_signal += amplitude * np.sin(2 * np.pi * frequency * t)
        elif signal_type == '方波':
            combined_signal += amplitude * signal.square(2 * np.pi * frequency * t)
        elif signal_type == '三角波':
            combined_signal += amplitude * signal.sawtooth(2 * np.pi * frequency * t, 0.5)
        elif signal_type == '锯齿波':
            combined_signal += amplitude * signal.sawtooth(2 * np.pi * frequency * t)
        elif signal_type == '白噪声':
            combined_signal += amplitude * np.random.normal(0, 1, t.shape)
        elif signal_type == '高斯噪声':
            combined_signal += amplitude * np.random.normal(0, 0.5, t.shape)
        elif signal_type == '脉冲噪声':
            combined_signal += amplitude * np.random.poisson(1, t.shape)
    
    return combined_signal

import numpy as np
from scipy import signal

def generate_signals(entries, sample_rate=1000):
    t = np.linspace(0, 1, sample_rate)
    combined_signal = np.zeros_like(t)
    
    for entry in entries:
        signal_type = entry['type']
        params = entry['params']
        amplitude = params['amplitude']
        if signal_type == '正弦波':
            period = params['period']
            phase = params['phase']
            combined_signal += amplitude * np.sin(2 * np.pi / period * t + phase)
        elif signal_type == '方波':
            period = params['period']
            duty = params['duty']
            combined_signal += amplitude * signal.square(2 * np.pi / period * t, duty)
        elif signal_type == '三角波':
            period = params['period']
            combined_signal += amplitude * signal.sawtooth(2 * np.pi / period * t, 0.5)
        elif signal_type == '锯齿波':
            period = params['period']
            combined_signal += amplitude * signal.sawtooth(2 * np.pi / period * t)
        elif signal_type == '白噪声':
            mean = params['mean']
            stddev = params['stddev']
            combined_signal += amplitude * np.random.normal(mean, stddev, t.shape)
        elif signal_type == '高斯噪声':
            mean = params['mean']
            stddev = params['stddev']
            combined_signal += amplitude * np.random.normal(mean, stddev, t.shape)
        elif signal_type == '脉冲噪声':
            rate = params['rate']
            combined_signal += amplitude * np.random.poisson(rate, t.shape)
        elif signal_type == '直流':
            dc_value = params['dc_value']
            combined_signal += dc_value * np.ones_like(t)

    return combined_signal

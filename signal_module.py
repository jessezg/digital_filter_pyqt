import numpy as np
from scipy import signal

def generate_signals():
    t = np.linspace(0, 1, 1000)
    signals = {
        'sin': np.sin(2 * np.pi * 10 * t),
        'square': signal.square(2 * np.pi * 10 * t),
        'triangle': signal.sawtooth(2 * np.pi * 10 * t, 0.5),
        'sawtooth': signal.sawtooth(2 * np.pi * 10 * t),
        'white_noise': np.random.normal(0, 1, t.shape),
        'gaussian_noise': np.random.normal(0, 0.5, t.shape),
        'pulse_noise': np.random.poisson(1, t.shape)
    }
    return signals

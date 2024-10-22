from scipy import signal

def apply_filter(signal, filter_type, params):
    if filter_type == '低通滤波器':
        b, a = signal.butter(params['order'], params['cutoff'], btype='low')
    elif filter_type == '高通滤波器':
        b, a = signal.butter(params['order'], params['cutoff'], btype='high')
    elif filter_type == '带通滤波器':
        b, a = signal.butter(params['order'], [params['low_cut'], params['high_cut']], btype='band')
    elif filter_type == '带阻滤波器':
        b, a = signal.butter(params['order'], [params['low_cut'], params['high_cut']], btype='bandstop')
    elif filter_type == '巴特沃兹滤波器':
        b, a = signal.butter(params['order'], params['cutoff'], btype='low')
    elif filter_type == '切比雪夫滤波器':
        b, a = signal.cheby1(params['order'], params['ripple'], params['cutoff'])
    
    filtered_signal = signal.filtfilt(b, a, signal)
    return filtered_signal

from scipy import signal
import numpy as np

def apply_filter(input_signal, filter_info, sample_rate):
    filter_type = filter_info['type']
    params = filter_info['params']
    
    if '巴特沃兹' in filter_type:
        b, a = signal.butter(params['order'], 
                             [params['low_cut'], params['high_cut']] if '带' in filter_type else params['cutoff'], 
                             btype='band' if '带通' in filter_type else 'bandstop' if '带阻' in filter_type else 'low' if '低通' in filter_type else 'high', 
                             fs=sample_rate)
    elif '切比雪夫1型' in filter_type:
        b, a = signal.cheby1(params['order'], params['ripple'], 
                             [params['low_cut'], params['high_cut']] if '带' in filter_type else params['cutoff'], 
                             btype='band' if '带通' in filter_type else 'bandstop' if '带阻' in filter_type else 'low' if '低通' in filter_type else 'high', 
                             fs=sample_rate)
    elif '切比雪夫2型' in filter_type:
        b, a = signal.cheby2(params['order'], params['ripple'], 
                             [params['low_cut'], params['high_cut']] if '带' in filter_type else params['cutoff'], 
                             btype='band' if '带通' in filter_type else 'bandstop' if '带阻' in filter_type else 'low' if '低通' in filter_type else 'high', 
                             fs=sample_rate)
    else:
        raise ValueError(f"未知滤波器类型: {filter_type}")

    filtered_signal = signal.lfilter(b, a, input_signal)
    return filtered_signal

def filter_func(filter_info, sample_rate):
    filter_type = filter_info['type']
    params = filter_info['params']
    
    if '巴特沃兹' in filter_type:
        b, a = signal.butter(params['order'], 
                             [params['low_cut'], params['high_cut']] if '带' in filter_type else params['cutoff'], 
                             btype='band' if '带通' in filter_type else 'bandstop' if '带阻' in filter_type else 'low' if '低通' in filter_type else 'high', 
                             fs=sample_rate)
    elif '切比雪夫1型' in filter_type:
        b, a = signal.cheby1(params['order'], params['ripple'], 
                             [params['low_cut'], params['high_cut']] if '带' in filter_type else params['cutoff'], 
                             btype='band' if '带通' in filter_type else 'bandstop' if '带阻' in filter_type else 'low' if '低通' in filter_type else 'high', 
                             fs=sample_rate)
    elif '切比雪夫2型' in filter_type:
        b, a = signal.cheby2(params['order'], params['ripple'], 
                             [params['low_cut'], params['high_cut']] if '带' in filter_type else params['cutoff'], 
                             btype='band' if '带通' in filter_type else 'bandstop' if '带阻' in filter_type else 'low' if '低通' in filter_type else 'high', 
                             fs=sample_rate)
    else:
        raise ValueError(f"未知滤波器类型: {filter_type}")

    # 创建一个单位脉冲序列，长度为 100
    impulse = np.zeros(1000)
    impulse[0] = 1

    # 使用 lfilter 函数计算滤波器的时域响应
    response = signal.lfilter(b, a, impulse)
    return response
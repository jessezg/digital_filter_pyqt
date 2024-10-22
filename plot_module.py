import matplotlib.pyplot as plt

def plot_signals(original_signals, filtered_signals):
    fig, axs = plt.subplots(3, 3, figsize=(12, 9))

    # 绘制原始信号和滤波后的信号
    for i, (name, signal) in enumerate(original_signals.items()):
        axs[i, 0].plot(signal)
        axs[i, 0].set_title(f"原始信号: {name}")

        filtered_signal = filtered_signals[name]
        axs[i, 1].plot(filtered_signal)
        axs[i, 1].set_title(f"滤波后信号: {name}")

    plt.tight_layout()
    plt.show()

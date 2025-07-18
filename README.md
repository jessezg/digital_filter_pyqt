# 信号滤波器分析与可视化程序

## 简介

本程序是一个基于 Python 的信号生成、滤波和可视化工具，适用于信号处理的教学、研究与工程应用。用户可以通过简单的图形界面，生成多种信号，选择不同滤波器，并观察滤波效果。

---

## 功能

### 1. 信号生成
- 支持多种类型信号：
  - 正弦波
  - 方波
  - 三角波
  - 锯齿波
  - 白噪声
  - 高斯噪声
  - 脉冲噪声
  - 直流信号
- 参数化设置：用户可以自由设置信号的幅值、频率、相位、均值等。

### 2. 滤波器设计
- 提供以下滤波器：
  - 巴特沃兹滤波器（低通、高通、带通、带阻）
  - 切比雪夫1型滤波器（低通、高通、带通、带阻）
  - 切比雪夫2型滤波器（低通、高通、带通、带阻）
- 滤波器参数设置：
  - 阶数
  - 截止频率
  - 纹波大小（适用于切比雪夫滤波器）
  - 带通/带阻的频率范围

### 3. 信号分析
- 可视化分析包括：
  - 输入信号的时域图与频谱图
  - 滤波器的冲激响应和幅频响应
  - 滤波后输出信号的时域图与频谱图

### 4. 用户界面
- 欢迎界面：概述程序功能，引导用户操作。
- 信号选择界面：添加/删除信号，设置信号参数。
- 滤波器选择界面：选择滤波器类型并设置参数。
- 结果展示界面：显示信号与滤波效果，支持详细分析。

### 5. 异常处理
- 捕获程序运行中发生的所有未处理异常，并弹窗提示错误信息。
- 避免程序崩溃，保证用户体验流畅。

---

## 安装与运行

### 环境要求
- Python 3.7 或以上
- 必要依赖：
  - `PyQt5`
  - `scipy`
  - `numpy`
  - `matplotlib`


### 使用说明

1. 启动程序后，进入欢迎界面，点击 "下一步" 开始。
2. 在信号选择界面：
   - 添加信号并设置参数。
   - 可添加多个信号，信号将叠加生成。
3. 在滤波器选择界面：
   - 选择滤波器类型并设置参数。
   - 根据选择的滤波器类型，动态调整参数输入框。
4. 点击 "下一步"，进入结果展示界面：
   - 观察输入信号、滤波器响应和输出信号的时域与频谱。
   - 如果参数异常（如截止频率设置错误），程序会弹窗提示。
5. 点击 "完成" 结束程序。

---

## 测试用例

1. **信号选择界面**

   信号1：正弦信号      幅值：5    频率：200Hz  相位：0；

   信号2：正弦信号      幅值：5    频率：300Hz  相位：0；

   信号3：正弦信号      幅值：5    频率：400Hz  相位：0；

   信号4：白噪声信号    幅值：0.1  均值：0      标准差：0；

2. **滤波器选择界面**
   
   切比雪夫一型带通

   阶数：10

   下截止频率：290.00
   
   上截止频率：310.00

   波纹：0.01
---

## 常见问题

1. **程序卡住或崩溃**
   - 请根据提示检查输入参数是否正确（如滤波器阶数是否过高、截止频率范围是否合理）。

2. **显示乱码或字体错误**
   - 请确保系统中安装了中文字体或对应的字体。
---

## 开发者

作者：太原理工大学 智能测控工程专业 郑健鑫

邮箱：z12502793@163.com

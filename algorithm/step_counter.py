# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/7
# @Author  : Huatao
# @Email   : 735820057@qq.com
# @File    : 
# @Description :
import numpy as np
from scipy import signal

from scipy.interpolate import interp1d


def resample_data(data, target_rate):
    """
    Resamples the input data to the specified target sampling rate.

    Parameters:
        data (numpy.ndarray): Input data as an N*4 array. The first column contains timestamps in milliseconds,
                              and the remaining columns contain sensor data.
        target_rate (float): Target sampling rate in Hz.

    Returns:
        numpy.ndarray: Resampled data as an array with the same structure (timestamps and sensor data).
    """
    # Extract timestamps and sensor data
    timestamps = data[:, 0]
    sensor_data = data[:, 1:]

    # Convert timestamps to seconds (relative time)
    timestamps = (timestamps - timestamps[0]) / 1000.0

    # Generate new timestamps for the target sampling rate
    new_timestamps = np.arange(timestamps[0], timestamps[-1], 1 / target_rate)

    # Perform interpolation for each column of sensor data
    interpolated_data = np.zeros((len(new_timestamps), sensor_data.shape[1]))
    for i in range(sensor_data.shape[1]):
        interpolator = interp1d(timestamps, sensor_data[:, i], kind='linear', fill_value="extrapolate")
        interpolated_data[:, i] = interpolator(new_timestamps)

    # Combine new timestamps (converted back to milliseconds) and interpolated data
    resampled_data = np.column_stack((new_timestamps * 1000, interpolated_data))

    return resampled_data


def step_pick(signals, thre=0.3):
    sm1 = signals - np.roll(signals, -1)
    sm1[-1] = 0.0
    sm2 = signals - np.roll(signals, 1)
    sm2[0] = 0.0
    peaks = (signals > thre) & (sm1 > 0) & (sm2 > 0)
    return peaks


def step_detect(acce, filter_frequency=2.0, fs=None, fs_default=30, count=True):
    if acce.size == 0:
        return None
    if fs is None:
        acc = resample_data(acce, fs_default)[:, 1:]
        fs = fs_default
    else:
        acc = acce[:, 1:]
    def filter(signals):
        sos = signal.butter(2, filter_frequency, btype='lowpass', output='sos', fs=fs)  # [0.1, 0.9]
        return signal.sosfilt(sos, signals)

    acce_processed = np.linalg.norm(acc, axis=1)
    acce_processed -= np.mean(acce_processed)
    acce_filtered = filter(acce_processed)
    # plot_sensor_peaks(acce_filtered)
    peaks = step_pick(acce_filtered, thre=0.3)
    if count:
        return np.sum(peaks)
    return peaks


def step_counter(data):
    """
    A simple step counter algorithm based on accelerometer data.
    Input:
        data: N*4 numpy array, where each row contains [timestamp, acc_x, acc_y, acc_z]
    Output:
        Step count
    """
    # Check if the input data is empty
    if data.size == 0:
        return 0

    # Check if the input data has the correct shape (N*4)
    if data.shape[1] != 4:
        raise ValueError("Input data must have 4 columns: [timestamp, acc_x, acc_y, acc_z]")

    # Compute the magnitude of acceleration
    acc_magnitude = np.sqrt(data[:, 1]**2 + data[:, 2]**2 + data[:, 3]**2)

    # Calculate the mean using a sliding window and center the data
    window_size = 5  # Sliding window size, adjustable
    acc_mean = np.convolve(acc_magnitude, np.ones(window_size)/window_size, mode='valid')
    acc_centered = acc_magnitude[len(acc_magnitude)-len(acc_mean):] - acc_mean

    # Peak detection (steps) with time consideration
    threshold = 0.2  # Peak detection threshold, adjustable
    min_step_interval = 300  # Minimum time between steps in milliseconds, adjustable
    steps = 0
    last_step_time = None

    for i in range(1, len(acc_centered) - 1):
        if acc_centered[i] > threshold and acc_centered[i] > acc_centered[i - 1] and acc_centered[i] > acc_centered[i + 1]:
            current_time = data[i, 0]
            if last_step_time is None or (current_time - last_step_time) > min_step_interval:
                steps += 1
                last_step_time = current_time

    return steps


if __name__ == "__main__":

    acc = np.loadtxt('Accelerometer.csv', delimiter=",", dtype=float)
    # acc_resample = resample_data(acc, 20)
    # print(step_counter(acc_resample))
    print(step_detect(acc))
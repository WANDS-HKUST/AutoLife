#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/8/2023
# @Author  : Huatao
# @Email   : 735820057@qq.com
# @File    : sensortool.py
# @Description :
import os
from io import StringIO
import numpy as np
from dataclasses import dataclass
import pandas as pd
from typing import Dict, Union, List
from scipy.io import wavfile


def is_file_empty(file_path):
    """
    Check if a file is empty by verifying its size.

    Parameters:
    file_path (str): The path to the file to check.

    Returns:
    bool: True if the file is empty, False otherwise.
    """
    # Check if the file exists to avoid FileNotFoundError
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return True  # or False, depending on how you want to treat non-existent files

    # Get the size of the file
    return os.path.getsize(file_path) == 0

@dataclass
class Experiment:
    name: str
    accelerometer: np.ndarray
    location: np.ndarray
    gyroscope: np.ndarray
    step_counter: np.ndarray
    game_rotation: np.ndarray
    cellular: np.ndarray
    satellite: np.ndarray
    magnetometer: np.ndarray
    wifi: np.ndarray
    gravity: np.ndarray
    label: np.ndarray
    linear_accelerometer: np.ndarray
    audio: np.ndarray
    bluetooth: np.ndarray
    rotation: np.ndarray
    proximity: np.ndarray
    light: np.ndarray
    pressure: np.ndarray

    @staticmethod
    def read_from_file(file_path, fix=False):
        if is_file_empty(file_path):
            return np.array([])
        else:
            if fix:
                fixed_lines = []
                with open(file_path, "r", encoding="utf-8") as file:
                    for line in file:
                        if line.count('"') % 2 != 0:
                            line = line.replace('"', '')
                        fixed_lines.append(line.strip())
                fixed_data = "\n".join(fixed_lines)
                return pd.read_csv(StringIO(fixed_data), header=None).values
            return pd.read_csv(file_path, header=None).values

    @staticmethod
    def from_directory(dir_path: str, name: str, read_audio=False) -> 'Experiment':
        # Loading CSVs
        accelerometer = Experiment.read_from_file(os.path.join(dir_path, 'Accelerometer.csv'))
        location = Experiment.read_from_file(os.path.join(dir_path, 'Location.csv'))
        gyroscope = Experiment.read_from_file(os.path.join(dir_path, 'Gyroscope.csv'))
        step_counter = Experiment.read_from_file(os.path.join(dir_path, 'Step_Counter.csv'))
        game_rotation = Experiment.read_from_file(os.path.join(dir_path, 'Game_Rotation.csv'))
        cellular = Experiment.read_from_file(os.path.join(dir_path, 'Cellular.csv'))
        satellite = Experiment.read_from_file(os.path.join(dir_path, 'Satellite.csv'))
        magnetometer = Experiment.read_from_file(os.path.join(dir_path, 'Magnetometer.csv'))
        wifi = Experiment.read_from_file(os.path.join(dir_path, 'WiFi.csv'), True)
        gravity = Experiment.read_from_file(os.path.join(dir_path, 'Gravity.csv'))
        label = Experiment.read_from_file(os.path.join(dir_path, 'Label.csv'))
        linear_accelerometer = Experiment.read_from_file(os.path.join(dir_path, 'Linear_Accelerometer.csv'))
        bluetooth = Experiment.read_from_file(os.path.join(dir_path, 'Bluetooth.csv'), True)
        rotation = Experiment.read_from_file(os.path.join(dir_path, 'Rotation.csv'))
        proximity = Experiment.read_from_file(os.path.join(dir_path, 'Proximity.csv'))
        light = Experiment.read_from_file(os.path.join(dir_path, 'Light.csv'))
        pressure = Experiment.read_from_file(os.path.join(dir_path, 'Pressure.csv'))


        # Loading Audio
        if read_audio:
            sample_rate, audio = wavfile.read(os.path.join(dir_path, 'Audio.wav'))
        else:
            audio = None

        if label.size == 0:
            return None

        return Experiment(
            name=name,
            accelerometer=accelerometer,
            location=location,
            gyroscope=gyroscope,
            step_counter=step_counter,
            game_rotation=game_rotation,
            cellular=cellular,
            satellite=satellite,
            magnetometer=magnetometer,
            wifi=wifi,
            gravity=gravity,
            label=label,
            linear_accelerometer=linear_accelerometer,
            audio=audio,
            bluetooth=bluetooth,
            rotation=rotation,
            proximity=proximity,
            light=light,
            pressure=pressure
        )

    @staticmethod
    def from_directories(parent_directory: str) -> List['Experiment']:
        experiments = []
        print("Loading dataset {%s}." % parent_directory)
        # Iterate over all subdirectories in the provided directory
        for subdir in os.listdir(parent_directory):
            if 'pycache' in subdir:
                continue
            subdir_path = os.path.join(parent_directory, subdir)
            if os.path.isdir(subdir_path):
                experiment = Experiment.from_directory(subdir_path, subdir)
                if experiment is not None:
                    experiments.append(experiment)
        experiments.sort(key=lambda exp: exp.label[0, 0])
        return experiments

    def get_time_range(self):
        return self.label[0, 0], self.label[-1, 0]

    def filter_by_timestamp(self, start_timestamp: int, end_timestamp: int) -> 'Experiment':
        # Helper function to filter data based on timestamp
        def filter_data(data: np.ndarray) -> np.ndarray:
            if data.size == 0:
                return data
            return data[(data[:, 0] >= start_timestamp) & (data[:, 0] <= end_timestamp)]

        return Experiment(
            name=self.name,
            accelerometer=filter_data(self.accelerometer),
            location=filter_data(self.location),
            gyroscope=filter_data(self.gyroscope),
            step_counter=filter_data(self.step_counter),
            game_rotation=filter_data(self.game_rotation),
            cellular=filter_data(self.cellular),
            satellite=filter_data(self.satellite),
            magnetometer=filter_data(self.magnetometer),
            wifi=filter_data(self.wifi),
            gravity=filter_data(self.gravity),
            label=filter_data(self.label),
            linear_accelerometer=filter_data(self.linear_accelerometer),
            audio=self.audio,  # Audio remains unchanged
            bluetooth=filter_data(self.bluetooth),
            rotation=filter_data(self.rotation),
            proximity=filter_data(self.proximity),
            light=filter_data(self.light),
            pressure=filter_data(self.pressure)
        )

    @staticmethod
    def format_simple_sensor(data: np.ndarray) -> Dict[str, Union[int, float]]:
        if data.size == 2: # step counter
            return {
                "timestamp": data[0],
                "value": data[1],
            }
        elif data.size > 4: # rotation, game_rotation
            return {
                "timestamp": data[0],
                "w": data[1],
                "x": data[2],
                "y": data[3],
                "z": data[4]
            }
        else: # accelerometer, linear_accelerometer, gyroscope, magnetometer, gravity
            return {
                "timestamp": data[0],
                "x": data[1],
                "y": data[2],
                "z": data[3]
            }

    @staticmethod
    def format_location(data: np.ndarray) -> Dict[str, Union[int, float, str]]:
        return {
            "timestamp": data[0],
            "category": data[1],
            "signal_timestamp": data[2],
            "provider": data[3],
            "longitude": data[4],
            "latitude": data[5],
            "altitude": data[6],
            "speed": data[7],
            "accuracy": data[8],
            "bearing": data[9]
        }

    @staticmethod
    def format_bluetooth(data: np.ndarray) -> Dict[str, Union[int, float, str]]:
        return {
            "timestamp": data[0],
            "device_name": str(data[1]).replace('nan', '').replace('null', ''),
            "address": data[2],
            "rssi": data[3],
            "uuids_string": data[4],
            "type": data[5],
            "bond_state": data[6]
        }

    @staticmethod
    def format_cellular(data: np.ndarray) -> Dict[str, Union[int, float, str]]:
        return {
            "timestamp": data[0],
            "type": data[1],
            "connected_signal_level": data[2],
            "size": data[3],
            "protocol": data[4],
            "time": data[5],
            "identity": data[6],
            "RSCP": data[7],
            "isRegistered": data[8]
        }

    @staticmethod
    def format_satellite(data: np.ndarray) -> Dict[str, Union[int, float, str]]:
        return {
            "timestamp": data[0],
            "count": data[1],
            "prn": data[2],
            "used_in_fix": data[3],
            "snr": data[4],
            "constellation_type": data[5],
            "azimuth": data[6],
            "elevation": data[7]
        }

    @staticmethod
    def format_wifi(data: np.ndarray) -> Dict[str, Union[int, float, str]]:
        return {
            "timestamp": data[0],
            "count": data[1],
            "signal_timestamp": data[2],
            "ssid": data[3],
            "bssid": data[4],
            "frequency": data[5],
            "rssi": data[6]
        }

    @staticmethod
    def format_label(data: np.ndarray) -> Dict[str, Union[int, float, str]]:
        return {
            "timestamp": data[0],
            "label_motion": data[1],
            "label_transportation": data[2],
            "label_environment": data[3],
        }


# Load data into the Experiment class
# subdir_path = r'data/j240322'
# experiment_data = Experiment.from_directory(subdir_path)
# acce = Experiment.format_simple_sensor(experiment_data.accelerometer[0])
# gyro = Experiment.format_simple_sensor(experiment_data.gyroscope[0])
# magn = Experiment.format_simple_sensor(experiment_data.magnetometer[0])
# grav = Experiment.format_simple_sensor(experiment_data.gravity[0])
# rota = Experiment.format_simple_sensor(experiment_data.rotation[0])
# grot = Experiment.format_simple_sensor(experiment_data.game_rotation[0])
# # step = Experiment.format_simple_sensor(experiment_data.step_counter[0])
# pressure = Experiment.format_simple_sensor(experiment_data.pressure[0])
# light = Experiment.format_simple_sensor(experiment_data.light[0])
# # proximity = Experiment.format_simple_sensor(experiment_data.proximity[0])
#
# sate = Experiment.format_satellite(experiment_data.satellite[0])
# wifi = Experiment.format_wifi(experiment_data.wifi[0])
# blue = Experiment.format_bluetooth(experiment_data.bluetooth[0])
# loca = Experiment.format_location(experiment_data.location[0])
# cell = Experiment.format_cellular(experiment_data.cellular[0])
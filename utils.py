# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/2/2
# @Author  : Huatao
# @Email   : 735820057@qq.com
# @File    : utils.py
# @Description :
import argparse
import json
import os
import random
import copy
from abc import abstractmethod
from collections import Counter

import numpy as np
import yaml


def set_seeds(seed):
    "set random seeds"
    random.seed(seed)
    np.random.seed(seed)


def find_mode(data):
    counter = Counter(data)
    max_count = max(counter.values())
    mode = [k for k, v in counter.items() if v == max_count]
    return mode[0]


def log_append(log, key, content):
    if len(log) > 0:
        log += '\n'
    log += "[[%s]]:{{%s}}\n------------------------------------" % (key, content)
    return log


class Printer:

    def __init__(self):
        self.info_list = []

    def print(self, info, p=True):
        if p: print(info)
        self.info_list.append(info)

    def save(self, saved_path):
        with open(saved_path + '.txt', 'w', encoding='utf-8') as file:
            # iterate over each log in the log list
            for info in self.info_list:
                # write each log to a new line in the file
                file.write(info + '\n')
        print('Print info saved at %s' % saved_path)
        self.info_list.clear()


def save_journal(folder_path, file_name, journal, replace=True):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
    full_path = os.path.join(folder_path, file_name + '.txt')
    if replace or not os.path.exists(full_path):
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(journal)


def remove_nan_rows(arr):
    # Use boolean indexing to select only rows without NaN values
    if len(arr) == 0:
        return arr
    clean_arr = arr[~np.isnan(arr).any(axis=1)]
    return clean_arr


def clean_sensor_data(sensor_data):
    sensor_data_clean = remove_nan_rows(sensor_data)
    if sensor_data_clean.size == 0:
        return None
    return sensor_data_clean
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/8/2025
# @Author  : Huatao
# @Email   : 735820057@qq.com
# @File    : life_journaling_template.py
# @Description :
import datetime
import os
import re
import pytz

from algorithm.motion_detection import detect_motion_rule, step_detect
from sensortool import Experiment
import numpy as np
import argparse
from utils import set_seeds, Printer, log_append, find_mode, save_journal, clean_sensor_data


def format_timestamp(timestamp_milliseconds):
    timestamp_seconds = timestamp_milliseconds / 1000

    # Convert to datetime object
    datetime_obj = datetime.datetime.fromtimestamp(timestamp_seconds, tz=pytz.utc)

    # Convert to UTC+8 timezone
    datetime_utc8 = datetime_obj.astimezone(pytz.timezone('Asia/Hong_Kong'))

    # Convert to string format
    date_string = datetime_utc8.strftime('%Y-%m-%d')
    time_string = datetime_utc8.strftime('%H:%M:%S')
    day_string = datetime_utc8.strftime('%A')
    return date_string, time_string, day_string


def format_number(value, decimal=0):
    if value is None:
        return 'None'
    if decimal == 0:
        return str(int(round(value)))
    else:
        format_str = '{:.{}f}'.format(value, decimal)
        return format_str


def duration_in_seconds(timestamp1, timestamp2):
    # Convert milliseconds to seconds
    timestamp1_seconds = timestamp1 / 1000
    timestamp2_seconds = timestamp2 / 1000

    # Calculate duration
    duration = abs(timestamp2_seconds - timestamp1_seconds)
    return duration


def preprocess_linear_accelerometer(linear_acce):
    linear_acce = clean_sensor_data(linear_acce)
    if linear_acce is None:
        return None, None
    linear_acce_data = linear_acce[:, 1:]
    norm_linear_acce = np.linalg.norm(linear_acce_data, axis=-1)
    mean_amplitude = np.mean(norm_linear_acce)
    standard_deviation = np.std(norm_linear_acce)
    return mean_amplitude, standard_deviation


def preprocess_step_counter(step_counter, time_duration, acce_backup):
    step_counter = clean_sensor_data(step_counter)
    if step_counter is None:
        return step_detect(acce_backup)
    step_counter_formatted = [Experiment.format_simple_sensor(sc) for sc in step_counter]
    step_count = step_counter_formatted[-1]['value'] - step_counter_formatted[0]['value']
    return step_count / time_duration * 60


def preprocess_pressure(pressure, time_duration=None, sea_level_pressure=1013.25, return_altitude=False):
    pressure = clean_sensor_data(pressure)
    if pressure is None:
        return None
    pressure_formatted = [Experiment.format_simple_sensor(p) for p in pressure]
    if len(pressure_formatted) > 0:
        pressure_values = np.array([item['value'] for item in pressure_formatted])
        altitudes = 44330 * (1 - (pressure_values / sea_level_pressure) ** (1 / 5.255))
    else:
        altitudes = np.array([0.0])
    if return_altitude:
        return altitudes[-1]
    if time_duration is None:
        return altitudes[-1] - altitudes[0]
    else:
        return (altitudes[-1] - altitudes[0]) / time_duration


def preprocess_light(light):
    light = clean_sensor_data(light)
    if light is None:
        return None
    light_formatted = [Experiment.format_simple_sensor(l) for l in light]
    lights = [l['value'] for l in light_formatted]
    return format_number(np.mean(lights))


def filter_locations(data, target_types, time_shift=[15, 30]):
    min_time = data[0, 0]
    max_time = data[-1, 0]

    time_lower_bound = min_time - time_shift[0] * 1000
    time_upper_bound = max_time + time_shift[1] * 1000

    filtered_data = data[
        (data[:, 2] >= time_lower_bound) & (data[:, 2] <= time_upper_bound) & np.isin(data[:, 1], target_types)]

    if filtered_data.size == 0:
        return None

    return filtered_data


def preprocess_location(locations, time_duration=None, transformer=None):
    if locations.size == 0:
        return None, None, None, None, None
    location_filtered = filter_locations(locations, [2, 3]) # Google fused location API
    if location_filtered is None:
        location_filtered = filter_locations(locations, [1]) # Android locationManager.requestLocationUpdates API
    if location_filtered is None:
        return None, None, None, None, None
    location_formatted = [Experiment.format_location(l) for l in location_filtered]
    latitude = location_formatted[-1]['latitude']
    longitude = location_formatted[-1]['longitude']
    if transformer is not None:
        latitude, longitude = transformer.transform(latitude, longitude)
    speed = location_formatted[-1]['speed']
    accuracy = location_formatted[-1]['accuracy']
    if len(location_formatted) > 0:
        altitudes = np.array([l['altitude'] for l in location_formatted])
    else:
        altitudes = np.array([0.0])
    if time_duration is None:
        return latitude, longitude, accuracy, speed, altitudes[-1] - altitudes[0]
    else:
        return latitude, longitude, accuracy, speed, (altitudes[-1] - altitudes[0]) / time_duration


def preprocess_satellite(satellite):
    if satellite.size == 0:
        return None, None, None, None
    satellite_format = [Experiment.format_satellite(sate) for sate in satellite]
    # counts_unique = np.unique(np.array(counts))
    # counts_unique_mean = np.mean(counts_unique)
    sate_count_latest = satellite_format[-1]['count']
    satellite_format_latest = []
    for sate in satellite_format[::-1]:
        if sate['count'] != sate_count_latest or len(satellite_format_latest) == sate_count_latest: break
        satellite_format_latest.append(sate)
    satellite_nonzero_snr_list = [sat for sat in satellite_format_latest if sat['snr'] != 0.0]
    if len(satellite_nonzero_snr_list) == 0:
        return 0, None, None, None
    snr_nonzero_mean_list = [sat['snr'] for sat in satellite_nonzero_snr_list]
    azimuth_nonzero_list = [sat['azimuth'] for sat in satellite_nonzero_snr_list]
    elevation_nonzero_list = [sat['elevation'] for sat in satellite_nonzero_snr_list]
    return len(snr_nonzero_mean_list), np.mean(snr_nonzero_mean_list), azimuth_nonzero_list, elevation_nonzero_list


def preprocess_wifi(wifi, rssi_threshold=-85, contain_rssi=True, return_str=False):
    wifi_count = 0
    latest_ap_list = []
    if wifi.size > 0:
        wifi_format = [Experiment.format_wifi(wi) for wi in wifi]
        wifi_count_latest = wifi_format[-1]['count']
        for wi in wifi_format[::-1]:
            if wi['count'] != wifi_count_latest or len(latest_ap_list) == wifi_count_latest: break
            if str(wi['ssid']) != 'nan' and 'powan' not in str(wi['ssid']) and str(wi['ssid']) != '': # powan is the hotspot name for experiment smartphone
                latest_ap_list.append((str(wi['ssid']), wi['rssi']))
        latest_ap_list = [item for item in latest_ap_list if item[1] >= rssi_threshold]
        latest_ap_list = sorted(latest_ap_list, key=lambda x: x[1], reverse=True)
        if not contain_rssi: latest_ap_list = [item[0] for item in latest_ap_list]
        wifi_count = len(latest_ap_list)
    if return_str:
        return format_number(wifi_count, 0), str(latest_ap_list)
    else:
        return wifi_count, latest_ap_list


def preprocess_time(label):
    label_format = [Experiment.format_label(la) for la in label]
    time_start = label_format[0]['timestamp']
    time_end = label_format[-1]['timestamp']
    time_duration = duration_in_seconds(time_start, time_end)
    return time_duration, time_start, time_end


def preprocess_label(label_raw, labels_previous=None):
    label_format = [Experiment.format_label(la) for la in label_raw]
    if len(label_format) == 0:
        return labels_previous[0], labels_previous[1], labels_previous[2], labels_previous
    label_motion = find_mode([la['label_motion'] for la in label_format])
    label_transportation = find_mode([la['label_transportation'] for la in label_format])
    label_environment = find_mode([la['label_environment'] for la in label_format])
    labels = [label_motion, label_transportation, label_environment]
    if labels_previous is None:
        return label_motion, label_transportation, label_environment, labels
    else:
        if labels.count(-1) == 3:
            return labels_previous[0], labels_previous[1], labels_previous[2], labels_previous
        else:
            return label_motion, label_transportation, label_environment, labels


def decode_response(response, re_journal=r"Summary:[ \n]*(.*)"):
    response_new = response.replace('*', '')
    match = re.search(re_journal, response_new)
    if match:
        journal = match.group(1)
        return journal
    else:
        return "None"


def infer_daily_activity(path_dataset, path_save,time_window=20, seed=3432):
    set_seeds(seed)
    data = Experiment.from_directories(path_dataset)

    printer = Printer()
    i, usage_sum = 0, 0
    while i < len(data):

        exp = data[i]
        time_duration, time_start, time_end = preprocess_time(exp.label)
        time_tag = time_start  #

        while time_tag < time_end:
            time_tag_next = time_tag + time_window * 1000
            exp_sliced = exp.filter_by_timestamp(time_tag, time_tag_next)

            date_string, time_str, day_str = format_timestamp(time_tag_next)

            step_min = preprocess_step_counter(exp_sliced.step_counter, time_window, exp_sliced.accelerometer)
            acce_mean, acce_std = preprocess_linear_accelerometer(exp_sliced.linear_accelerometer)
            light = preprocess_light(exp_sliced.light)
            pressure_altitude_change = preprocess_pressure(exp_sliced.pressure, time_duration=None)
            satellite_count, satellite_snr, azimuths, elevations = preprocess_satellite(exp_sliced.satellite)
            wifi_last_count, latest_ap_list_filter = preprocess_wifi(exp_sliced.wifi)
            wifi_ssid_list = [ap[0] for ap in latest_ap_list_filter] if len(latest_ap_list_filter) > 0 else []
            wifi_rssi_list = [ap[1] for ap in latest_ap_list_filter] if len(latest_ap_list_filter) > 0 else []
            latitude, longitude, accuracy, speed, satellite_altitude_change = preprocess_location(exp_sliced.location,
                                                                                                  time_duration=time_window)
            speed_filter = speed if satellite_count is not None and satellite_count >= 5 else None
            motion_detected = detect_motion_rule(step_min, acce_mean, pressure_altitude_change, speed_filter, return_str=True)


            # Put your processing codes here
            #
            #

            printer.print("------------------------------------")
            journal_tag = date_string + " " + time_str

            journal_log = ''
            journal_log = log_append(journal_log, 'JOURNAL_TIME', journal_tag + " " + day_str)
            journal_log = log_append(journal_log, 'RESPONSE_MOTION', motion_detected)
            journal_log = log_append(journal_log, 'SENSOR_WIFI_SSID', str(wifi_ssid_list))
            journal_log = log_append(journal_log, 'SENSOR_LOCATION', str((latitude, longitude)))
            journal_log = log_append(journal_log, 'SENSOR_STEP', format_number(step_min, 2))
            journal_log = log_append(journal_log, 'SENSOR_ACCE', format_number(acce_mean, 2))
            journal_log = log_append(journal_log, 'SENSOR_LIGHT', light)
            journal_log = log_append(journal_log, 'SENSOR_ALTI_PRESSURE', format_number(pressure_altitude_change, 2))
            journal_log = log_append(journal_log, 'SENSOR_SPEED', format_number(speed_filter, 2))
            other_info = ("(satellite count: %s, satellite SNR: %s, satellite azimuths: %s, satellite elevations: %s,"
                          "wifi count: %s, wifi rssi: %s, location accuracy: %s)") % (
                             satellite_count, satellite_snr, azimuths, elevations, wifi_last_count, wifi_rssi_list,
                             accuracy)
            journal_log = log_append(journal_log, 'OTHERS', other_info)

            save_journal(path_save, "%s %s" % (date_string, time_str.replace(':', '')), journal_log)

            printer.print("Content:%s" % journal_log)
            time_tag = time_tag_next

        i += 1
    printer.print("------------------------------------")
    printer.print("Total usage token: %d" % usage_sum)
    printer.save(os.path.join(path_save, "log"))
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AutoLife sensor processing')
    parser.add_argument('experiment_dir', help='Input directory path')
    parser.add_argument('output_dir', help='Output directory path')

    args = parser.parse_args()

    infer_daily_activity(f"data/{args.experiment_dir}", f"saved/{args.output_dir}")

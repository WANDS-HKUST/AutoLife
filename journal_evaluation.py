# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/22
# @Author  : Huatao
# @Email   : 735820057@qq.com
# @File    : 
# @Description :
import json
import os
import re
import nltk
import numpy as np
from collections import defaultdict
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.chrf_score import sentence_chrf, corpus_chrf
from nltk.tokenize import word_tokenize
from rouge import Rouge
from nltk.translate import meteor
from bert_score import score

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

def extract_time_interval(name: str) -> int:
    """
    Extract the time interval from a string like
    'autolife_j240322_[1717-1746]' and return the duration in minutes.

    The time format is HHMM-HHMM.
    If the end time is earlier than the start time, it is treated as crossing midnight.
    """
    # Extract start and end time in HHMM format
    match = re.search(r'\[(\d{4})-(\d{4})\]', name)
    if not match:
        raise ValueError("Time interval not found in the string")

    start, end = match.groups()

    # Convert HHMM to minutes since 00:00
    sh, sm = int(start[:2]), int(start[2:])
    eh, em = int(end[:2]), int(end[2:])
    start_min = sh * 60 + sm
    end_min = eh * 60 + em

    # Handle cross-day case
    if end_min < start_min:
        end_min += 24 * 60

    # Return the duration in minutes
    return end_min - start_min


def determine_interval(time, time_intervals):
    # Check if the time is beyond the last interval
    if time >= time_intervals[-1]:
        return len(time_intervals) - 1
    # Iterate through the intervals to find in which interval the time falls
    for i in range(len(time_intervals) - 1):
        if time_intervals[i] <= time < time_intervals[i + 1]:
            return i


def merge_items_with_prefix(json_dict, prefix_length):
    merged_dict = defaultdict(list)

    for key, value in json_dict.items():
        prefix = key[:prefix_length]
        merged_dict[prefix].append(value)

    # Convert defaultdict back to a regular dict
    return dict(merged_dict)


def ensure_nltk_resource(resource_name: str, resource_path: str):
    """
    Ensure that an NLTK resource is available.
    If not, download it automatically.
    """
    try:
        nltk.data.find(resource_path)
    except LookupError:
        nltk.download(resource_name)

def evaluate_metrics(reference_text, candidate_text, metric_names, device='cuda:0'):
    # ensure_nltk_resource("punkt", "tokenizers/punkt")
    # ensure_nltk_resource("punkt_tab", "tokenizers/punkt_tab")
    candidate_text = candidate_text.lower()
    reference_text = reference_text.lower()
    metric_dict = {}
    if 'BLEU' in metric_names or 'ALL' in metric_names:
        candidate_tokens = word_tokenize(candidate_text)
        reference_tokens = [word_tokenize(reference_text)]
        bleu_score = sentence_bleu(reference_tokens, candidate_tokens)
        metric_dict['BLEU'] = bleu_score
    if 'chrF' in metric_names or 'ALL' in metric_names:
        chrf_score = sentence_chrf(reference_text, candidate_text)
        metric_dict['chrF'] = chrf_score
    if 'ROUGE' in metric_names or 'ALL' in metric_names:
        rouge_score = Rouge().get_scores(candidate_text, reference_text)
        metric_dict['ROUGE-1 f'] = rouge_score[0]['rouge-1']['f']
        metric_dict['ROUGE-1 p'] = rouge_score[0]['rouge-1']['p']
        metric_dict['ROUGE-1 r'] = rouge_score[0]['rouge-1']['r']
        metric_dict['ROUGE-2 f'] = rouge_score[0]['rouge-2']['f']
        metric_dict['ROUGE-2 p'] = rouge_score[0]['rouge-2']['p']
        metric_dict['ROUGE-2 r'] = rouge_score[0]['rouge-2']['r']
        metric_dict['ROUGE-l f'] = rouge_score[0]['rouge-l']['f']
        metric_dict['ROUGE-l p'] = rouge_score[0]['rouge-l']['p']
        metric_dict['ROUGE-l r'] = rouge_score[0]['rouge-l']['r']
    if 'METEOR' in metric_names or 'ALL' in metric_names:
        candidate_tokens = word_tokenize(candidate_text)
        reference_tokens = [word_tokenize(reference_text)]
        me_score = meteor(reference_tokens, candidate_tokens)
        metric_dict['METEOR'] = me_score
    # if 'BERTScore' in metric_names or 'ALL' in metric_names:
    #     # model_type = "bert-base-uncased" "microsoft/deberta-xlarge-mnli" | r"C:\Users\73582\Downloads\bert"
    #     P, R, F1 = score([candidate_text], [reference_text], lang="en", model_type="bert-base-uncased",
    #                      verbose=True)
    #     # P, R, F1 = score([candidate_text], [reference_text], lang="en", model_type=r"C:\Users\73582\Downloads\bert", verbose=True, device=device, num_layers=9)
    #     metric_dict['BERTScore p'] = P.item()
    #     metric_dict['BERTScore r'] = R.item()
    #     metric_dict['BERTScore f'] = F1.item()
    return metric_dict


def average_dicts(dict_list, precision=3):
    average_dict = {}

    if not dict_list:
        return average_dict

    for key in dict_list[0]:
        average_dict[key] = 0.0

    for d in dict_list:
        for key, value in d.items():
            average_dict[key] += value

    num_items = len(dict_list)
    for key in average_dict:
        average_dict[key] = round(average_dict[key] / num_items, precision)

    return average_dict


def max_dicts(dict_list, precision=3):
    max_dict = {}

    if not dict_list:
        return max_dict

    for key in dict_list[0]:
        max_dict[key] = 0.0

    for d in dict_list:
        for key, value in d.items():
            max_dict[key] = max(value, max_dict[key])
    return max_dict


def evaluate(path_ref, path_estimate, metric_list, time_interval_bins=[0, 30, 60, 90, 120, 150]):
    metric_dict_list = []
    metric_dict_time_list = [[] for i in range(len(time_interval_bins))]
    with open(path_estimate, 'r', encoding='utf-8') as file:
        journal_estimate = json.load(file)
    with open(path_ref, 'r', encoding='utf-8') as file:
        journal_ref = json.load(file)
    fail_list = []
    for key_ref, value_refs in journal_ref.items():
        match = False
        for key, value in journal_estimate.items():
            if key_ref in key:
                match = True
                print("Match found: %s to %s" % (key_ref, key))
                time_interval = value_refs['duration']
                tidx = determine_interval(time_interval, time_interval_bins)
                metric_dict_list_temp = []
                for j_ref in value_refs['reference_journals']:
                    for j_gen in value:
                        metric_dict_list_temp.append(evaluate_metrics(j_ref, j_gen, metric_list))
                metric_dict_list_max = max_dicts(metric_dict_list_temp)
                metric_dict_list.append(metric_dict_list_max)
                metric_dict_time_list[tidx].append(metric_dict_list_max)
                break
        if not match:
            print("Match failed: [%s]" % key_ref)
            fail_list.append(key_ref)
    print("Match failed keys: [%s]" % str(fail_list))
    return metric_dict_list, metric_dict_time_list


if __name__ == '__main__':
    metrics_all, metrics_all_time = evaluate('journals_reference.json', 'journals_generated_sample.json', metric_list=['ALL'])
    metrics_avg = average_dicts(metrics_all)
    print(metrics_avg)
    metrics_avg_time = [average_dicts(metrics_all_i) for metrics_all_i in metrics_all_time]
    print(metrics_avg_time)

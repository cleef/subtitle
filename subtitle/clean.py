# -*- coding: utf-8 -*-

import difflib


def is_similar(line1, line2, threshold=0.9):
    """
    Check if two lines are similar based on a given threshold.
    """
    similarity_ratio = difflib.SequenceMatcher(None, line1, line2).ratio()
    return similarity_ratio > threshold


def clean_subtitle(input_file, output_file, threshold=0.9):
    """
    Remove consecutive similar lines from a file.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    unique_lines = []
    previous_line = None

    for line in lines:
        # 小于4个字符clean
        if len(line.strip()) <4:
            continue

        if previous_line is None or not is_similar(previous_line, line, threshold):
            unique_lines.append(line)
            unique_lines.append('\n')
            previous_line = line

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)
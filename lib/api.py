#!/usr/bin/env python
# coding: UTF-8

import os
import sys
import csv
import yaml

from collections import OrderedDict

def represent_odict(dumper, instance):
    return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())

def writer(file_path, data, mode):
    try:
        wfp = os.path.normpath(file_path)
        with open(wfp, mode) as f:
            f.write(data)
    except IOError:
        sys.stderr.write("Error:Can not write %s file\n" % file_path)
        raise


def make_dir(dir_dic):
    for key_path in dir_dic:
        if not os.path.exists(dir_dic[key_path]):
            os.makedirs(dir_dic[key_path])


def convert_row2json(header, row_data, dict_data, skip_list):
    for header_key, value in zip(header, row_data):
        # if there is no value skip processing
        if not value:
            continue
        # Skip header_key matching skip_list
        if header_key in skip_list:
            continue
        # if header_key can be split
        if '.' in header_key:
            # if there is no header_key, a dictionary is create
            keys = header_key.split(".")
            tmp_dict = dict_data

            for key in keys:
                if key == keys[-1]:
                    tmp_dict[key] = value
                else:
                    if key not in tmp_dict:
                        tmp_dict[key] = {}
                    tmp_dict = tmp_dict[key]
        # set value
        else:
            dict_data[header_key] = value


def get_static_routes(hash_name, header, csv_data, csv_dict):
    csv_dict[0] = {}
    csv_dict[0][hash_name] = []

    for row_data in csv_data:
        # Avoid empty lines
        if len(row_data) == 0:
            continue

        tmp_dict = {}
        skip_list = [header[0]]
        convert_row2json(header, row_data, tmp_dict, skip_list)
        csv_dict[0][hash_name].append(tmp_dict)

    return csv_dict


def get_common(hash_name, header, csv_data, csv_dict):
    csv_dict[0] = {}
    csv_dict[0][hash_name] = {}

    for row_data in csv_data:
        # Avoid empty lines
        if len(row_data) == 0:
            continue

        csv_dict[0][hash_name][row_data[0]] = {}
        skip_list = [header[0]]
        convert_row2json(header, row_data, csv_dict[0][hash_name][row_data[0]], skip_list)

    return csv_dict


def get_endpoint(hash_name, header, csv_data, csv_dict):
    csv_dict[0] = {}
    csv_dict[0][hash_name] = {}
    csv_dict[0][hash_name]['endpoint'] = {}

    for row_data in csv_data:
        # Avoid empty lines
        if len(row_data) == 0:
            continue

        csv_dict[0][hash_name]['endpoint'][row_data[0]] = {}
        skip_list = [header[0]]
        convert_row2json(header, row_data, csv_dict[0][hash_name]['endpoint'][row_data[0]], skip_list)

    return csv_dict


def get_others(header, csv_data, csv_dict):
    for row_data in csv_data:
        # Avoid empty lines
        if len(row_data) == 0:
            continue

        csv_dict[row_data[0]] = {}
        skip_list = []
        convert_row2json(header, row_data, csv_dict[row_data[0]], skip_list)

    return csv_dict


def csv2json(file_path, hash_name=None, mode=None):
    # read csv file
    with open(file_path, 'rU') as f:
        csv_data = csv.reader(f)
        header = csv_data.next()
        csv_dict = OrderedDict()

        if mode == "static_routes":
            csv_dict = get_static_routes(hash_name, header, csv_data, csv_dict)
        elif mode == "common":
            csv_dict = get_common(hash_name, header, csv_data, csv_dict)
        elif mode == "endpoint":
            csv_dict = get_endpoint(hash_name, header, csv_data, csv_dict)
        else:
            csv_dict = get_others(header, csv_data, csv_dict)
    return csv_dict

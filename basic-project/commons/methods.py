from datetime import datetime
from functools import wraps
from os.path import expandvars

import yaml

def load_yaml(yaml_path):
    def process_dict(dict_to_process):
        for key, item in dict_to_process.items():
            if isinstance(item, dict):
                dict_to_process[key] = process_dict(item)
            elif isinstance(item, str):
                dict_to_process[key] = expandvars(item)
            elif isinstance(item, list):
                dict_to_process[key] = process_list(item)
        return dict_to_process

    def process_list(list_to_process):
        new_list = []
        for item in list_to_process:
            if isinstance(item, dict):
                new_list.append(process_dict(item))
            elif isinstance(item, str):
                new_list.append(expandvars(item))
            elif isinstance(item, list):
                new_list.append(process_list(item))
            else:
                new_list.append(item)
        return new_list

    with open(yaml_path) as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)

    return process_dict(yaml_content)

def get_current_timestamp(use_hour=True):
    if use_hour:
        return datetime.now().strftime("%Y%m%d-%H%M%S")
    else:
        return datetime.now().strftime("%Y%m%d")

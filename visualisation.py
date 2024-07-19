import math
import json
import os
from typing import Union, List
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def read_json_file(file_name):

    with open(file_name, 'r') as file:
        # Load the JSON data
        data = json.load(file)
    return data


def get_json_files(directory: str):
    json_files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and file.endswith(".json"):
            json_files.append(file_path)
    return json_files


def get_latest_data(directory: str):
    return [pd.DataFrame(read_json_file(file_path))
            for file_path in get_json_files(dir)]


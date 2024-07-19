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
            for file_path in get_json_files(directory)]


def spectogram_filter(
    frequencies: np.array,
    min_freq: Union[None, float] = None,
    max_freq: Union[None, float] = None,
) -> List[bool]:
    if min_freq is None:
        min_freq = np.nanmin(frequencies)
    if max_freq is None:
        max_freq = np.nanmax(frequencies)
    return (frequencies >= min_freq) & (frequencies <= max_freq)


def spectogram_plot(
        fig,
        ax,
        data: List,  # list of dataframes
        min_freq: Union[None, float] = None,
        max_freq: Union[None, float] = None
):

    time, amplitude = range(len(data)), np.array(
        [df["spectrum"] for df in data]).transpose()
    freq = np.arange(len(data[0])) * data[0]["freq_incr"]

    freq_indices = spectogram_filter(
        freq, min_freq=min_freq, max_freq=max_freq
    )
    freq = freq[freq_indices]
    amplitude = amplitude[freq_indices, :]

    im = ax.pcolormesh(time, freq, amplitude, shading="nearest")
    # fig.colorbar(im)
    return fig


def real_time_spectrogram(dir):
    fig, ax = plt.subplots()

    def animate(i):
        data = get_latest_data(dir)
        spectogram_plot(fig, ax, data, 100, 500)
        return fig, ax
    anim = FuncAnimation(fig, animate, interval=1000)  # Update every 1 second
    plt.tight_layout()
    plt.show()


def features_plot(
        fig, axes,
        comb,
        num_cols=5
):

    features = list(comb[0].columns)

    for i, feature in enumerate(features):
        row = i // num_cols
        col = i % num_cols
        time, data = range(len(comb)), [df.loc[0, feature] for df in comb]

        axes[row, col].plot(time, data)

        axes[row, col].set_title(feature)
    plt.tight_layout()
    plt.show()


def real_time_features(dir):
    fig, axes = plt.subplots(
        7, 5, figsize=(10, 10))

    def animate(i):
        data = get_latest_data(dir)
        features_plot(fig, axes, data)
        return fig, axes

    anim = FuncAnimation(fig, animate, interval=1000)  # Update every 1 second
    plt.tight_layout()
    plt.show()

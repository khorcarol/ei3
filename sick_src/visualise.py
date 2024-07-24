import time
import numpy as np
from sick_src import database
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


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

        axes[row, col].clear()
        axes[row, col].plot(time, data)
        axes[row, col].set_title(feature)
    plt.tight_layout()


def real_time_features(db, limit=10):
    fig, axes = plt.subplots(
        7, 5, figsize=(10, 10))

    def animate(i):
        latest_data = db.fetch_last_n_processed_features(limit)
        latest_data_as_dataframes = [pd.DataFrame(
            features_dict) for features_dict in latest_data]
        features_plot(fig, axes, latest_data_as_dataframes)
        return fig, axes

    anim = FuncAnimation(fig, animate, interval=1000)  # Update every 1 second
    plt.tight_layout()
    plt.show()


def spectogram_plot(
        fig,
        ax,
        data: List,  # list of dataframes
):

    time, amplitude = range(len(data)), np.array(
        [df["spectrum"] for df in data]).transpose()
    freq = np.arange(len(data[0]["spectrum"])) * data[0]["freq_incr"]

    im = ax.pcolormesh(time, freq, amplitude, shading="nearest")
    
    return fig


def real_time_spectrogram(db, limit = 10):
    fig, ax = plt.subplots()
    im = ax.pcolormesh([0], [0], [[0]], shading="nearest")
    cb =fig.colorbar(im)

    def animate(i):
        latest_data = db.fetch_last_n_processed_features(limit)
        latest_data_as_dataframes = [pd.DataFrame(
            features_dict) for features_dict in latest_data]
        spectogram_plot(fig, ax, latest_data)
        return fig, ax
    anim = FuncAnimation(fig, animate, interval=1000)  # Update every 1 second
    plt.tight_layout()
    plt.show()

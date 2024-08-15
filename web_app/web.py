import time
from typing import List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from sick_src.database import DBConnection

db = DBConnection()
sensor_id = 1


def spectrogram_plot(fig, ax, data: List):
    if len(data) == 0:
        return fig

    time, amplitude = range(len(data)), np.array(
        [df["spectrum"] for df in data]).transpose()
    freq = np.arange(len(data[0]["spectrum"])) * data[0]["freq_incr"]

    ax.clear()
    im = ax.pcolormesh(time, freq, amplitude, shading="nearest")
    fig.colorbar(im, ax=ax)

    return fig


def features_plot(fig, axes, comb, num_cols=5):
    if len(comb) == 0:
        return fig

    features = list(comb[0].columns)

    for i, feature in enumerate(features):
        row = i // num_cols
        col = i % num_cols
        time, data = range(len(comb)), [df.loc[0, feature] for df in comb]

        axes[row, col].clear()
        axes[row, col].plot(time, data)
        axes[row, col].set_title(feature)
    plt.tight_layout()

    return fig


def real_time_plots(db, sensor_id, limit=50, num_cols=5):
    # Setup for spectrogram plot
    fig_spectrogram, ax_spectrogram = plt.subplots(figsize=(10, 5))

    # Setup for features plot
    fig_features, axes_features = plt.subplots(7, num_cols, figsize=(15, 10))

    while True:
        latest_data = db.fetch_last_n_processed_features(sensor_id, limit)
        latest_data_as_dataframes = [pd.DataFrame(
            features_dict) for features_dict in latest_data]

        fig_spectrogram = spectrogram_plot(
            fig_spectrogram, ax_spectrogram, latest_data_as_dataframes)
        fig_features = features_plot(
            fig_features, axes_features, latest_data_as_dataframes, num_cols)

        st.pyplot(fig_spectrogram)
        st.pyplot(fig_features)
        time.sleep(1)
        st.rerun()

# Streamlit app
st.title('Live Dashboard')

data = db.fetch_all_to_df()
sensor_options = pd.unique(data["sensor_id"])
sensor_id = st.selectbox('Select Sensor ID', sensor_options)

real_time_plots(db, sensor_id)

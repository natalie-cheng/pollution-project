import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

plt.style.use('ggplot')

def yearly_pollution(df, pollutant, cali=True):

    # Prepare Data
    if cali:
        plot_data = df[df['State']=='California']
    else:
        plot_data = df
    
    plot_data = plot_data.sort_values(by="YearLocal")

    plot_grouped = plot_data.groupby('YearLocal').mean()

    # Draw Chart
    fig, ax = plt.subplots()

    ax.plot(plot_data['YearLocal'].unique(),
            plot_grouped[pollutant],
            marker='o')

    ax.plot(plot_data['YearLocal'].unique(),
                    np.full(len(plot_data['YearLocal'].unique()),
                            plot_grouped[pollutant].mean()),
                    linestyle='--')

    for x,y in zip(plot_data['YearLocal'].unique(),plot_grouped[pollutant]):
        ax.annotate(round(y,3), (x,y))

    for label in ax.xaxis.get_ticklabels()[1::2]:
        label.set_visible(False)

    ax.text(plot_data['YearLocal'].unique()[0],
            plot_grouped[pollutant].mean(),
            f'Mean: {round(plot_grouped[pollutant].mean(),3)}')

    return fig
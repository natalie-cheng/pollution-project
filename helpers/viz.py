import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st

plt.style.use('ggplot')

def yearly_pollution(df, pollutant, cali=True, values=True):
    
    # Prepare Data
    if cali:
        plot_data = df[df['State']=='California']
    else:
        plot_data = df
    
    plot_data = plot_data.sort_values(by="YearLocal")

    numeric_columns = plot_data.select_dtypes(include='number').columns

    # Perform the groupby and mean calculation
    plot_grouped = plot_data.groupby("YearLocal")[numeric_columns].mean()

    # Draw Chart
    fig, ax = plt.subplots()

    ax.plot(plot_data['YearLocal'].unique(),
            plot_grouped[pollutant],
            marker='o',
            color='indigo')

    ax.plot(plot_data['YearLocal'].unique(),
            np.full(len(plot_data['YearLocal'].unique()),
            plot_grouped[pollutant].mean()),
            linestyle='--')
    
    if values:
        for x,y in zip(plot_data['YearLocal'].unique(),plot_grouped[pollutant]):
            ax.annotate(round(y,3), (x,y), fontsize=7)

    for label in ax.xaxis.get_ticklabels()[1::2]:
        label.set_visible(False)

    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(10)
    
    ax.text(plot_data['YearLocal'].unique()[0],
            plot_grouped[pollutant].mean(),
            f'Mean: {round(plot_grouped[pollutant].mean(),3)}' if values else 'Mean')

    return fig

def monthly_pollution(df, pollutant, cali=True, values=True):

    # Prepare Data
    if cali:
        plot_data = df[df['State']=='California']
    else:
        plot_data = df
        
    plot_data = plot_data.sort_values(by="MonthLocal")

    numeric_columns = plot_data.select_dtypes(include='number').columns

    plot_grouped = plot_data.groupby('MonthLocal')[numeric_columns].mean()

    # Draw Chart
    fig, ax = plt.subplots()

    ax.plot(plot_data['MonthLocal'].unique(),
            plot_grouped[pollutant],
            marker='o',
            color='indigo')

    ax.plot(plot_data['MonthLocal'].unique(),
            np.full(len(plot_data['MonthLocal'].unique()),
            plot_grouped[pollutant].mean()),
            linestyle='--')
    
    if values:
        for x,y in zip(plot_data['MonthLocal'].unique(),plot_grouped[pollutant]):
            ax.annotate(round(y,3), (x,y))

    for label in ax.xaxis.get_ticklabels()[1::2]:
        label.set_visible(False)
    
    ax.text(plot_data['MonthLocal'].unique()[0],
            plot_grouped[pollutant].mean(),
            f'Mean: {round(plot_grouped[pollutant].mean(),3)}' if values else 'Mean')

    return fig

def ranking_pollution(df, pollutant, values):

    # Prepare Data
    plot_data = df.groupby('State')[pollutant].mean()

    country_data = pd.Series(plot_data.mean(),['US National Average'])

    plot_data = pd.concat([plot_data, country_data])

    plot_data = plot_data.sort_values(ascending=False).head(30).sort_values()
    
    cali_index = list(plot_data.index).index('California')
    country_index = list(plot_data.index).index('US National Average')

    # Draw Chart
    fig, ax = plt.subplots()
    ax.barh(plot_data.index,plot_data.values)
    ax.get_children()[cali_index].set_color('green')
    ax.get_children()[country_index].set_color('grey')
    xlim = plot_data.values.min() * 0.9
    ax.set(xlim=[xlim,None],
    yticks=np.arange(0,30),)

    if values:
        for x,y in enumerate(plot_data.values):
            ax.text(xlim,x,round(y,3),color='black',va='center')
    
    return fig

def pollution_map(merged, pollution,values=True):
    
    # Draw Chart
    fig, ax = plt.subplots()
    gplt.choropleth(merged[['NAME', 'geometry', pollution, 'coords']],
    hue=pollution,cmap='Reds', ax=ax)

    # Label states and data
    if values:
        for _,row in merged.iterrows():
            if row['NAME'] not in ['Connecticut', 'Massachusetts', 'Rhode Island','Vermont',
            'District of Columbia', 'Delaware', 'Maryland', 'New Jersey']:
                ax.text(row['coords'][0], row['coords'][1], row['NAME'],ha='center',fontsize=3)
                ax.text(row['coords'][0], row['coords'][1]-.75,
                round(row[pollution],2) if row[pollution]!=0 else 'N/A',ha='center',fontsize=4)
    
    return fig
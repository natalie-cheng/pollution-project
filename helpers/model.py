import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.linear_model  import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures

plt.style.use('ggplot')

def pollution_model(data, name, degree):
    numeric_columns = data.select_dtypes(include='number').columns

    plot_grouped = data.groupby('YearLocal')[numeric_columns].mean()
    
    X = np.arange(len(plot_grouped[name])).reshape(-1,1)
    y = plot_grouped[name]
    
    poly_reg = PolynomialFeatures(degree = degree)
    X_poly = poly_reg.fit_transform(X)
    
    lm = LinearRegression(normalize=True)
    lm.fit(X_poly, y)
    
    return lm,poly_reg

def pollution_prediction(df, pollutant, cali=True, values=True):

    # Prepare Data
    if cali:
        plot_data = df[df['State']=='California']
    else:
        plot_data = df
    
    plot_data = plot_data.sort_values(by="YearLocal")

    numeric_columns = plot_data.select_dtypes(include='number').columns

    plot_grouped = plot_data.groupby('YearLocal')[numeric_columns].mean()

    years = range(2000,2026)

    # Draw Chart
    fig, ax = plt.subplots()

    ax.plot(plot_data['YearLocal'].unique(), plot_grouped[pollutant], marker='o')
        
    model, poly_reg = pollution_model(plot_data, pollutant, 1)
    X_test = poly_reg.fit_transform(np.arange(len(years)).reshape(-1,1))
    prediction = model.predict(X_test)
    prediction[prediction<0] = 0
    
    ax.plot(years, prediction, linestyle = '--')
    ax.set(xticks=years)

    if values:
        for x,y in zip(plot_data['YearLocal'].unique(),plot_grouped[pollutant]):
            ax.annotate(round(y,3), (x,y))

    for label in ax.xaxis.get_ticklabels()[1::2]:
        label.set_visible(False)
    
    return fig
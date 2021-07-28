import pandas as pandas
import matplotlib.pyplot as pyplot
import numpy as numpy

import streamlit as st

from helpers.data import load_data, data_preprocessing
from helpers.viz import yearly_pollution

DATA_PATH = 'pollution_us_2000_2016.csv'

st.title("Pollution Project")

# Read Data
df = load_data(DATA_PATH, 1000)

st.subheader('Raw data')
st.dataframe(df)
st.write(df.columns)

# Clean Data

st.subheader('Data Preprocessing')
df_cleaned = data_preprocessing(df.copy())

st.subheader('Cleaned data')
st.dataframe(df_cleaned)

# Data Visualization

st.subheader('Data Visualization')

pollutant = st.selectbox('By Pollutant', ["NO2Mean", "SO2Mean", "O3Mean", "COMean"])

cali = st.checkbox('Cali Data Only')

st.markdown(f"__{pollutant} in {'California' if cali else 'the US'} between 2000 and 2016__")

yearly_pollution_chart = yearly_pollution(df_cleaned, pollutant, cali)

st.pyplot(yearly_pollution_chart)
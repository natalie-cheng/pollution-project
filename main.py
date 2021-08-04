import pandas as pandas
import matplotlib.pyplot as pyplot
import numpy as numpy
import geopandas as gpd
import geoplot as gplt
import streamlit as st

from helpers.data import load_data, data_preprocessing, load_geo_data, geo_data_preprocessing
from helpers.viz import yearly_pollution, monthly_pollution, ranking_pollution, pollution_map
from helpers.model import pollution_prediction

DATA_PATH = 'pollution_us_2000_2016.csv'

st.title("Analysis of US Pollution between 2000 and 2016, focusing on California")

# Read Data

df = load_data(DATA_PATH,145000)

st.header('Raw data')
st.dataframe(df)

# Clean Data

st.header('Data Preprocessing')
df_cleaned = data_preprocessing(df.copy())

st.subheader('Cleaned data')
st.dataframe(df_cleaned)


# Data Visualization

st.header('Data Visualization')

st.sidebar.title('Filters')


pollutant = st.sidebar.selectbox('Pollutant', ["NO2Mean", "SO2Mean", "O3Mean", "COMean"])

cali = st.sidebar.checkbox('Cali Data Only')

values = st.sidebar.checkbox('Show Data Values')

# Yearly plot
st.subheader('Yearly pollution change')

st.markdown(f"__{pollutant} in {'California' if cali else 'the US'} by year between 2000 and 2016__")

yearly_pollution_chart = yearly_pollution(df_cleaned, pollutant, cali, values)

st.pyplot(yearly_pollution_chart)

# Monthly plot
st.subheader('Monthly pollution change')

st.markdown(f"__{pollutant} in {'California' if cali else 'the US'} by month between 2000 and 2016__")

monthly_pollution_chart = monthly_pollution(df_cleaned, pollutant, cali, values)

st.pyplot(monthly_pollution_chart)

# Ranking plot
st.subheader('State rankings')

st.markdown(f"__Top 30 {pollutant} rankings in the US__")

ranking_pollution_chart = ranking_pollution(df_cleaned, pollutant, values)

st.pyplot(ranking_pollution_chart)

# Modeling
st.subheader('Prediction Model')

st.markdown(f"__{pollutant} predictions until 2026 in {'California' if cali else 'the US'}__")

prediction_model = pollution_prediction(df_cleaned, pollutant, cali, values)

st.pyplot(prediction_model)


# Data Mapping

st.header('Data Mapping')

GEO_DATA_PATH = 'geo_data.json'

# Read Data
geo_data = load_geo_data(GEO_DATA_PATH)

st.subheader('Raw Geo Data (sample of 3)')

st.write(geo_data.sample(3))

# Clean and merge data
st.subheader('Geo data Preprocessing: Cleaned and Merged Geo data (sample of 3)')
merged = geo_data_preprocessing(geo_data.copy(), df_cleaned.copy())
st.write(merged.sample(3))

# Map data
st.subheader('Mapped data')

st.markdown(f"__US {pollutant} Averages from 2000 to 2016__")

pollution_map = pollution_map(merged, pollutant, values)

st.pyplot(pollution_map)
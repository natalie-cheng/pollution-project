import pandas as pd
import streamlit as st

@st.cache(allow_output_mutation = True)
def load_data(path, nrows=None):
    df = pd.read_csv(path)

    if nrows:
        df = df.sample(nrows)
    
    return df

def data_preprocessing(df):
    with st.echo():

        # Drop unused columns
        #df.drop(columns=['SO2 AQI','CO AQI','Unnamed: 0','NO2 Units','O3 Units','SO2 Units','CO Units'],inplace=True)
        
        # Remove duplicated data
        df = df[~df.duplicated()]

        # Rename columns
        df.columns = ['StateCode', 'CountyCode', 'SiteNum', 'Address', 'State', 'County',
        'City', 'DateLocal', 'NO2Mean', 'NO2Value',
        'NO2Hour', 'NO2AQI', 'O3Mean',
        'O3Value', 'O3Hour', 'O3AQI',
        'SO2Mean', 'SO2Value', 'SO2Hour',
        'COMean', 'COValue', 'COHour']
        
        # Exclude Mexico
        df = df[df['State']!='Country Of Mexico']

        # Convert to datetime
        df['DateLocal'] = pd.to_datetime(df['DateLocal'])
        df['MonthLocal'] = df['DateLocal'].dt.month
        df['YearLocal'] = df['DateLocal'].dt.year

    return df
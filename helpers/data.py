import pandas as pd
import geopandas as gpd
import streamlit as st

@st.cache_data()
#allow_output_mutation = True
def load_data(path, nrows=None):
    df = pd.read_csv(path)

    if nrows:
        df = df.sample(nrows)
    
    return df

def data_preprocessing(df):
    with st.echo():

        # Drop unused columns
        df.drop(columns=['SO2 AQI','CO AQI','Unnamed: 0','NO2 Units','O3 Units','SO2 Units','CO Units','Address'],inplace=True)
        
        # Remove duplicated data
        df = df[~df.duplicated()]

        # Rename columns
        df.columns = ['StateCode', 'CountyCode', 'SiteNum', 'State', 'County',
        'City', 'DateLocal', 'NO2Mean', 'NO2Value',
        'NO2Hour', 'NO2AQI', 'O3Mean',
        'O3Value', 'O3Hour', 'O3AQI',
        'SO2Mean', 'SO2Value', 'SO2Hour',
        'COMean', 'COValue', 'COHour']
        
        # Exclude Mexico
        df = df[df['State']!='Country Of Mexico']

        # Rename District of Columbia
        df['State'].replace('District Of Columbia','District of Columbia',inplace=True)

        # Convert to datetime
        df['DateLocal'] = pd.to_datetime(df['DateLocal'])
        df['MonthLocal'] = df['DateLocal'].dt.month
        df['YearLocal'] = df['DateLocal'].dt.year

        return df

@st.cache_data
def load_geo_data(path):
    geo_data = gpd.read_file(path)

    # Remove non-relevant columns
    geo_data = geo_data[['NAME','geometry']]

    return geo_data

def geo_data_preprocessing(geo_data, df):
    
    # Exclude Puerto Rico
    geo_data = geo_data[geo_data['NAME']!='Puerto Rico']

    # Group the pollution data by state
    grouped = df.groupby('State')[["NO2Mean", "SO2Mean", "O3Mean", "COMean"]].mean()

    # Merge the pollution data and geo data
    merged = geo_data.merge(grouped,how='left',right_index=True,left_on='NAME')

    # Exlude Alaska and Hawaii (does not fit on map)
    merged = merged[merged['NAME']!='Alaska']
    merged = merged[merged['NAME']!='Hawaii']

    # Fill null values
    merged.fillna(0,inplace=True)

    # Extract coordinates from geo data
    merged['coords'] = merged['geometry'].apply(lambda x: x.representative_point().coords)
    
    merged['long'] = [coords[0][0] for coords in merged['coords']]
    merged['lat'] = [coords[0][1] for coords in merged['coords']]

    merged = merged[['NAME','NO2Mean','O3Mean','SO2Mean','COMean','long','lat']]

    return merged
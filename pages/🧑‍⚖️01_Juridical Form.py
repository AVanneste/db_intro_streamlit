import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px
import numpy as np


st.set_page_config(layout="wide", page_title="Belgium Enterprises Visualization", page_icon = 'App_Icon.png')

load_page = False


# Check if a dataframe has been created from upload in Homepage
if 'df' in st.session_state :
    df = st.session_state['df']
    load_page = True
else:
    st.write('Upload a file on Homepage first')

# If yes then we can work on it
if load_page:

    df = df.dropna()
    df = df[df['Region'].notna()]
    regions = list(df['Region'].unique())
    regions.sort()
    regions.insert(0,'All of Belgium')
    
    region_choice = st.sidebar.selectbox('Select a Region:', regions, index=0)

    if region_choice == 'All of Belgium':
        pass
    else:

        df = df.loc[df['Region']==region_choice]
        provinces = df["Province"].loc[df["Region"] == region_choice]
        provinces = list(np.unique(provinces))
        provinces.sort()
        provinces.insert(0,'Whole Region')
        province_choice = st.sidebar.selectbox('Select a Province', provinces, index=0) 

        if province_choice == 'Whole Region':
            pass
        else:

            df = df.loc[df['Province']==province_choice]
            cities = df["City"].loc[df["Province"] == province_choice]
            cities = list(np.unique(cities))
            cities.sort()
            cities.insert(0,'Whole Province')
            city_choice = st.sidebar.selectbox('Select a City', cities, index=0)
            if city_choice == 'Whole Province':
                pass
            else:
                df = df.loc[df['City']== city_choice]


    # Get percentage of each code
    df = df.groupby(['JuridicalForm','Description'])['JuridicalForm'].count().sort_values(ascending=False).reset_index(name="Percentage")
    df['Percentage'] = 100*df['Percentage']/df['Percentage'].sum()


    # Scatterplot display
    col1, col2 = st.columns(2)

    x_axis_val = col1.selectbox('Select the X-axis', options=df.columns)
    y_axis_val = col2.selectbox('Select the Y-axis', options=df.columns, index=2)

    col = st.color_picker('Select a plot colour')

    plot = px.scatter(df, x=x_axis_val, y=y_axis_val)
    plot.update_traces(marker=dict(color=col))
    st.plotly_chart(plot, use_container_width=True)

    df


# Hide footer and top menu
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

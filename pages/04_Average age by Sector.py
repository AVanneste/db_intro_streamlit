import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px
from datetime import datetime
from datetime import date
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


    # The idea here is to create a few select boxes in the sidebar to choose (or not) region/province/city
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



    df = df[['StartDate', 'NaceCode']]
    df['NaceCode'] = df['NaceCode'].astype(str)


    df['Code'] = df['NaceCode']

    df['Code'] = [x[:2] for x in df['Code']]

    df = df.drop(df[df['Code'].str.isalpha()].index)

    def categories(data):
        if (data=='01') or (data=='02') or (data=='03'):
            return 'A'
        elif (data=='05') or (data=='06') or (data=='07') or (data=='08') or (data=='09'):
            return 'B'
        elif (int(data)>10) and (int(data)<34):
            return 'C'
        elif (int(data)==35):
            return 'D'
        elif (int(data)>35) and (int(data)<40):
            return 'E'
        elif (int(data)>40) and (int(data)<44):
            return 'F'
        elif (int(data)>44) and (int(data)<48):
            return 'G'
        elif (int(data)>48) and (int(data)<54):
            return 'H'
        elif (int(data)>54) and (int(data)<57):
            return 'I'
        elif (int(data)>57) and (int(data)<64):
            return 'J'
        elif (int(data)>63) and (int(data)<67):
            return 'K'
        elif (int(data)==68):
            return 'L'
        elif (int(data)>68) and (int(data)<76):
            return 'M'
        elif (int(data)>76) and (int(data)<83):
            return 'N'
        elif (int(data)==84):
            return 'O'
        elif (int(data)==85):
            return 'P'
        elif (int(data)>85) and (int(data)<89):
            return 'Q'
        elif (int(data)>89) and (int(data)<94):
            return 'R'
        elif (int(data)>93) and (int(data)<97):
            return 'S'
        elif (int(data)>96) and (int(data)<99):
            return 'T'
        elif (int(data)==99):
            return 'U'

    df['Category'] = df['Code'].apply(categories)


    def calculate_age(start):
        start = datetime.strptime(start, "%Y-%m-%d").date()
        today = date.today()
        return today.year - start.year - ((today.month, today.day) < (start.month, start.day))

    df = df.mask(df.eq('None')).dropna()

    df['StartDate'] = df['StartDate'].astype(str)

    df['StartDate'] = [x[:10] for x in df['StartDate']]

    df['age'] = df['StartDate'].apply(calculate_age)

    df = df.mask(df['age']>220)
    df = df.dropna()

    df = df.groupby(['Category'])['age'].mean().reset_index(name ='Average age')


    col1, col2 = st.columns(2)

    x_axis_val = col1.selectbox('Select the X-axis', options=df.columns)
    y_axis_val = col2.selectbox('Select the Y-axis', options=df.columns, index=1)

    plot = px.histogram(df, x=x_axis_val, y=y_axis_val).update_xaxes(categoryorder='total descending')
    st.plotly_chart(plot, use_container_width=True)

    con = sqlite3.connect("bce.db")
    df4 = pd.read_sql_query("SELECT Code, Description from code WHERE Category = 'Nace2008' and Language = 'FR'", con) 
    df4 = df4.drop(df4[~df4['Code'].str.isalpha()].index)
    df4.rename(columns={'Code':'Category'}, inplace=True)

    df = df.merge(df4, on='Category')

    df

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)
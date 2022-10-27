import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px
from datetime import datetime
from datetime import date

df = st.session_state['df']
# df = pd.read_csv('merge.csv')

df = df[['StartDate', 'NaceCode']]
df['NaceCode'] = df['NaceCode'].astype(str)


df['Code'] = df['NaceCode']

df['Code'] = [x[:2] for x in df['Code']]

df = df.drop(df[df['Code'].str.isalpha()].index)
df['Code'] = df['Code'].astype(int)



def categories(data):
    if data<4:
        return 'A'
    elif (data>4) and (data<10):
        return 'B'
    elif (data>9) and (data<34):
        return 'C'
    elif (data==35):
        return 'D'
    elif (data>35) and (data<40):
        return 'E'
    elif (data>40) and (data<44):
        return 'F'
    elif (data>44) and (data<48):
        return 'G'
    elif (data>48) and (data<54):
        return 'H'
    elif (data>54) and (data<57):
        return 'I'
    elif (data>57) and (data<64):
        return 'J'
    elif (data>63) and (data<67):
        return 'K'
    elif (data==68):
        return 'L'
    elif (data>68) and (data<76):
        return 'M'
    elif (data>76) and (data<83):
        return 'N'
    elif (data==84):
        return 'O'
    elif (data==85):
        return 'P'
    elif (data>85) and (data<89):
        return 'Q'
    elif (data>89) and (data<94):
        return 'R'
    elif (data>93) and (data<97):
        return 'S'
    elif (data>96) and (data<99):
        return 'T'
    elif (data==99):
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
y_axis_val = col2.selectbox('Select the Y-axis', options=df.columns)

plot = px.histogram(df, x=x_axis_val, y=y_axis_val).update_xaxes(categoryorder='total descending')
st.plotly_chart(plot, use_container_width=True)

con = sqlite3.connect("bce.db")
df4 = pd.read_sql_query("SELECT Code, Description from code WHERE Category = 'Nace2008' and Language = 'FR'", con) 
df4 = df4.drop(df4[~df4['Code'].str.isalpha()].index)
df4.rename(columns={'Code':'Category'}, inplace=True)

df = df.merge(df4, on='Category')

df

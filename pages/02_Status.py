import pandas as pd
import sqlite3
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide", page_title="Belgium Enterprises Visualization", page_icon = 'App_Icon.png')


st.text('We can see that 100% of the enterprises in the database have the AC (=Active) status')

con = sqlite3.connect("bce.db")
df = pd.read_sql_query("SELECT EnterpriseNumber, Status from enterprise", con)

df = df.groupby(['Status'])['Status'].count().reset_index(name="Count")


col1, col2 = st.columns(2)

x_axis_val = col1.selectbox('Select the X-axis', options=df.columns, index=0)
y_axis_val = col2.selectbox('Select the Y-axis', options=df.columns, index=1)

plot = px.histogram(df, x=x_axis_val, y=y_axis_val).update_xaxes(categoryorder='total descending')
st.plotly_chart(plot, use_container_width=True)

df

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)
import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide", page_title="Belgium Enterprises Visualization", page_icon = 'App_Icon.png')

# Connection to the database
con = sqlite3.connect("bce.db")

# Make it a dataframe with joined tables in SQL queries
df = pd.read_sql_query("SELECT EnterpriseNumber, Code, Description FROM code INNER JOIN enterprise ON enterprise.JuridicalForm = code.Code WHERE Language = 'FR' and Category = 'JuridicalForm' ", con)

# Get percentage of each code
df = df.groupby(['Code','Description'])['Code'].count().sort_values(ascending=False).reset_index(name="Percentage")
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
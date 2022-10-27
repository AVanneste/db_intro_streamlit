import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px


con = sqlite3.connect("bce.db")
df = pd.read_sql_query("SELECT * from enterprise", con)

df2 = df.groupby(['JuridicalForm'])['JuridicalForm'].count().sort_values(ascending=False).reset_index(name="Percentage")
df2['Percentage'] = 100*df2['Percentage']/df2['Percentage'].sum()

df_JFNames = pd.read_sql_query("SELECT Code, Description FROM code WHERE Language = 'FR' and Category = 'JuridicalForm' ", con)
df_JFNames.rename(columns={'Code':'JuridicalForm'}, inplace=True)

df2 = df2.merge(df_JFNames, on='JuridicalForm')

col1, col2 = st.columns(2)

x_axis_val = col1.selectbox('Select the X-axis', options=df2.columns)
y_axis_val = col2.selectbox('Select the Y-axis', options=df2.columns)

plot = px.scatter(df2, x=x_axis_val, y=y_axis_val)
st.plotly_chart(plot, use_container_width=True)

df2
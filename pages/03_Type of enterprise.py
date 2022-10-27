import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px


con = sqlite3.connect("bce.db")
df = pd.read_sql_query("SELECT * from enterprise", con)

df2 = df.groupby(['TypeOfEnterprise'])['TypeOfEnterprise'].count().sort_values(ascending=False).reset_index(name="Percentage")
df2['Percentage'] = 100*df2['Percentage']/df2['Percentage'].sum()

df_Type = pd.read_sql_query("SELECT Code, Description FROM code WHERE Language = 'FR' and Category = 'TypeOfEnterprise' ", con)
df_Type.rename(columns={'Code':'TypeOfEnterprise'}, inplace=True)

df2 = df2.merge(df_Type, on='TypeOfEnterprise')

plot = px.histogram(df2, x=df2['Description'], y=df2['Percentage'])
st.plotly_chart(plot, use_container_width=True)

df2

import pandas as pd
import sqlite3
import plotly.express as px
import streamlit as st

st.text('We can see that 100% of the enterprises in the database have the AC (=Active) status')

con = sqlite3.connect("bce.db")
df = pd.read_sql_query("SELECT * from enterprise", con)

df3 = df.groupby(['Status'])['Status'].count().reset_index(name="Count")


col1, col2 = st.columns(2)

x_axis_val = col1.selectbox('Select the X-axis', options=df.columns)
y_axis_val = col2.selectbox('Select the Y-axis', options=df.columns)

plot = px.histogram(df, x=x_axis_val, y=y_axis_val).update_xaxes(categoryorder='total descending')
st.plotly_chart(plot, use_container_width=True)

df3



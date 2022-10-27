from turtle import width
import pandas as pd
import sqlite3
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
from datetime import date
from PIL import Image

# Home page display

st.set_page_config(layout="wide", page_title="Belgium Enterprises Visualization", page_icon = 'App_Icon.png')


# display of BeCode logo and center it (thus the colummns thing)
col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')
with col2:
    st.image('BeCode.png', width=300)
with col3:
    st.write(' ')

# Title of the project
st.title('🇧🇪Belgium Enterprises Visualization🇧🇪')

# Upload box, select file
upload_file = st.file_uploader('Upload a file containing data')

# upload the file
if upload_file is not None:

    try:
        df = pd.read_csv(upload_file,dtype=str)
        st.write('Data uploaded successfully. These are the first 5 rows.')
        st.dataframe(df.head(5))

        # make the file usable in other pages:
        st.session_state['df'] = df

    except Exception as e:
        st.write(e)

# Hide the footer
hide_default_format = """
       <style>
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


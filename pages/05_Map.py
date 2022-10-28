import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", page_title="Belgium Enterprises Visualization", page_icon = 'App_Icon.png')

# df = pd.read_csv('sample_latlng.csv')


load_page = False
# Check if a dataframe has been created from upload in Homepage
if 'df' in st.session_state :
    df = st.session_state['df']
    load_page = True
else:
    st.write('Upload a file on Homepage first')

# If yes then we can work on it
if load_page:

    df.rename(columns={'lng':'lon'}, inplace=True)
    st.map(df.sample(frac=0.1), zoom=7)
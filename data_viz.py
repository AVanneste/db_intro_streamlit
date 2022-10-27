import pandas as pd
import sqlite3
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
from datetime import date

# con = sqlite3.connect("bce.db")

st.title('Belgium enterprises visualization')

upload_file = st.file_uploader('Upload a file containing data')

if upload_file is not None:

    try:
        df = pd.read_csv(upload_file)
        # df.to_sql(name=table_name, con=conn)
        st.write('Data uploaded successfully. These are the first 5 rows.')
        st.dataframe(df.head(5))
        st.session_state['df'] = df

    except Exception as e:
        st.write(e)





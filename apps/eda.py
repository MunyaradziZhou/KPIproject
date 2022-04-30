import streamlit as st
import pandas as pd  
import plotly.express as px  
import base64  
from io import StringIO, BytesIO  
import numpy as np
import pandas as pd
from sklearn import datasets
import matplotlib.pyplot as plt
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

def app():
    st.markdown('''
# **The EDA App**
This is the **EDA App** by Munyaradzi Zhou
---
''')

# Upload CSV data
    with st.sidebar.header('1. Upload your XLSX data'):
        uploaded_file = st.sidebar.file_uploader("Upload your input XLSX file", type=["xlsx"])
       

    # Pandas Profiling Report
    if uploaded_file is not None:
        @st.cache
        def load_csv():
            csv = pd.read_excel(uploaded_file,engine='openpyxl')
            #csv = pd.read_csv(uploaded_file,encoding='latin1', index_col=None,usecols = "A,B,C,D,E,F,H,G,H,I,J")
            return csv
        df = load_csv()
        pr = ProfileReport(df, explorative=True)
        st.header('**Input DataFrame**')
        st.write(df)
        st.write('---')
        st.header('**Pandas Profiling Report**')
        st_profile_report(pr)
        
    else:
        st.info('Awaiting for CSV file to be uploaded.')
        
        if st.button('Press to use Example Dataset'):
            # Example data
            @st.cache
            def load_data():
                a = pd.DataFrame(
                    np.random.rand(100, 5),
                    columns=['a', 'b', 'c', 'd', 'e']
                )
                return a
            df = load_data()
            pr = ProfileReport(df, explorative=True)
            st.header('**Input DataFrame**')
            st.write(df)
            st.write('---')
            st.header('**Pandas Profiling Report**')
            st_profile_report(pr)
            
            
        

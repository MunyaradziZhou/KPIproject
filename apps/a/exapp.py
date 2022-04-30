# pip install openpyxl
import pandas as pd
import streamlit as st
import zipfile
import base64
import os
from PIL import Image
def app():
    st.title('Excel File Merger')
    
    img = Image.open("unnamed.png")
    
# Web App Title  **Omni Contact DataScience Application**
   
# st.sidebar.image('unnamed.png', width=200)
    st.markdown('''





---
 ## Upload your ZIP file
''')
    header = st.container()
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    def excel_file_merge(zip_file_name):
        
        df = pd.DataFrame()
        archive = zipfile.ZipFile(zip_file_name, 'r')
        with zipfile.ZipFile(zip_file_name, "r") as f:
            for file in f.namelist():
                xlfile = archive.open(file)
                if file.endswith('.xlsx'):
                    
            # Add a note indicating the file name that this dataframe originates from
                    df_xl = pd.read_excel(xlfile, engine='openpyxl',index_col=None, usecols = "D,F,H,J,L")
                    df_xl['Note'] = file
            # Appends content of each Excel file iteratively       , na_values=['NA'], usecols = "L"
            # index_col=None, na_values=['NA'], usecols = "A,C:AA"
                    df_xl = df_xl[df_xl['Unnamed: 11'].notna()]
                    df = df.append(df_xl, ignore_index=True)
            #df = df[df['tail'].notna()]
           
            # columns=['col 1', 'col 2']
        return df
    
    # Upload CSV data
    with st.sidebar.header('Upload your ZIP file'):
        
       
        #uploaded_file = st.sidebar.file_uploader("", type=["zip"])
        
        st.sidebar.markdown("""

                            

                            
""")
    uploaded_file = st.file_uploader("", type=["zip"])

    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    #st.sidebar.write("")
   
  
    

# File download
    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="merged_file.csv">Download Merged File as CSV</a>'
        return href

    def xldownload(df):
        df.to_excel('data1.xlsx', index=False)
        data = open('data1.xlsx', 'rb').read()
        b64 = base64.b64encode(data).decode('UTF-8')
        #b64 = base64.b64encode(xl.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/xls;base64,{b64}" download="merged_file.xlsx">Download Merged File as XLSX</a>'
        return href
    
    
# Main panel
    st.write("")
   # st.write("")
    if st.button('Submit'):
    #@st.cache
        df = excel_file_merge(uploaded_file)
        st.header('**Merged data**')
        st.write(df)
        st.markdown(filedownload(df), unsafe_allow_html=True)
        st.markdown(xldownload(df), unsafe_allow_html=True)
        
    else:
        st.write("")
        st.info('Awaiting for ZIP file to be uploaded.')
        st.image('5.png', width=700)            

    

           
    

    


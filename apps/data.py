import streamlit as st
import pandas as pd  
import plotly.express as px  
import base64  
from io import StringIO, BytesIO  
import numpy as np
import pandas as pd
from sklearn import datasets
import matplotlib.pyplot as plt

def app():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title('Data')
    def generate_excel_download_link(df):
        
        towrite = BytesIO()
        df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
        towrite.seek(0)  # reset pointer
        b64 = base64.b64encode(towrite.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
        return st.markdown(href, unsafe_allow_html=True)

    def generate_html_download_link(fig):
    
        towrite = StringIO()
        fig.write_html(towrite, include_plotlyjs="cdn")
        towrite = BytesIO(towrite.getvalue().encode())
        b64 = base64.b64encode(towrite.read()).decode()
        href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
        return st.markdown(href, unsafe_allow_html=True)


    #st.set_page_config(page_title='Excel Plotter')
    #st.title('Excel Plotter 📈')
   # st.subheader('Feed me with your Excel file')

    #df.columns.values.tolist()
    uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
    if uploaded_file:
        st.markdown('---')
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        st.dataframe(df)
        groupby_column = st.selectbox(
        'What would you like to analyse?',df.columns.values.tolist(),
    )

        groupby_column2 = st.selectbox(
        'Select column for further analysis',df.columns.values.tolist(),
    )
        

        # -- GROUP DATAFRAME
        output_columns = 'SCORE',groupby_column2
        df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()

    # -- PLOT DATAFRAME
        fig = px.bar(
            df_grouped,
            x=groupby_column,
            y='SCORE',
            color='SCORE',
            color_continuous_scale=['red', 'yellow', 'green'],
            template='plotly_white',
            title=f'<b>SCORE by {groupby_column}</b>'
            )
        st.plotly_chart(fig)
        
        df_grouped.hist()
        plt.show()
        st.pyplot()
        
        fig2 = px.area(
            df_grouped,
            x=groupby_column,
            y='SCORE',
            color='SCORE',
            template='plotly_white',
            title=f'<b>SCORE by {groupby_column}</b>'
            )
        st.plotly_chart(fig2)
      

    # -- DOWNLOAD SECTION
        st.subheader('Downloads:')
        generate_excel_download_link(df_grouped)
        generate_html_download_link(fig)
        
    else:
        st.write("")
        st.info('Awaiting for Exel File.')
        st.image('4.png', width=700) 
    
   
    

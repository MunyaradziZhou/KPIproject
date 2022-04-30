from pycaret.regression import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import plotly.express as px
import base64
import os
import io
from PIL import Image


def app():
    ccc=""
    ccc1=""
    ccc2=""
    ccc3=""
    ccc4=""
    ccc5=""
    ccc6=""
    ccc7=""
    ccc8=""
    ccc9=""

    model = load_model('Bongani5')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    def predict(model, input_df):
        predictions_df = predict_model(estimator=model, data=input_df)
        predictions = predictions_df['Label'][0]
        return predictions
        
    
    st.title("Productivity Prediction (Batch)")
    
    uploaded_file = st.file_uploader("Upload your input XLSX file", type=["xlsx"])

    if uploaded_file is not None:

        data =  pd.read_excel(uploaded_file,engine='openpyxl')
        predictions = predict_model(estimator=model,data=data)
        #st.write(predictions)
        df = st.dataframe(predictions)
        tapiwa1 = predictions['Label'].mean()
        tapiwa11 = predictions['AES Average'].mean()
        tapiwa12 = predictions['Calls'].mean()
        tapiwa13 = predictions['AHT'].mean()
        tapiwa14 = predictions['Adherance'].mean() 
        tapiwa15 = predictions['Unqualified'].mean()
        tapiwa2  = predictions.describe()
        tapiwa3 = predictions[predictions['Label'] >= 4.25]
        tapiwa4 = predictions[predictions['Label'] < 4.25]

        groupby_column = st.selectbox(
        'What would you like to analyse?',predictions.columns.values.tolist(),)
        output_columns = 'Label'
        tapiwa = predictions.groupby(by=[groupby_column], as_index=False)[output_columns].count()

        st.write("**OVERAL STATS**")
        st.table(tapiwa2)
        st.subheader("**AVERAGE PRODUCTIVITY SCORE : **" + str(tapiwa1))
        if tapiwa1 < 4.25:
            ccc="The average is below the standard, Lets minimize agents under the **low performance bracket**"
            st.error(ccc)
        elif tapiwa1 >= 4.25:
            ccc1="Our average productivity is trending positivily"
            st.success(ccc1)

        if tapiwa11 < 94:
            ccc2="AES is below the standard, Lets improve on **product knowledge**"
            st.error(ccc2)
        elif tapiwa11 >= 94:
            ccc3="Our AES is trending positivily"
            st.success(ccc3)


        if tapiwa12 < 200:
            ccc4="Calls are below the standard, Lets improve on reaching our **daily target calls**"
            st.error(ccc4)
        elif tapiwa12 >= 200:
            ccc5="Our Calls target is trending positivily"
            st.success(ccc5)

        if tapiwa13 > 2.5:
            ccc6="AHT is below the standard, Lets improve on reducing our **handling time**"
            st.error(ccc6)
        elif tapiwa13 <= 2.5:
            ccc7="Our ATH target is trending positivily"
            st.success(ccc7)

        if tapiwa14 < 98:
            ccc8="Adherance is below the standard, Lets login all times during  **working hours**"
            st.error(ccc8)
        elif tapiwa14 >= 98:
            ccc9="Our Adherance target is trending positivily"
            st.success(ccc9)

        st.write("                 ")
        
        st.write("***BEST PERFORMING AGENTS***")
        st.table(tapiwa3)
        st.write("***LOW PERFORMING AGENTS***")
        st.table(tapiwa4)

        add_selectbox1 = st.sidebar.selectbox(
    "Select your graph?",
    ("Pie", "Area", "Histogram","Scatter","Bar"))

        if add_selectbox1 == 'Pie':
            fig4 = px.pie(predictions, values=predictions['Label'], names=predictions[groupby_column])
            st.plotly_chart(fig4)
            
        if add_selectbox1 == 'Bar':

            fig = px.bar(
                
                tapiwa,
                x=groupby_column,
                y='Label',
                color='Label',
                color_continuous_scale=['red', 'yellow', 'green','blue'],
                template='plotly_white',
                title=f'<b>Predictions by {groupby_column}</b>'
                )
            st.plotly_chart(fig)

        if add_selectbox1 == 'Area':

            fig2 = px.area(
                tapiwa,
                x=groupby_column,
                y='Label',
                color='Label',
                template='plotly_white',
                title=f'<b>Prodictions by {groupby_column}</b>'
                )
            st.plotly_chart(fig2)

        if add_selectbox1 == 'Histogram':
            tapiwa.hist()
            plt.show()
            st.pyplot()

        if add_selectbox1 == 'Scatter':
            fig3 = px.scatter(
                x=predictions["Label"],
                y=predictions[groupby_column],
            )
            fig3.update_layout(
                xaxis_title="Predictions",
                yaxis_title=f'<b>{groupby_column}</b>',
        )
            st.write(fig3)

        

            
        dfs= pd.DataFrame(predictions)
        towrite = io.BytesIO()
        downloaded_file = dfs.to_excel(towrite, encoding='utf-8', index=False, header=True)
        towrite.seek(0)  # reset pointer
        b64 = base64.b64encode(towrite.read()).decode()  # some strings
        linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="myfilename.xlsx">Download excel file</a>'
        st.markdown(linko, unsafe_allow_html=True)

       

    else:
        st.write("")
        st.info('Awaiting for Exel File.')
        st.image('8.png', width=700) 

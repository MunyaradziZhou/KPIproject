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

    model = load_model('Bongani6')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    def predict(model, input_df):
        predictions_df = predict_model(estimator=model, data=input_df)
        predictions = predictions_df['Label'][0]
        return predictions
        
    
    st.title("CSAT Prediction (Batch)")
    
    uploaded_file = st.file_uploader("Upload your input XLSX file", type=["xlsx"])

    if uploaded_file is not None:

        data =  pd.read_excel(uploaded_file,engine='openpyxl')
        predictions = predict_model(estimator=model,data=data)
        #st.write(predictions)
        df = st.dataframe(predictions)
        output = predictions['Label'].mean()
        Recommendation = predictions['recommendation'].mean()
        Response = predictions['Response time'].mean()
        Friendliness = predictions['Friendliness'].mean()
        Follow = predictions['Following up'].mean() 
        tapiwa2  = predictions.describe()
        tapiwa3 = predictions[predictions['Label'] >= 8.5]
        tapiwa4 = predictions[predictions['Label'] < 8.5]

        Agents = predictions['Label'].count() 
        Answer = predictions['Answer'].mean() 
        Query = predictions['Query'].unique()


        score1 = round(Recommendation/10 * 22 ,0)
        score2 = round(Response/10 * 27, 0)
        score3 = round(Friendliness/10 * 16,0)
        score4 = round(Follow/10 * 35,0)
        ans1 = round(9/Follow * Agents)
        fol1 = round(ans1 * 15)
        ans = round(Answer)
        cal2 = round(Response * Agents)
        folv = round(15)


        groupby_column = st.selectbox(
        'What would you like to analyse?',predictions.columns.values.tolist(),)
        output_columns = 'Label'
        tapiwa = predictions.groupby(by=[groupby_column], as_index=False)[output_columns].count()

        st.write("**OVERAL STATS**")
        st.table(tapiwa2)
        st.subheader("**AVERAGE CSAT SCORE : **" + str(output))




        if output<8.5:
           # output = str(output)
            action="The CSAT score is low , training and adjustments are highly required"
            st.error(str(output) + '  ' + action)
        if output>=8.5:
           # output = str(output)
            action="The CSAT Score is in the recommended zone , Lets Aim for a higher score"
            st.success(str(output)+ '  ' + action)
       

        if Recommendation < 8.5: 
            st.write("**Recommendation**")    
            st.write("Insights : ") 
            reco= "Customers rate of recommending the bussiness is below standard :"
            csa = "We should increase our CSAT to a score above 85%"
            fo = " We should make sure we reach " + str(fol1) + " daily follow ups"
            st.warning(reco)
            st.warning(csa)
            st.warning(fo)
        if Response < 8.5:
            st.write("**Responce**")
            st.write("Insights : ")
            resp = "We should reduce our the response time :"
            cal2 = round(9/Response * Agents)
            ans = round(9/Response * Answer)
            in2 = "We should increase the number of agents from " + str(Agents) + " to " + str(cal2)
            in22 = str(cal2) + " Agents need proper training when handling " + str(Query) + " queries"
            in222 = str("We should increase our average answered calls to ") + str(ans)
            st.warning(resp)
            st.warning(in2)
            st.warning(in22)
            st.warning(in222)
        if Friendliness > 8:
            st.write("**Friendliness**")
            st.write("Insights : ")
            fren = "Aim to improve on Friendliness :"
            st.warning(fren)
        if Follow < 9:
            st.write("**Follow Up**")
            st.write("Insights : ")
            folv = round(fol1 / Agents,0)
            foll= "The company should focus more on follow ups (Hightest contributer to CSAT) :"
            fol2= "Lets aim to increase our follow ups to "+ str(fol1)
            folt = "Make sure each agent handles " + str(folv) + " query follow ups"
            st.warning(foll)
            st.warning(fol2)
            st.warning(folt)

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

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

model = load_model('Tapiwa_AI')
st.set_option('deprecation.showPyplotGlobalUse', False)
def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    return predictions

def run():
    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?",
    ("Real Time", "Batch"))
    add_selectbox1 = st.sidebar.selectbox(
    "Select your graph?",
    ("Bar", "Area", "Histogram","Scatter",Pie))
    st.title("Insurance Charges Prediction App")

    if add_selectbox == 'Real Time':
        gender = st.selectbox('gender', ['Male', 'Female'])
        SeniorCitizen = st.number_input('SeniorCitizen', 0,1)
        tenure = st.number_input('tenure', min_value=0, max_value=80, value=0)
        MultipleLines = st.selectbox('MultipleLines', ['Yes', 'No', 'No phone service'])
        
        InternetService = st.selectbox('InternetService', ['DSL', 'Fiber optic', 'No'])
        OnlineSecurity = st.selectbox('OnlineSecurity', ['Yes', 'No', 'No phone service'])
        OnlineBackup = st.selectbox('OnlineBackup', ['Yes', 'No', 'No phone service'])
        DeviceProtection = st.selectbox('DeviceProtection', ['Yes', 'No', 'No phone service'])

        TechSupport = st.selectbox('TechSupport', ['Yes', 'No', 'No phone service'])
        StreamingTV = st.selectbox('StreamingTV', ['Yes', 'No', 'No phone service'])
        StreamingMovies = st.selectbox('StreamingMovies', ['Yes', 'No', 'No phone service'])
        Contract = st.selectbox('Contract', ['Month-to-month', 'One year', 'Two year'])
        
        PaymentMethod = st.selectbox('PaymentMethod', ['Electronic check', 'Mailed check', 'Bank transfer (automatic)','Credit card (automatic)'])
        MonthlyCharges = st.number_input('MonthlyCharges', min_value=18.00, max_value=120.00, step=0.10)
        TotalCharges = st.number_input('TotalCharges', min_value=18.00, max_value=8700.00, step=1.00)
        if st.checkbox('Partner'):
            Partner = 'yes'
        else:
            Partner = 'no'

        if st.checkbox('Dependents'):
            Dependents = 'yes'
        else:
            Dependents = 'no'

        if st.checkbox('PhoneService'):
            PhoneService = 'yes'
        else:
            PhoneService = 'no'
        if st.checkbox('PaperlessBilling'):
            PaperlessBilling = 'yes'
        else:
            PaperlessBilling = 'no'
        

        output=""
        action=""

        input_dict = {'gender' : gender, 'SeniorCitizen' : SeniorCitizen, 'tenure' : tenure, 'MultipleLines' : MultipleLines, 'InternetService' : InternetService, 'OnlineSecurity' : OnlineSecurity
        ,'OnlineBackup' : OnlineBackup, 'DeviceProtection' : DeviceProtection, 'TechSupport' : TechSupport, 'StreamingTV' : StreamingTV, 'StreamingMovies' : StreamingMovies, 'Contract' : Contract,
        'PaymentMethod' : PaymentMethod, 'MonthlyCharges' : MonthlyCharges, 'TotalCharges' : TotalCharges, 'Partner' : Partner, 'Dependents' : Dependents, 'PhoneService' : PhoneService, 'PaperlessBilling' : PaperlessBilling}
        input_df = pd.DataFrame([input_dict])

        if st.button("Predict"):
            output = predict(model=model, input_df=input_df)
            
            if output==1:
                output = 'Arlet ! This customer has a high chance of leaving the business.' + '  ' +'The predicted outcome is :'+' '+str(output)
                action="Contact Risk !"
                st.error(output + '  ' + action)
            else:
                output = 'Great ! This customer is loyal to the business.' + '  ' +'The predicted outcome is :'+' '+str(output)
                st.success(output + '  ' + action)
        
    if add_selectbox == 'Batch':

        uploaded_file = st.file_uploader("Upload your input XLSX file", type=["xlsx"])

        if uploaded_file is not None:
            data =  pd.read_excel(uploaded_file,engine='openpyxl')
            predictions = predict_model(estimator=model,data=data)
            #st.write(predictions)
            df = st.dataframe(predictions)

            groupby_column = st.selectbox(
        'What would you like to analyse?',predictions.columns.values.tolist(),)
            output_columns = 'Label'
            tapiwa = predictions.groupby(by=[groupby_column], as_index=False)[output_columns].count()
            
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

            if add_selectbox1 == 'Pie':
                fig4 = px.pie(predictions, values=predictions['Label'], names=predictions[groupby_column])
                st.plotly_chart(fig4)

            

            


            

            

            dfs= pd.DataFrame(predictions)
            towrite = io.BytesIO()
            downloaded_file = dfs.to_excel(towrite, encoding='utf-8', index=False, header=True)
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode()  # some strings
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="myfilename.xlsx">Download excel file</a>'
            st.markdown(linko, unsafe_allow_html=True)

        



if __name__ == '__main__':
    run()

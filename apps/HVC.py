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

    st.sidebar.markdown("""# Select Model

""")

    path = st.sidebar.selectbox('Daily / Weekly', ('Daily_HVC', 'Weekly_HVC'))
    model = load_model(path)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    def predict(model, input_df):
        predictions_df = predict_model(estimator=model, data=input_df)
        predictions = predictions_df['Label'][0]
        return predictions

   
    st.title("HVC Productivity")
    st.sidebar.markdown("""# Select features

""")
    
    
    AES = st.sidebar.number_input('AES Average', min_value=0.0, max_value=100.0, value=0.0)
    CSAT = st.sidebar.number_input('CSAT', min_value=0.0, max_value=1000.0, value=0.0)
    Calls = st.sidebar.number_input('Calls', min_value=0.0, max_value=2000.0, value=0.0)
    TalkTime = st.sidebar.number_input('TalkTime (Hourly)', min_value=0.00, max_value=1000.00, value=0.00)
    Outbound = st.sidebar.number_input('Outbound', min_value=0.0, max_value=1000.0, value=0.0)
    Unquilified = st.sidebar.number_input('Unqualified', min_value=0.0, max_value=1000.0, value=0.0)
    
    
        

    output=""
    action=""
    aes1=""
    calls1=""
    ath1=""
    ad1=""
    un1=""
    if path == 'Daily_HVC':

        input_dict = {'AES' : AES, 'Calls' : Calls, 'DailyTalkTime' : TalkTime, 'Outbound' : Outbound, 'Unquilified' : Unquilified, 'CSAT' : CSAT}
        input_df = pd.DataFrame([input_dict])

    if path == 'Weekly_HVC':

        input_dict = {'AES' : AES, 'Total Calls' : Calls, 'TalkTime' : TalkTime, 'Outbound' : Outbound, 'Unquilified' : Unquilified, 'CSAT' : CSAT}
        input_df = pd.DataFrame([input_dict])
    

    if st.button("Predict"):
        output = predict(model=model, input_df=input_df)
        try:
            if output<1:
           # output = str(output)
                action="Your score is very low , training is needed ASAP"
                st.error(str(output) + '  ' + action)
            if 1<output<2:
           # output = str(output)
                action="Your score is low , training is needed ASAP"
                st.error(str(output)+ '  ' + action)
            if 2<=output<3:
           # output = str(output)
                action="Your score is low , training is needed ASAP"
                st.error(str(output) + '  ' + action)
            if 3<=output<4.25:
           # output = str(output)
                action="Your score is below the Company average , focus on reaching your targets"
                st.warning(str(output) + '  ' + action)
            if 4.25<=output<4.5:
            #output = str(output)
                action="Your score is, focus more on perfecting all your KPI"
                st.success(str(output) + '  ' + action)
            if 4.5<=output<=5:
                output = str(output)
                action="Your score is great, lets aim reaching the perfect score (5)"
                st.success(str(output) + '  ' + action)
        
            else:
                output = 5
                output = str(output)
                action="Perfect Score, Great !!!!!!!!!!!"
                st.success(str(output) + '  ' + action)

        except ValueError as err:
            pass   

        if AES<98:
            aes1= "Your AES is below the standard, improvent in needed"
            st.warning(aes1)
        if Calls <111:
            calls1= "You should improve in your daily calls to 112"
            st.warning(calls1)
        try:
            if path == 'Daily_HVC':
                if TalkTime < 4.33:
                    ath1= "Aim to increase your daily talk time"
                    st.warning(ath1)
            if path == 'Weekly_HVC':
                if TalkTime < 21.65:
                    ath1= "Aim to increase your weekly talk time"
                    st.warning(ath1)
        except ValueError as err:
            pass
        if Outbound < 15:
            ad1= "Make sure to reach 15 callbacks daily"
            st.warning(ad1)
        if CSAT < 85:
            un1= "Improve on your CSAT"
            st.warning(un1)
       

    else:
        st.write("")
        st.info('Awaiting for The prediction.')
        st.image('10.png', width=700)
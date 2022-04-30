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
#customer lifetime value.
#business-smart metric,taking into account the risk and reward proposition.
def app():
    model = load_model('Bongani5')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    def predict(model, input_df):
        predictions_df = predict_model(estimator=model, data=input_df)
        predictions = predictions_df['Label'][0]
        return predictions

   
    st.title("Productivity")
    st.sidebar.markdown("""# Select features

""")
    #{'apple':1, 'bat':2, 'car':3, 'pet':4}
    
    AES = st.sidebar.number_input('AES Average', min_value=0, max_value=100, value=0)
    Calls = st.sidebar.number_input('Calls', min_value=0, max_value=1000, value=0)
    ATH = st.sidebar.number_input('ATH', min_value=0, max_value=1000, value=0)
    Adherance = st.sidebar.number_input('Adherance', min_value=0, max_value=1000, value=0)
    Unqualified = st.sidebar.number_input('Unqualified', min_value=0, max_value=1000, value=0)
    
        

    output=""
    action=""

    input_dict = {'AES Average' : AES,'Calls': Calls,'ATH' : ATH, 'Adherance' : Adherance, 'Unqualified' : Unqualified}
    input_df = pd.DataFrame([input_dict])

    if st.button("Predict"):
        output = predict(model=model, input_df=input_df)
            
        if output>1:
            output = str(output)
            action="Prediction !"
            st.error(output + '  ' + action)
        else:
            output = str(output)
            st.success(output + '  ' + action)

    else:
        st.write("")
        st.info('Awaiting for The prediction.')
        st.image('10.png', width=700)
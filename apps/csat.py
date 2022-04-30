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
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
#customer lifetime value.
#business-smart metric,taking into account the risk and reward proposition.
def app():
    model = load_model('BossRas')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    def predict(model, input_df):
        predictions_df = predict_model(estimator=model, data=input_df)
        predictions = predictions_df['Label'][0]
        return predictions

   
    st.title("CSAT")
    st.sidebar.markdown("""# Select features
    
""")
    
    
    
    Recommendation = st.sidebar.number_input('Recommendation', min_value=0, max_value=10, value=0)
    Response = st.sidebar.number_input('Response Time', min_value=0, max_value=10, value=0)
    Friendliness = st.sidebar.number_input('Friendliness', min_value=0, max_value=10, value=0)
    Follow = st.sidebar.number_input('Follow Up', min_value=0, max_value=10, value=0)
    Day = st.selectbox('Day', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday'])
    Agents = st.sidebar.number_input('Number of Agents', min_value=0, value=0)
    Answer = st.sidebar.number_input('Answered Calls', min_value=0, value=0)
    Query = st.sidebar.text_input('Type of Query')
    
        

    output=""
    action=""
    reco=""
    resp=""
    fren=""
    foll=""
    

    input_dict = {'recommendation' : Recommendation, 'Response time' : Response, 'Friendliness' : Friendliness, 'Following up' : Follow}
    input_df = pd.DataFrame([input_dict])

    if st.button("Predict"):
        predictions = predict_model(estimator=model,data=input_df)
        output = round(predict(model=model, input_df=input_df),1)
        score1 = round(Recommendation/10 * 22 ,0)
        score2 = round(Response/10 * 27, 0)
        score3 = round(Friendliness/10 * 16,0)
        score4 = round(Follow/10 * 35,0)
        ans1 = round(9/Follow * Agents)
        fol1 = round(ans1 * 15)
        ans = round(Answer)
        cal2 = round(Response * Agents)
        folv = round(15)

        if output<8.5:
           # output = str(output)
            action="The CSAT score is low , training and adjustments are highly required"
            st.error(str(output) + '  ' + action)
        if output>=8.5:
           # output = str(output)
            action="The CSAT Score is in the recommended zone , Lets Aim for a higher score"
            st.success(str(output)+ '  ' + action)
       

        if Recommendation < 8.5: 
            st.write("Recommendation")    
            st.write("Insights : ") 
            reco= "Customers rate of recommending the bussiness is below standard :"
            csa = "We should increase our CSAT to a score above 85%"
            fo = " We should make sure we reach " + str(fol1) + " daily follow ups"
            st.warning(reco)
            st.warning(csa)
            st.warning(fo)
        if Response < 8.5:
            st.write("Responce")
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
            st.write("Friendliness")
            st.write("Insights : ")
            st.write("Friendliness : ")
            fren = "Aim to improve on Friendliness :"
            st.warning(fren)
        if Follow < 9:
            st.write("Follow Up")
            st.write("Insights : ")
            folv = round(fol1 / Agents,0)
            foll= "The company should focus more on follow ups (Hightest contributer to CSAT) :"
            fol2= "Lets aim to increase our follow ups to "+ str(fol1)
            folt = "Make sure each agent handles " + str(folv) + " query follow ups"
            st.warning(foll)
            st.warning(fol2)
            st.warning(folt)

        dat2 = pd.DataFrame({'Day':[Day],'Agents': [cal2], 'Follow Ups Required':[folv],'Calls No Required':[ans], 'Query':[Query]})
        dfs= pd.DataFrame(predictions) 
        dd = dat2.join(dfs)
        st.table(dd)
        dd.to_csv('C:/Users/Pc/Desktop/CSAT FILES/csat.csv', mode='a', index = False, header=False)
    
    else:
        st.write("")
        st.info('Awaiting for The prediction.')
        st.image('10.png', width=700)
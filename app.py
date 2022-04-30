# pip install openpyxl
import pandas as pd
import streamlit as st
import zipfile
import base64
import os
from PIL import Image
from multiapp import MultiApp
from apps import home, data, exapp, model, eda, customer2, cstomer1, productivity1, productivity, csat, csat1, test, HVC, Fresh_Chat, Fresh_Desk # import your app modules here
img = Image.open("unnamed.png")
app = MultiApp()

st.set_page_config(page_icon=img)
st.image('unnamed.png', width=200)

st.sidebar.markdown("""# DataScience App

""")
with st.sidebar.header(''):
    

    app.add_app("Home", home.app)
    #app.add_app("File Merger", exapp.app)
    app.add_app("EDA", eda.app)
    #app.add_app("Visuals & Reprts", data.app)
    #app.add_app("Real Time Customer Churn", cstomer1.app)
    #app.add_app("Batch Customer Churn", customer2.app)
    #app.add_app("Batch Poductivity", productivity1.app)
    app.add_app("LVC", productivity.app)
    app.add_app("HVC", HVC.app)
    app.add_app("Fresh Chat", Fresh_Chat.app)
    #app.add_app("Fresh Desk", Fresh_Desk.app)
    #app.add_app("Batch CSAT", csat1.app)
    app.add_app("Experiment", test.app)
   # app.add_app("Predictions", model.app)
    
    
    
    
st.markdown("""




""")
primaryColor = st.get_option("theme.primaryColor")
s = f"""
<style>
div.stButton > button:first-child {{ border: 10px solid {primaryColor};background-color: #6C63FF;color:white;font-size:16px;height:3em;width:18.5em; border-radius:5px 5px 5px 5px; }}
<style>
"""
st.markdown(s, unsafe_allow_html=True)
# Add all your application here

# The main app
app.run()

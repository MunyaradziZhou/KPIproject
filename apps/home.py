# pip install openpyxl
import pandas as pd
import streamlit as st
import zipfile
import base64
import os
from PIL import Image
from streamlit_lottie import st_lottie
import json
import requests





def app():
    st.title('Home')
    st.markdown("""
                ## Munya DataScience App.
                



---
""")

    st.write('')
    st.write('Welcome to business intelligence and reporting data tool')
    st.image('undraw_data_processing_yrrv.png', width=700)
  

import json
import os
import pandas as pd
import requests
from datetime import datetime, timedelta, date
import streamlit as st
import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(page_title="Dashboard!!!", page_icon=":bar_chart:",layout="wide")
st.markdown('<style>div.block-container{padding-top:5rem;}</style>',unsafe_allow_html=True)

st.sidebar.header("Select the Page : ")

with st.form(key='login_form'):
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    # Create a submit button
    submit_button = st.form_submit_button(label='Login')

# Check if the submit button was pressed
if submit_button:
    if username == "admin" and password == "password":  # Replace with your own logic
        st.success(f"Welcome, {username}!")
    else:
        st.error("Invalid username or password")




directory = 'Data/'
files = os.listdir(directory)
# st.write(files)
# st.write(files[0].split("_")[-1].split(".")[0])

for fls in files:
    st.write(fls.split("_")[-1].split(".")[0])
    write_date = fls.split("_")[-1].split(".")[0]
    dt = datetime.strptime(write_date,"%Y-%m-%d")
    if (datetime.today()-timedelta(days=1)) > dt:
        file_path = os.path.join(directory, fls)
        os.remove(file_path)
        st.write(f'file removed : {file_path}')
    else:
        st.write("False")

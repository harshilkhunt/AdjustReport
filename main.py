import json
import os
import pandas as pd
import requests
from datetime import datetime, timedelta, date
import streamlit as st
import plotly.express as px
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(page_title="Dashboard!!!", page_icon=":bar_chart:",layout="wide")
st.markdown('<style>div.block-container{padding-top:5rem;}</style>',unsafe_allow_html=True)


credentials = {
    'usernames': {
        st.secrets['username']: {
            'email': 'jsmith@gmail.com',
            'failed_login_attempts': 0,  # Will be managed automatically
            'logged_in': False,           # Will be managed automatically
            'name': 'Admin',
            'password':  st.secrets['pass'],            # Will be hashed automatically
            'roles': ['admin', 'editor', 'viewer']
        }
    }
}




# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days']
# )


authenticator = stauth.Authenticate(
    credentials,
    "Dashboard",
    "keyss",
    cookie_expiry_days=30
)

authenticator.login()

if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')


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
        # st.write(f'file removed : {file_path}')
    else:
        # st.write("False")

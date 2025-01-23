import os
import pandas as pd
import requests
from datetime import datetime, timedelta, date

import streamlit



lst_token ='"f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s","x4pi8tlg9gxs","pjrgtt69evi8","ie60raqfubr4","nxb5aof0yhog","owuxajwx277k","i0dznwr1glxc"'

today = datetime.today().date()
formatted_date = today.strftime('%Y-%m-%d')


sevendays = datetime.today().date() - timedelta(days =7)
sevendays_back = sevendays.strftime('%Y-%m-%d')
print(sevendays_back)

def fetch_adjust_report(tkn,date_period, dimensions, metrics,filename):

    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{filename}_{current_date}.csv"
    folder_path = 'Data'
    file_path = os.path.join(folder_path, filename)
    print(file_path)

    # Step 1: Check if the file exists
    if os.path.exists(file_path):
        print(f"The file {file_path} already exists. No API call will be made.")
        df = pd.read_csv(file_path)
        return df
    else:
        print(f"The file {file_path} does not exist. Making API call...")
        url = "https://automate.adjust.com/reports-service/report"
        params = {
             "ad_revenue_sources":"Applovin MAX SDK",
             "cost_mode": "network",
              "app_token__in": lst_token,
             "date_period": date_period,
              "dimensions": dimensions,
             "metrics": metrics,
             "readable_names":"true"

        }

        headers = {
            # "Authorization": "Bearer WWU3R_NVWshLX-h4yy4e"

            "Authorization": streamlit.secrets["auth_tkn"]
        }

        response = requests.get(url, params=params, headers=headers)
        jsn = response.json()
        df = pd.DataFrame(jsn['rows'])

        # Step: Save DataFrame to CSV

        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
        return df



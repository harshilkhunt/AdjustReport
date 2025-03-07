import api_call as ac
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if 'authentication_status' not in st.session_state or not st.session_state.authentication_status:
    st.info("Please login from the Home page and try again.")
    st.stop()


today = datetime.today().date()
today_date = today.strftime('%Y-%m-%d')
nth_day = 45
n_days = datetime.today().date() - timedelta(days = nth_day)
n_days_back = n_days.strftime('%Y-%m-%d')
print(n_days_back)





lst_token =["f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s"]

df = ac.fetch_adjust_report('"f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s","x4pi8tlg9gxs"',f"{n_days_back}:{today_date}","day,app","cost,retention_rate_d1,retention_rate_d7,retention_rate_d30,roas_d1,roas_d7,roas_d30","dashboard")
df['day'] = pd.to_datetime(df['day'])
unique_apps = df['app'].unique()

columns = ['app','cost', 'retention_rate_d1', 'retention_rate_d7', 'retention_rate_d30', 'roas_d1', 'roas_d7', 'roas_d30']
# Create an empty DataFrame with the specified columns
df_data = pd.DataFrame(columns=columns)
df_data['app'] =unique_apps




def calculate_cost(appname,data):
    n = datetime.today().date()
    start_date = n - pd.Timedelta(days=8)

    end_date = n - pd.Timedelta(days=2)

    # st.write(start_date)
    # st.write(end_date)
    # Filter rows between the dates
    df= data[data['app'] ==appname]
    filtered_df = df[(df['day'].dt.date >= start_date) & (df['day'].dt.date <= end_date)]
    # st.write(filtered_df)
    avg_cost = filtered_df['cost'].mean()
    avg_d1 = filtered_df['retention_rate_d1'].mean()
    avg_d1_roas = filtered_df['roas_d1'].mean()
    return avg_cost,avg_d1,avg_d1_roas

def calculate_d7(appname,data):
    n = datetime.today().date()
    start_date = n - pd.Timedelta(days=16)

    end_date = n - pd.Timedelta(days=9)

    # st.write(start_date)
    # st.write(end_date)
    # Filter rows between the dates
    df= data[data['app'] ==appname]
    filtered_df = df[(df['day'].dt.date >= start_date) & (df['day'].dt.date <= end_date)]
    # st.write(filtered_df)
    avg_d7 = filtered_df['retention_rate_d7'].mean()
    avg_d7_roas = filtered_df['roas_d7'].mean()
    return avg_d7,avg_d7_roas

def calculate_d30(appname,data):
    n = datetime.today().date()
    start_date = n - pd.Timedelta(days=38)

    end_date = n - pd.Timedelta(days=32)

    # st.write(start_date ,"d30")
    # st.write(end_date)
    # Filter rows between the dates
    df= data[data['app'] ==appname]
    filtered_df = df[(df['day'].dt.date >= start_date) & (df['day'].dt.date <= end_date)]
    # st.write(filtered_df)
    avg_d30 = filtered_df['retention_rate_d7'].mean()
    avg_d30_roas = filtered_df['roas_d7'].mean()
    return avg_d30,avg_d30_roas

def calculate_metrics(app_name,data):
    avg_cost, avg_d1, avg_d1_roas = calculate_cost(app_name,data)
    avg_d7, avg_d7_roas  = calculate_d7(app_name,data)
    avg_d30, avg_d30_roas = calculate_d30(app_name,data)
    cost = round(avg_cost,2)  # Example: cost based on app name length
    retention_rate_d1 = round(avg_d1 *100,2)  # Example calculation
    retention_rate_d7 = round(avg_d7*100,2)
    retention_rate_d30 = round(avg_d30*100,2)
    roas_d1 =round( avg_d1_roas,2)
    roas_d7 = round(avg_d7_roas,2)
    roas_d30 = round(avg_d30_roas,2)
    return cost, retention_rate_d1, retention_rate_d7, retention_rate_d30, roas_d1, roas_d7, roas_d30


# Iterate through each row in the empty DataFrame and calculate data dynamically
for index, row in df_data.iterrows():
    app_name = row['app']

    # Calculate metrics for the current app dynamically
    cost, retention_rate_d1, retention_rate_d7, retention_rate_d30, roas_d1, roas_d7, roas_d30 = calculate_metrics(
        app_name,df)

    # Fill the calculated values into the respective columns of the DataFrame
    df_data.at[index, 'cost'] = cost
    df_data.at[index, 'retention_rate_d1'] = retention_rate_d1
    df_data.at[index, 'retention_rate_d7'] = retention_rate_d7
    df_data.at[index, 'retention_rate_d30'] = retention_rate_d30
    df_data.at[index, 'roas_d1'] = roas_d1
    df_data.at[index, 'roas_d7'] = roas_d7
    df_data.at[index, 'roas_d30'] = roas_d30

st.write(df_data)


# -------------------------------------------------------------
st.divider()



df_country = ac.fetch_adjust_report('"f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s","x4pi8tlg9gxs"',f"{n_days_back}:{today_date}","day,app,country","cost,retention_rate_d1,retention_rate_d7,retention_rate_d30,roas_d1,roas_d7,roas_d30","dashboard_cntry")
options_country = st.selectbox("Select the Country", df_country['country'].unique())
df_country = df_country[df_country['country']==options_country]
# st.write(df_country)

df_country['day'] = pd.to_datetime(df_country['day'])
unique_apps_cntry = df_country['app'].unique()

columns_cntry = ['app','cost', 'retention_rate_d1', 'retention_rate_d7', 'retention_rate_d30', 'roas_d1', 'roas_d7', 'roas_d30']
# Create an empty DataFrame with the specified columns
df_data_country = pd.DataFrame(columns=columns_cntry)
df_data_country['app'] = unique_apps_cntry



# Iterate through each row in the empty DataFrame and calculate data dynamically
for index, row in df_data_country.iterrows():
    app_name = row['app']

    # Calculate metrics for the current app dynamically
    cost, retention_rate_d1, retention_rate_d7, retention_rate_d30, roas_d1, roas_d7, roas_d30 = calculate_metrics(
        app_name,df_country)

    # Fill the calculated values into the respective columns of the DataFrame
    df_data_country.at[index, 'cost'] = cost
    df_data_country.at[index, 'retention_rate_d1'] = retention_rate_d1
    df_data_country.at[index, 'retention_rate_d7'] = retention_rate_d7
    df_data_country.at[index, 'retention_rate_d30'] = retention_rate_d30
    df_data_country.at[index, 'roas_d1'] = roas_d1
    df_data_country.at[index, 'roas_d7'] = roas_d7
    df_data_country.at[index, 'roas_d30'] = roas_d30

st.write(df_data_country)









#
# n = datetime.today().date()
# start_date = n - pd.Timedelta(days=6)
# end_date = n - pd.Timedelta(days=3)
# # Filter rows between the dates
# filtered_df = df[(df['day'].dt.date >= start_date) & (df['day'].dt.date <= end_date)]
#
# st.write(filtered_df)
#



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
lst_token =["f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s"]
df_ltv = ac.fetch_adjust_report('"f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s"',f"2024-04-01:{today_date}","week,app,country","lifetime_value_d7,lifetime_value_d30,lifetime_value_d60","ltv")
df_ltv_day = ac.fetch_adjust_report('"f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s"',f"2024-04-01:{today_date}","day,app,country","lifetime_value_d1,lifetime_value_d2,lifetime_value_d3,lifetime_value_d7,lifetime_value_d14,lifetime_value_d30,lifetime_value_d60","ltv-day")

df_ltv['start_date'] = df_ltv['week'].str.split(' - ').str[0]

# Converting to datetime format
df_ltv['start_date'] = pd.to_datetime(df_ltv['start_date'])
# df_roas['start_date'] = df_roas['start_date'].dt.date


startDate = pd.to_datetime(df_ltv["start_date"]).min()
endDate = pd.to_datetime(df_ltv["start_date"]).max()#

col1, col2 = st.columns((2))
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

c1, c2 = st.columns((2))
with c1:
    options_app = st.selectbox("Select the App",df_ltv['app'].unique())
with c2:

    options_country = st.selectbox("Select the Country",df_ltv['country'].unique())



if date1 > date2:
    st.write("Enter correct date")
else:
    st.write("Entered Dates are correct")

# st.write(df_ltv)

df_filter = df_ltv[(df_ltv["start_date"] >= date1) & (df_ltv["start_date"] <= date2)].copy()
df_filter =df_filter[(df_filter['app']==options_app) & (df_filter['country']==options_country)]
df_filter['start_date'] = df_filter['start_date'].dt.date
df_filter  = df_filter.sort_values(by='start_date', ascending=True)
# st.write(df_filter)

st.divider()
fig_1 = go.Figure()

# Add first line
fig_1.add_trace(go.Scatter(x=df_filter['start_date'], y=df_filter['lifetime_value_d7'],  mode='lines+markers', name='LTV d7'))

# Add second line
fig_1.add_trace(go.Scatter(x=df_filter['start_date'], y=df_filter['lifetime_value_d30'], mode='lines+markers', name='LTV d30'))

# Add third line
fig_1.add_trace(go.Scatter(x=df_filter['start_date'], y=df_filter['lifetime_value_d60'], mode='lines+markers', name='LTV d60'))

# Update layout
fig_1.update_layout(title=f"LTVs of {options_app} in {options_country}",
                      xaxis_title='DAY',
                      yaxis_title='LTV usd$')
st.plotly_chart(fig_1, use_container_width=True)


df_ltv_day['day'] = pd.to_datetime(df_ltv_day['day'])

df_filter_ltv_day = df_ltv_day[(df_ltv_day["day"] >= date1) & (df_ltv_day["day"] <= date2)].copy()
df_filter_ltv_day =df_filter_ltv_day[(df_filter_ltv_day['app']==options_app) & (df_filter_ltv_day['country']==options_country)]
df_filter_ltv_day  = df_filter_ltv_day.sort_values(by='day', ascending=True)
# st.write(df_filter_ltv_day)

df_filter_ltv_day['lifetime_value_d1_rolling']=df_filter_ltv_day['lifetime_value_d1'].shift(1).rolling(window=7).mean()
df_filter_ltv_day['lifetime_value_d2_rolling']=df_filter_ltv_day['lifetime_value_d2'].shift(2).rolling(window=7).mean()
df_filter_ltv_day['lifetime_value_d3_rolling']=df_filter_ltv_day['lifetime_value_d3'].shift(3).rolling(window=7).mean()
df_filter_ltv_day['lifetime_value_d7_rolling']=df_filter_ltv_day['lifetime_value_d7'].shift(7).rolling(window=7).mean()
df_filter_ltv_day['lifetime_value_d14_rolling']=df_filter_ltv_day['lifetime_value_d14'].shift(14).rolling(window=7).mean()
df_filter_ltv_day['lifetime_value_d30_rolling']=df_filter_ltv_day['lifetime_value_d30'].shift(30).rolling(window=7).mean()
df_filter_ltv_day['lifetime_value_d60_rolling']=df_filter_ltv_day['lifetime_value_d60'].shift(60).rolling(window=7).mean()
df_filter_ltv_day['ltv'] = "Values"
df_filter_ltv_day = df_filter_ltv_day.drop(columns = ['lifetime_value_d1','lifetime_value_d2','lifetime_value_d3','lifetime_value_d7','lifetime_value_d14','lifetime_value_d30','lifetime_value_d60'])

# st.write(df_filter_ltv_day.tail(1))
df_plot = df_filter_ltv_day.tail(1).transpose()

new_header = df_plot.iloc[10]
df_plot = df_plot[3:10]     # Take the data less the header row
df_plot.columns = new_header     # Set the new header


# st.write(df_plot)

st.divider()
fig_2 = go.Figure()

# Add first line
fig_2.add_trace(go.Scatter(x=df_plot.index, y=df_plot['Values'],  mode='lines+markers',text= df_plot['Values'], name='LTV d7'))



# Update layout
fig_2.update_layout(title=f"LTVs of {options_app} in {options_country}",
                      xaxis_title='Days ltv',
                      yaxis_title='LTV usd$',
                      yaxis=dict(range=[0, max(df_plot["Values"]) + 2]))
st.plotly_chart(fig_2, use_container_width=True)



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
df_roas = ac.fetch_adjust_report('"f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s"',f"2024-04-01:{today_date}","week,app","retention_rate_d7,roas_d7,retention_rate_d30,roas_d30,retention_rate_d60,roas_d60","roas")

# Extracting the start date from the 'week' column
df_roas['start_date'] = df_roas['week'].str.split(' - ').str[0]

# Converting to datetime format
df_roas['start_date'] = pd.to_datetime(df_roas['start_date'])
# df_roas['start_date'] = df_roas['start_date'].dt.date


startDate = pd.to_datetime(df_roas["start_date"]).min()
endDate = pd.to_datetime(df_roas["start_date"]).max()#

col1, col2 = st.columns((2))
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

c1, c2 = st.columns((2))
with c1:
    options_app = st.selectbox("Select the App",df_roas['app'].unique())
with c2:
    pass



if date1 > date2:
    st.write("Enter correct date")
else:
    st.write("Entered Dates are correct")

# st.dataframe(df_roas)

df_filter = df_roas[(df_roas["start_date"] >= date1) & (df_roas["start_date"] <= date2)].copy()
df_filter =df_filter[df_roas['app']==options_app]
df_filter['start_date'] = df_filter['start_date'].dt.date
df_filter  = df_filter.sort_values(by='start_date', ascending=True)

# st.dataframe(df_filter)
st.divider()
fig_1 = go.Figure()
fig_1 = make_subplots(specs=[[{"secondary_y": True}]])
# Add a bar trace
fig_1.add_trace(go.Bar(x=df_filter["start_date"],y=df_filter["roas_d7"],name='roas_d7',marker_color='lightslategray'),secondary_y=False)

# Add a line trace
fig_1.add_trace(go.Scatter(x=df_filter["start_date"],y=df_filter["retention_rate_d7"],name='retention_rate_d7',mode='lines+markers',line=dict(color='royalblue')),secondary_y=True)

# Update layout for better presentation
fig_1.update_layout(
    title=f"Retention and Roas D7 for {options_app}",
    xaxis_title='Week',
    yaxis_title='Roas',
    yaxis2_title='retention_d7',
    barmode='group' , # This can be 'stack' or 'group' based on your preference
    yaxis=dict(range=[0, max(df_filter["roas_d7"]) + 0.5]),

)
fig_1.update_xaxes(tickmode='array', tickvals=df_filter["start_date"], ticktext=df_filter["start_date"], tickangle=45)
st.plotly_chart(fig_1, use_container_width=True)
st.divider()
fig_2 = go.Figure()
fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
# Add a bar trace
fig_2.add_trace(go.Bar(x=df_filter["start_date"],y=df_filter["roas_d30"],name='roas_d30',marker_color='lightslategray'),secondary_y=False)

# Add a line trace
fig_2.add_trace(go.Scatter(x=df_filter["start_date"],y=df_filter["retention_rate_d30"],name='retention_rate_d30',mode='lines+markers',line=dict(color='royalblue')),secondary_y=True)

# Update layout for better presentation
fig_2.update_layout(
    title=f"Retention and Roas D30 for {options_app}",
    xaxis_title='Week',
    yaxis_title='Roas',
    yaxis2_title='retention_d30',
    barmode='group' , # This can be 'stack' or 'group' based on your preference
    yaxis=dict(range=[0, max(df_filter["roas_d30"]) + 0.5]),

)
fig_2.update_xaxes(tickmode='array', tickvals=df_filter["start_date"], ticktext=df_filter["start_date"], tickangle=45)
st.plotly_chart(fig_2, use_container_width=True)
st.divider()
fig_3 = go.Figure()
fig_3= make_subplots(specs=[[{"secondary_y": True}]])
# Add a bar trace
fig_3.add_trace(go.Bar(x=df_filter["start_date"],y=df_filter["roas_d60"],name='roas_d60',marker_color='darkseagreen'),secondary_y=False)

# Add a line trace
fig_3.add_trace(go.Scatter(x=df_filter["start_date"],y=df_filter["retention_rate_d60"],name='retention_rate_d60',mode='lines+markers',line=dict(color='purple')),secondary_y=True)

# Update layout for better presentation
fig_3.update_layout(
    title=f"Retention and Roas D60 for {options_app}",
    xaxis_title='Week',
    yaxis_title='Roas',
    yaxis2_title='retention_d60',
    barmode='group' , # This can be 'stack' or 'group' based on your preference
    yaxis=dict(range=[0, max(df_filter["roas_d60"]) + 0.5]),

)
fig_3.update_xaxes(tickmode='array', tickvals=df_filter["start_date"], ticktext=df_filter["start_date"], tickangle=45)
st.plotly_chart(fig_3, use_container_width=True)
st.divider()
st.subheader("Time Spent per active user d7")
df_time_spent = ac.fetch_adjust_report('"f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s"',f"2024-06-01:{today_date}","week,app","time_spent_per_active_user_d7,retention_rate_d7","time_spent_d7")
df_time_spent['start_date'] = df_time_spent['week'].str.split(' - ').str[0]

# Converting to datetime format
df_time_spent['start_date'] = pd.to_datetime(df_time_spent['start_date'])

df_filter_time_spent = df_time_spent[(df_time_spent["start_date"] >= date1) & (df_time_spent["start_date"] <= date2)].copy()
df_filter_time_spent =df_filter_time_spent[df_time_spent['app']==options_app]
df_filter_time_spent['start_date'] = df_filter_time_spent['start_date'].dt.date
df_filter_time_spent  = df_filter_time_spent.sort_values(by='start_date', ascending=True)
# st.write(df_filter_time_spent)

fig_4 = go.Figure()
fig_4= make_subplots(specs=[[{"secondary_y": True}]])
# Add a bar trace
fig_4.add_trace(go.Bar(x=df_filter_time_spent["start_date"],y=df_filter_time_spent["time_spent_per_active_user_d7"],text=df_filter_time_spent["time_spent_per_active_user_d7"],name='time_spent_per_active_user_d7',marker_color='paleturquoise'),secondary_y=False)

# Add a line trace
fig_4.add_trace(go.Scatter(x=df_filter_time_spent["start_date"],y=df_filter_time_spent["retention_rate_d7"],text=df_filter_time_spent["retention_rate_d7"],name='retention_rate_d7',mode='lines+markers',line=dict(color='purple')),secondary_y=True)

# Update layout for better presentation
fig_4.update_layout(
    title=f"Time spent by active user D7 {options_app}",
    xaxis_title='Week',
    yaxis_title='Time Spent per active user d7',
    yaxis2_title='retention_d7',
    barmode='group' , # This can be 'stack' or 'group' based on your preference
    yaxis=dict(range=[0, max(df_filter_time_spent["time_spent_per_active_user_d7"]) + 1000]),

)
fig_4.update_xaxes(tickmode='array', tickvals=df_filter_time_spent["start_date"], ticktext=df_filter_time_spent["start_date"], tickangle=45)
st.plotly_chart(fig_4, use_container_width=True)
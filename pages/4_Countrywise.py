import api_call as ac
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


today = datetime.today().date()
today_date = today.strftime('%Y-%m-%d')
sevendays = datetime.today().date() - timedelta(days =9)
sevendays_back = sevendays.strftime('%Y-%m-%d')
print(sevendays_back)
fourteendays = datetime.today().date() - timedelta(days =16)
fourteendays_back = fourteendays.strftime('%Y-%m-%d')
print(fourteendays_back)


lst_token =["f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s"]

df_countrywise = ac.fetch_adjust_report('"f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s"',f"{fourteendays_back}:{sevendays_back}","country,app","installs,daus,retention_rate_d7,roas_d7,cost","countrywise")
df_countrywise['cost'] = df_countrywise['cost'].astype(float)

col_1_1,col_1_2 = st.columns((2))
with col_1_1:
    pass
    my_slider_val = st.slider("Weekly Cost", min(df_countrywise['cost']), max(df_countrywise['cost']))
    st.write(my_slider_val)
with col_1_2:
    options_app = st.selectbox("Select the App", df_countrywise['app'].unique())
# st.write(df_countrywise)
#
df_filter = df_countrywise[(df_countrywise["cost"] >= my_slider_val) & (df_countrywise["app"] == options_app)].copy()
# st.write(df_filter)


st.divider()
fig_1 = go.Figure()
fig_1 = make_subplots(specs=[[{"secondary_y": True}]])
# Add a bar trace
fig_1.add_trace(go.Bar(x=df_filter["country"],y=df_filter["roas_d7"],name='roas_d7',text=df_filter["roas_d7"],marker_color='rosybrown'),secondary_y=False)

# Add a line trace
fig_1.add_trace(go.Scatter(x=df_filter["country"],y=df_filter["retention_rate_d7"],name='retention_rate_d7',mode='lines+markers',line=dict(color='royalblue')),secondary_y=True)

# Update layout for better presentation
fig_1.update_layout(
    title=f"Retention and Roas D7 for {options_app}",
    xaxis_title='Week',
    yaxis_title='Roas',
    yaxis2_title='retention_d7',
    barmode='group' , # This can be 'stack' or 'group' based on your preference
    yaxis=dict(range=[0, max(df_filter["roas_d7"]) + 0.5]),

)
fig_1.update_xaxes(tickmode='array', tickvals=df_filter["country"], ticktext=df_filter["country"], tickangle=45)
st.plotly_chart(fig_1, use_container_width=True)
# st.divider()
# fig_2 = go.Figure()
# fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
# # Add a bar trace
# fig_2.add_trace(go.Bar(x=df_filter["start_date"],y=df_filter["roas_d30"],name='roas_d30',marker_color='lightslategray'),secondary_y=False)
#
# # Add a line trace
# fig_2.add_trace(go.Scatter(x=df_filter["start_date"],y=df_filter["retention_rate_d30"],name='retention_rate_d30',mode='lines+markers',line=dict(color='royalblue')),secondary_y=True)
#
# # Update layout for better presentation
# fig_2.update_layout(
#     title=f"Retention and Roas D30 for {options_app}",
#     xaxis_title='Week',
#     yaxis_title='Roas',
#     yaxis2_title='retention_d30',
#     barmode='group' , # This can be 'stack' or 'group' based on your preference
#     yaxis=dict(range=[0, max(df_filter["roas_d30"]) + 0.5]),
#
# )
# fig_2.update_xaxes(tickmode='array', tickvals=df_filter["start_date"], ticktext=df_filter["start_date"], tickangle=45)
# st.plotly_chart(fig_2, use_container_width=True)
# st.divider()
# fig_3 = go.Figure()
# fig_3= make_subplots(specs=[[{"secondary_y": True}]])
# # Add a bar trace
# fig_3.add_trace(go.Bar(x=df_filter["start_date"],y=df_filter["roas_d60"],name='roas_d60',marker_color='darkseagreen'),secondary_y=False)
#
# # Add a line trace
# fig_3.add_trace(go.Scatter(x=df_filter["start_date"],y=df_filter["retention_rate_d60"],name='retention_rate_d60',mode='lines+markers',line=dict(color='purple')),secondary_y=True)
#
# # Update layout for better presentation
# fig_3.update_layout(
#     title=f"Retention and Roas D60 for {options_app}",
#     xaxis_title='Week',
#     yaxis_title='Roas',
#     yaxis2_title='retention_d60',
#     barmode='group', # This can be 'stack' or 'group' based on your preference
#     yaxis=dict(range=[0, max(df_filter["roas_d60"]) + 0.5]),
#
# )
# fig_3.update_xaxes(tickmode='array', tickvals=df_filter["start_date"], ticktext=df_filter["start_date"], tickangle=45)
# st.plotly_chart(fig_3, use_container_width=True)
#
# df_filter_rev = df_roas_country[(df_roas_country["start_date"] >= date1) & (df_roas_country["start_date"] <= date2)].copy()
# df_filter_rev =df_filter_rev[(df_filter_rev['app']==options_app) & (df_filter_rev['country']==options_country)]
# df_filter_rev['start_date'] = df_filter_rev['start_date'].dt.date
# df_filter_rev  = df_filter_rev.sort_values(by='start_date', ascending=True)
# df_filter_rev['total_revenue'] = df_filter_rev['revenue'] + df_filter_rev['ad_revenue']
#
# # st.write(df_filter_rev)
#
# st.divider()
# fig_4 = go.Figure()
#
# # Add a bar trace
# fig_4.add_trace(go.Bar(x=df_filter_rev["start_date"],y=df_filter_rev["cost"],name='Cost',marker_color='darkseagreen'))
#
# # Add a line trace
# fig_4.add_trace(go.Scatter(x=df_filter_rev["start_date"],y=df_filter_rev["total_revenue"],name='Total Revenue',mode='lines+markers',line=dict(color='purple')))
#
# # Update layout for better presentation
# fig_4.update_layout(
#     title=f"Revenue and Cost for {options_app} in {options_country}",
#     xaxis_title='Week',
#     yaxis_title='USD $',
#     barmode='group', # This can be 'stack' or 'group' based on your preference
#     yaxis=dict(range=[0, max(df_filter_rev["total_revenue"]) + 500]),
#
# )
# fig_4.update_xaxes(tickmode='array', tickvals=df_filter_rev["start_date"], ticktext=df_filter_rev["start_date"], tickangle=45)
# st.plotly_chart(fig_4, use_container_width=True)
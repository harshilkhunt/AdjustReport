import api_call as ac
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


today = datetime.today().date()
today_date = today.strftime('%Y-%m-%d')
lst_token =["f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s"]
df_ltv = ac.fetch_adjust_report('"f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s"',f"2024-04-01:{today_date}","week,app,country","lifetime_value_d7,lifetime_value_d30,lifetime_value_d60","ltv")

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
fig_1.add_trace(go.Scatter(x=df_filter['start_date'], y=df_filter['lifetime_value_d7'], mode='lines', name='LTV d7'))

# Add second line
fig_1.add_trace(go.Scatter(x=df_filter['start_date'], y=df_filter['lifetime_value_d30'], mode='lines', name='LTV d30'))

# Add third line
fig_1.add_trace(go.Scatter(x=df_filter['start_date'], y=df_filter['lifetime_value_d60'], mode='lines', name='LTV d60'))

# Update layout
fig_1.update_layout(title=f"LTVs of {options_app} in {options_country}",
                      xaxis_title='DAY',
                      yaxis_title='LTV usd$')
st.plotly_chart(fig_1, use_container_width=True)



# Sample DataFrame with date index
data = {
    'date': pd.date_range(start='2024-01-01', periods=10),
    'values': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
}
df = pd.DataFrame(data).set_index('date')

# Define the number of days to skip
days_to_skip = 3

# Calculate rolling mean while skipping the most recent days
df['rolling_mean'] = df['values'].shift(days_to_skip).rolling(window=5).mean()

# Display the DataFrame
st.write(df)
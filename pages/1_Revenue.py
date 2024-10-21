import api_call as ac
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Revenue!!!", page_icon=":bar_chart:",layout="wide")

if 'authentication_status' not in st.session_state or not st.session_state.authentication_status:
    st.info("Please login from the Home page and try again.")
    st.stop()

today = datetime.today().date()
seven_day_back = datetime.today().date()-pd.Timedelta(days=7)
today_date = today.strftime('%Y-%m-%d')
seven_day_back_date = seven_day_back.strftime('%Y-%m-%d')
lst_token =["f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s"]
df_revenue = ac.fetch_adjust_report('"f56a8zluprsw","1gymy6f2kfeo","mf30wj2dii9s"',f"2024-04-01:{today_date}", "day,country,app","installs,revenue,ad_revenue,cost,ecpi_all,daus,paid_installs,arpdau,arpdau_ad,arpdau_iap","revenue")
df_revenue[['installs', 'revenue', 'ad_revenue', 'cost', 'ecpi_all', 'daus', 'paid_installs', 'arpdau', 'arpdau_ad','arpdau_iap']] = df_revenue[['installs', 'revenue', 'ad_revenue', 'cost', 'ecpi_all', 'daus', 'paid_installs', 'arpdau', 'arpdau_ad','arpdau_iap']].astype(float)
df_revenue['total_revenue'] = df_revenue['revenue'] + df_revenue['ad_revenue']
df_revenue['day'] = pd.to_datetime(df_revenue['day'])





startDate = pd.to_datetime(df_revenue["day"]).min()
endDate = pd.to_datetime(df_revenue["day"]).max()


col1, col2 = st.columns((2))
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))


c1, c2 = st.columns((2))
with c1:
    options_app = st.multiselect("Select the App",df_revenue['app'].unique(),df_revenue['app'].unique()[0])
with c2:
    pass



if date1 > date2:
    st.write("Enter correct date")
else:
    st.write("correct date")

# st.dataframe(df_revenue)

df_filter = df_revenue[(df_revenue["day"] >= date1) & (df_revenue["day"] <= date2)].copy()
df_filter =df_filter[df_filter['app'].isin(options_app)]
df_filter = df_filter.groupby(by = 'day')[['installs','revenue','ad_revenue','cost','daus','paid_installs','total_revenue']].sum()


cl1,cl2 = st.columns([2,1])
with cl1:
    st.subheader("Chart")
    fig = px.line(x=df_filter.index, y=df_filter['total_revenue'], labels=dict(x="Day", y="Total Revenue", color="Time Period"),text=df_filter['total_revenue'].round())
    fig.add_bar(x=df_filter.index, y=df_filter['cost'],text=df_filter['cost'].round())
    st.plotly_chart(fig, use_container_width=True)

with cl2:
    st.subheader(f"Table for {options_app}")
    st.dataframe(df_filter)


cl_3_1,cl_3_2 = st.columns([1,1])
with cl_3_1:
    st.subheader("ARPDAU")
    option_country = st.selectbox("Select Country",df_revenue['country'].unique())
    option_app = st.selectbox("Select the App",df_revenue['app'].unique())
    df_arpdau = df_revenue[(df_revenue["day"] >= date1) & (df_revenue["day"] <= date2)].copy()
    df_arpdau = df_arpdau[(df_arpdau['app'] == option_app) & (df_arpdau['country'] == option_country)]
    df_arpdau  = df_arpdau.sort_values(by='day', ascending=True)

    # st.write(df_arpdau)
    # Create a figure
    fig = go.Figure()

    # Add first line
    fig.add_trace(go.Scatter(x=df_arpdau['day'], y=df_arpdau['arpdau'], mode='lines', name='Total ARPDAU'))

    # Add second line
    fig.add_trace(go.Scatter(x=df_arpdau['day'], y=df_arpdau['arpdau_ad'], mode='lines', name='ARPDAU Ads'))

    # Add third line
    fig.add_trace(go.Scatter(x=df_arpdau['day'], y=df_arpdau['arpdau_iap'], mode='lines', name='ARPDAY IAPs'))

    # Update layout
    fig.update_layout(title='ARPDAU',
                      xaxis_title='DAY',
                      yaxis_title='ARPDAU')
    st.plotly_chart(fig, use_container_width=True)

with cl_3_2:
    st.subheader("Install/DAU")
    # Create a figure
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add first line (primary Y-axis)
    fig.add_trace(go.Scatter(x=df_arpdau['day'], y=df_arpdau['installs'], mode='lines', name='installs'), secondary_y=False)

    # Add second line (primary Y-axis)
    fig.add_trace(go.Scatter(x=df_arpdau['day'], y=df_arpdau['paid_installs'], mode='lines', name='paid_installs'), secondary_y=False)

    # Add third line (secondary Y-axis)
    fig.add_trace(go.Scatter(x=df_arpdau['day'], y=df_arpdau['daus'], mode='lines', name='daus'),secondary_y=False)

    fig.add_trace(go.Scatter(x=df_arpdau['day'], y=df_arpdau['installs']/df_arpdau['daus']*100, mode='lines', name='Installs/Daus (Secondary Y-axis)'),secondary_y=True)

    # Update layout
    fig.update_layout(title='Installs / Daus',
                      xaxis_title='Day',
                      yaxis_title='Installs,Daus,Paid Installs',
                      yaxis2_title='Ratio Installs/Daus')
    st.plotly_chart(fig, use_container_width=True)

    fig_ecpi = go.Figure()

    # Add first line
    fig_ecpi.add_trace(go.Scatter(x=df_arpdau['day'], y=df_arpdau['ecpi_all'], mode='lines', name='ecpi'))
    fig_ecpi.update_layout(title='eCPI',
                      xaxis_title='Day',
                      yaxis_title='ecpi')
    st.plotly_chart(fig_ecpi, use_container_width=True)

st.divider()





cl_4_1,cl_4_2 = st.columns([1,1])
with cl_4_1:
    get_app = st.selectbox("Select  App", df_revenue['app'].unique())
with cl_4_2:
    df_rev_lst = df_revenue[(df_revenue["day"] >= seven_day_back_date) & (df_revenue["day"] <= today_date)].copy()
    df_rev_lst = df_rev_lst[df_rev_lst['app'] == get_app]
    df_rev_lst = df_rev_lst.groupby('country')['cost'].mean()
    # st.write(df_rev_lst)

    df_rev_lst = pd.DataFrame(df_rev_lst)

    df_rev_lst_sorted = df_rev_lst.sort_values(by='cost', ascending=False)
    df_rev_lst_sorted = df_rev_lst_sorted.head(10)
    cntry_lst = df_rev_lst_sorted.index.values.tolist()
    # st.write(cntry_lst)
    options_cntry = st.multiselect("Select the Country : By default top 10 country by spend in last 7 days", df_revenue['country'].unique(), cntry_lst)
# st.write(df_revenue)







df_rev_dau  = df_revenue[(df_revenue["day"] >= date1) & (df_revenue["day"] <= date2)].copy()
df_rev_dau =df_rev_dau[df_rev_dau['country'].isin(options_cntry) & (df_rev_dau['app'] == get_app)]
df_rev_dau = df_rev_dau.groupby(by = 'day')[['installs','revenue','ad_revenue','cost','daus','paid_installs','total_revenue']].sum()
df_rev_dau['Rev/Dau'] = df_rev_dau['total_revenue'] / df_rev_dau['daus']
df_rev_dau['rolling_average'] = df_rev_dau['Rev/Dau'].rolling(window=7).mean()
# st.write(df_rev_dau)

fig_4 = go.Figure()

# Add first line
fig_4.add_trace(go.Scatter(x=df_rev_dau.index, y=df_rev_dau['Rev/Dau'], mode='lines', name='Rev/Dau'))
fig_4.add_trace(go.Scatter(x=df_rev_dau.index, y=df_rev_dau['rolling_average'], mode='lines',marker_color='orangered', name='rolling_average 7 days'))

# Update layout
fig_4.update_layout(title=f'Rev/Dau in {options_cntry}',
                  xaxis_title='DAY',
                  yaxis_title='Rev/Dau')
st.plotly_chart(fig_4, use_container_width=True)
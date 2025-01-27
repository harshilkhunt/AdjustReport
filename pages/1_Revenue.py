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
lst_token = ac.lst_token
st.write(lst_token)
df_revenue = ac.fetch_adjust_report(lst_token,f"2024-02-01:{today_date}", "day,country,app","installs,revenue,ad_revenue,cost,ecpi_all,daus,paid_installs,arpdau,arpdau_ad,arpdau_iap","revenue")
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
    st.write('Default Dates')
    c1_1, c2_1,c3_1, c4_1, c5_1 = st.columns((5))
    with c1_1:
        if st.button("Last 7 Days"):
            date1 =  pd.to_datetime(datetime.now() - timedelta(days=7))
            # st.write(f'clicked:{startDate}  :  {date1}')
    with c2_1:
        if st.button("Last 14 Days"):
            date1 =  pd.to_datetime(datetime.now() - timedelta(days=14))
            # st.write(f'clicked:{startDate}  :  {date1}')
    with c3_1:
        if st.button("Last 30 Days"):
            date1 =  pd.to_datetime(datetime.now() - timedelta(days=30))
            # st.write(f'clicked:{startDate}  :  {date1}')
    with c4_1:
        if st.button("Last 60 Days"):
            date1 =  pd.to_datetime(datetime.now() - timedelta(days=60))
            # st.write(f'clicked:{startDate}  :  {date1}')
    with c5_1:
        if st.button("Last 90 Days"):
            date1 =  pd.to_datetime(datetime.now() - timedelta(days=90))
            # st.write(f'clicked:{startDate}  :  {date1}')



if date1 > date2:
    st.write("Enter correct date")
else:
    st.write("correct date")

# st.dataframe(df_revenue)

df_filter = df_revenue[(df_revenue["day"] >= date1) & (df_revenue["day"] <= date2)].copy()
df_filter =df_filter[df_filter['app'].isin(options_app)]
df_filter = df_filter.groupby(by = 'day')[['installs','revenue','ad_revenue','cost','daus','paid_installs','total_revenue']].sum()



st.subheader("Revenue v/s Spend Chart")
fig = px.line(x=df_filter.index, y=df_filter['total_revenue'], labels=dict(x="Day", y="Total Revenue", color="Time Period"),text=df_filter['total_revenue'].round())
fig.add_bar(x=df_filter.index, y=df_filter['cost'],text=df_filter['cost'].round())
st.plotly_chart(fig, use_container_width=True)



st.divider()
def game_data(name):
    cl_3_1,cl_3_2,cl_3_3 = st.columns([1,1,1])
    with cl_3_1:
        st.subheader(f"ARPDAU For {name}")
        st_date  =  pd.to_datetime(datetime.now() - timedelta(days=7))
        ed_date = date2
        df_arpdau = df_revenue[(df_revenue["day"] >= st_date) & (df_revenue["day"] <= ed_date)].copy()
        df_arpdau = df_arpdau[(df_arpdau['app'] == name) ]

        df_arpdau = df_arpdau.groupby(by='country')[['arpdau','cost','arpdau_ad','arpdau_iap','installs','paid_installs','daus','ecpi_all']].mean()
        df_arpdau = df_arpdau.sort_values(by='cost', ascending=False)
        df_arpdau = df_arpdau.head(7)
        # st.write(df_arpdau)
        # Create a figure
        fig = go.Figure()

        # Add first line
        fig.add_trace(go.Bar(x=df_arpdau.index, y=df_arpdau['arpdau'],name='arpdau',marker_color='firebrick'))

        # Add second line
        fig.add_trace(go.Bar(x=df_arpdau.index, y=df_arpdau['arpdau_ad'], name='arpdau_ad',marker_color='darkolivegreen'))

        # Add third line
        fig.add_trace(go.Bar(x=df_arpdau.index, y=df_arpdau['arpdau_iap'], name='arpdau_iap',marker_color='peru'))

        # Update layout
        fig.update_layout(title='ARPDAU',
                          xaxis_title='DAY',
                          yaxis_title='ARPDAU',
                            legend = dict(
                                 orientation="h",  # Horizontal orientation
                                    yanchor="bottom",  # Anchor to the bottom of the legend
                                    y=1.1,  # Position above the plot area
                                    xanchor="center",  # Center the legend horizontally
                                     x=0.5  # Center position (0 to 1)
                                 )
        )
        st.plotly_chart(fig, use_container_width=True)
    with cl_3_2:
        st.subheader("Install/DAU")
        # Create a figure
        # Create figure with secondary y-axis
        fig_i_d = make_subplots(specs=[[{"secondary_y": True}]])

        # Add first line (primary Y-axis)
        fig_i_d.add_trace(go.Bar(x=df_arpdau.index, y=df_arpdau['installs'], name='Installs', marker_color='firebrick'),secondary_y=False)

        # Add second line (primary Y-axis)
        fig_i_d.add_trace(go.Bar(x=df_arpdau.index, y=df_arpdau['paid_installs'], marker_color='mediumseagreen', name='paid_installs'), secondary_y=False)

        # Add third line (secondary Y-axis)
        fig_i_d.add_trace(go.Bar(x=df_arpdau.index, y=df_arpdau['daus'], marker_color='darkolivegreen', name='daus'),secondary_y=False)

        fig_i_d.add_trace(go.Scatter(x=df_arpdau.index, y=df_arpdau['installs'] / df_arpdau['daus'] * 100, marker_color='rosybrown', mode='lines',name='Installs/Daus (Secondary Y-axis)'), secondary_y=True)
        # fig.add_trace(go.scatter(x=))

        # Update layout
        fig_i_d.update_layout(title='Installs / Daus',
                          xaxis_title='Day',
                          yaxis_title='Installs,Daus,Paid Installs',
                          yaxis2_title='Ratio Installs/Daus',
                            legend=dict(
                                  orientation="h",  # Horizontal orientation
                                  yanchor="bottom",  # Anchor to the bottom of the legend
                                  y=1.1,  # Position above the plot area
                                  xanchor="center",  # Center the legend horizontally
                                  x=0.5  # Center position (0 to 1)
                              ))
        st.plotly_chart(fig_i_d, use_container_width=True)
    with cl_3_3:
        st.subheader("eCPI")
        fig_ecpi = go.Figure()
        # Add first line
        fig_ecpi.add_trace(go.Bar(x=df_arpdau.index, y=df_arpdau['ecpi_all'], marker_color='rosybrown', name='ecpi'))
        fig_ecpi.update_layout(title='eCPI',
                          xaxis_title='Day',
                          yaxis_title='ecpi',
                               legend=dict(
                                   orientation="h",  # Horizontal orientation
                                   yanchor="bottom",  # Anchor to the bottom of the legend
                                   y=1.1,  # Position above the plot area
                                   xanchor="center",  # Center the legend horizontally
                                   x=0.5  # Center position (0 to 1)
                               ))
        st.plotly_chart(fig_ecpi, use_container_width=True)

st.divider()


game_data('Merge Fever')
st.divider()
game_data('Merge HomeTown')
st.divider()
game_data('Tales and Dragon')
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

df_rev_dau['Ad_Rev/Dau'] = df_rev_dau['ad_revenue'] / df_rev_dau['daus']
df_rev_dau['rolling_average_ad'] = df_rev_dau['Ad_Rev/Dau'].rolling(window=7).mean()

df_rev_dau['IAP_Rev/Dau'] = df_rev_dau['revenue'] / df_rev_dau['daus']
df_rev_dau['rolling_average_IAP'] = df_rev_dau['IAP_Rev/Dau'].rolling(window=7).mean()
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

fig_5 = go.Figure()

# Add first line
fig_5.add_trace(go.Scatter(x=df_rev_dau.index, y=df_rev_dau['Ad_Rev/Dau'], mode='lines', name='AD_Rev/Dau'))
fig_5.add_trace(go.Scatter(x=df_rev_dau.index, y=df_rev_dau['rolling_average_ad'], mode='lines',marker_color='orangered', name='rolling_average 7 days'))

# Update layout
fig_5.update_layout(title=f'AD_Rev/Dau in {options_cntry}',
                  xaxis_title='DAY',
                  yaxis_title='AD_Rev/Dau')
st.plotly_chart(fig_5, use_container_width=True)

fig_6 = go.Figure()

# Add first line
fig_6.add_trace(go.Scatter(x=df_rev_dau.index, y=df_rev_dau['IAP_Rev/Dau'], mode='lines', name='IAP_Rev/Dau'))
fig_6.add_trace(go.Scatter(x=df_rev_dau.index, y=df_rev_dau['rolling_average_IAP'], mode='lines',marker_color='orangered', name='rolling_average 7 days'))

# Update layout
fig_6.update_layout(title=f'IAP_Rev/Dau in {options_cntry}',
                  xaxis_title='DAY',
                  yaxis_title='IAP_Rev/Dau')
st.plotly_chart(fig_6, use_container_width=True)
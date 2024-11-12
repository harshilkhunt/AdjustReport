import pandas as pd
import streamlit as st

st.set_page_config(page_title="Stack!!!", page_icon=":bar_chart:",layout="wide")
st.title("Ads Stack visualizer")




# Create a sidebar for file upload
with st.sidebar:
    st.header("Upload your file")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Determine the file type and read it into a DataFrame
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file type.")
        except Exception as e:
            st.error(f"Error reading the file: {e}")

        # Display the DataFrame in the main area

# st.write("DataFrame:")
# st.dataframe(df)

app_selected = st.selectbox("Select App",df['Application'].unique())

df_app_selected = df[df['Application'] == app_selected]

df_organic = df.copy()
df_ct = df.copy()
# st.write(df_app_selected)

ad_unit_name = df_app_selected['Ad Unit Name'].unique()
no_of_ad_units  = len(ad_unit_name)
# st.write(ad_unit_name)



cntry_option = st.selectbox("Select Country",df_app_selected['Country'].unique())
st.divider()

columns = st.columns(no_of_ad_units)

st.divider()


for i in range(no_of_ad_units):
    with columns[i]:
        st.markdown(f"Ad Unit - {ad_unit_name[i]}")
        if st.button(f"Click Here - {i+1}"):
            df_filter =df_app_selected[(df_app_selected['Ad Unit Name'] == ad_unit_name[i]) & (df_app_selected['Country']== cntry_option)]
            df_all_type = df_filter.copy()
            df_filter = df_filter[df_filter['Network Type'] != 'Bidding']

df_filter['%ile_Impr'] = df_filter['Impressions'].rank(pct=True)*100

df_filter['%ile_Rev'] = df_filter['Est. Revenue'].rank(pct=True)*100
st.write(df_filter)

cl1_1,cl1_2,cl1_3,cl1_4 = st.columns(4)
with cl1_1:
    st.subheader(f"All network for {df_all_type['Ad Unit Name'].unique()}")
    network_wise_all = df_all_type.groupby('Network')['Est. Revenue'].sum()
    st.write(network_wise_all)
with cl1_2:
    st.subheader(f"Nonbidding network for {df_filter['Ad Unit Name'].unique()}")
    network_wise = df_filter.groupby('Network')['Est. Revenue'].sum()
    st.write(network_wise)
with cl1_3:
    st.subheader(f"Rev Split for {df_filter['Ad Unit Name'].unique()}")
    bidding_wise = df_all_type.groupby('Network Type')['Est. Revenue'].sum()
    st.write(bidding_wise)
with cl1_4:
    st.subheader(f"Rev Split b/w ad Units")
    df_organic_cntry = df_app_selected[df_app_selected['Country']== cntry_option]
    unit_wise_all = df_organic_cntry.groupby('Ad Unit Name')['Est. Revenue'].sum()
    st.write(unit_wise_all)

st.divider()
st.subheader(f"{df_app_selected['Package Name'].unique()} country wise rev & imps")
df_all_cntry = df_app_selected.groupby('Country')[['Est. Revenue','Impressions']].sum()
st.write(df_all_cntry)


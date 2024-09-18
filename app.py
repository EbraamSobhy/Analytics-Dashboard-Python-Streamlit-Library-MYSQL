import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query import view_all_data
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")
st.header("🔔 Insurance Descriptive Analytics")
st.markdown("##")

# Fetch Data
result = view_all_data()
df = pd.DataFrame(result, columns=["Policy", "Expiry", "Location", "State", "Region", "Investment", "Construction", "BusinessType", "Earthquake", "Flood", "Rating"])


# Side Bar
st.sidebar.image("data/logo.png", caption="Online Analytics")

# Switcher
st.sidebar.header("Please Filter")
region=st.sidebar.multiselect(
    "SELECT REGION",
    options=df["Region"].unique(),
    default=df["Region"].unique(),
)
location=st.sidebar.multiselect(
    "SELECT LOCATION",
    options=df["Location"].unique(),
    default=df["Location"].unique(),
)
construction=st.sidebar.multiselect(
    "SELECT CONSTRUCTION",
    options=df["Construction"].unique(),
    default=df["Construction"].unique(),
)

df_selection = df.query(
    "Region==@region & Location==@location & Construction ==@construction"
)

def Home():
    with st.expander("Tabular"):
        showData = st.multiselect('Filter:', df_selection.columns,default=[])
        st.write(df_selection[showData])

    # Compute top analytics
    if not df_selection.empty:
        total_investment = df_selection["Investment"].sum()
        investment_mode = df_selection["Investment"].mode().iloc[0] if not df_selection["Investment"].mode().empty else 0
        investment_mean = df_selection["Investment"].mean()
        investment_median = df_selection["Investment"].median()
        rating = df_selection["Rating"].sum()

        total1, total2, total3, total4, total5 = st.columns(5, gap='small')
        with total1:
            st.info('Sum Investment', icon="💰")
            st.metric(label="Sum TZS", value=f"{total_investment:,.0f}")

        with total2:
            st.info('Most Investment', icon="💰")
            st.metric(label="Mode TZS", value=f"{investment_mode:,.0f}")

        with total3:
            st.info('Total Average', icon="💰")
            st.metric(label="Average TZS", value=f"{investment_mean:,.0f}")

        with total4:
            st.info('Central Earnings', icon="💰")
            st.metric(label="Median TZS", value=f"{investment_median:,.0f}")

        with total5:
            st.info('Total Ratings', icon="💰")
            st.metric(label="Rating", value=numerize(rating), help=f"Total Rating: {rating}")

        st.markdown("""---""")
    else:
        st.warning("No data available for the selected filters.")

# Graphs
def graphs():
    total_investment = df_selection["Investment"].sum()
    averageRating = round(df_selection["Rating"].mean(), 2)

    # Simple Bar Graph
    investment_by_business_type = (
        df_selection.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")
    )
    fig_investment = px.bar(
        investment_by_business_type,
        x="Investment",
        y=investment_by_business_type.index,
        orientation="h",
        title="<b> Investment by Business Type </b>",
        color_discrete_sequence=["#0083b8"] * len(investment_by_business_type),
        template="plotly_white",
    )
    
    fig_investment.update_layout(
        plot_bgcolor="rgb(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )
    
    # Simple Line Graph
    investment_state = df_selection.groupby(by=["State"]).count()[["Investment"]]
    
    fig_state = px.line(
        investment_state,
        x=investment_state.index,
        y="Investment",
        title="<b> Investment by State </b>",
        color_discrete_sequence=["#0083b8"] * len(investment_state),
        template="plotly_white",
    )
    fig_state.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgb(0,0,0,0)",
        yaxis=dict(showgrid=False)
    )

    left, right = st.columns(2)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)


#function to show current earnings against expected target
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
    target = 3000000000
    current = df_selection["Investment"].sum()
    percent = round((current/target*100))
    mybar = st.progress(0)

    if percent > 100:
        st.subheader("Target done !")
    else:
        st.write("you have ",percent, "% " ,"of ", (format(target, 'd')), "TZS")
        for percent_complete in range(percent):
            time.sleep(0.1)
            mybar.progress(percent_complete + 1,text=" Target Percentage")

#menu bar
def sideBar():

    with st.sidebar:
        selected=option_menu(
        menu_title="Main Menu",
        options=["Home","Progress"],
        icons=["house","eye"],
        menu_icon="cast",
        default_index=0
    )

    if selected == "Home":
        st.subheader(f"Page: {selected}")
        Home()
        graphs()
    elif selected == "Progress":
        st.subheader(f"Page: {selected}")
        Progressbar()
        graphs()

sideBar()

if 'BusinessType' in df.columns:
    st.subheader('PICK FEATURES TO EXPLORE DISTRIBUTIONS TRENDS BY QUARTILES')

    # Select feature for quantitative data
    feature_y = st.selectbox('Select feature for y Quantitative Data', df_selection.select_dtypes("number").columns)

    # Create the Plotly figure
    fig2 = go.Figure(
        data=[go.Box(x=df['BusinessType'], y=df[feature_y])],
        layout=go.Layout(
            title=go.layout.Title(text="BUSINESS TYPE BY QUARTILES OF INVESTMENT"),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
            yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
            font=dict(color='#cecdcd'),
        )
    )

    # Display the Plotly figure using Streamlit
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("The 'BusinessType' column is missing from the DataFrame.")


#theme
hide_st_style="""

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

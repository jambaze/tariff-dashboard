import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Tariff Tracker Dashboard", layout="wide")

# Load data from Google Sheets CSV
@st.cache_data
def load_data():
    sheet_url = st.secrets["sheet_url"]
    return pd.read_csv(sheet_url)

df = load_data()

# Sidebar controls
st.sidebar.title("Tariff Dashboard")
view_option = st.sidebar.selectbox("View", ["US Tariffs", "Retaliatory Tariffs"])
country_selected = st.sidebar.selectbox("Country Insight", df["Country"].unique())

# Dashboard title
st.title("🌐 Global Tariff Tracker Dashboard")
st.markdown("Live visualization of **US-imposed tariffs** and **retaliatory tariffs** from affected countries.")

# Map visualization
if view_option == "US Tariffs":
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="US Tariff (%)",
        hover_name="Country",
        color_continuous_scale="Reds",
        title="US Tariffs by Country"
    )
else:
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Retaliatory Tariff (%)",
        hover_name="Country",
        color_continuous_scale="Blues",
        title="Retaliatory Tariffs on US"
    )

st.plotly_chart(fig, use_container_width=True)

# Country insights
st.subheader(f"📍 Detailed View: {country_selected}")
country_data = df[df["Country"] == country_selected].iloc[0]
st.markdown(f"""
**🧾 Affected Products**: {country_data['Affected Products']}  
**💰 Trade Volume**: ${country_data['Trade Volume ($B)']}B  
**🇺🇸 US Tariff**: {country_data['US Tariff (%)']}%  
**🔁 Retaliatory Tariff**: {country_data['Retaliatory Tariff (%)']}%
""")

# Top 5 US Tariffs chart
st.subheader("📊 Top 5 Countries by US Tariff")
top_df = df.sort_values(by="US Tariff (%)", ascending=False).head(5)
bar_fig = px.bar(
    top_df,
    x="Country",
    y="US Tariff (%)",
    title="Top 5 Countries with Highest US Tariffs",
    color="US Tariff (%)",
    color_continuous_scale="Reds"
)
st.plotly_chart(bar_fig, use_container_width=True)

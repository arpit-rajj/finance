import streamlit as st
from api_client import api
from components.charts import render_portfolio_allocation

st.title("💼 Portfolio")

token = st.session_state.get('token')

if not token:
    st.warning("Please log in.")
    st.stop()

st.markdown("Overview of all linked accounts, assets, and investments.")

with st.spinner("Fetching portfolio data..."):
    # This calls our placeholder endpoint function
    portfolio_data = api.get_portfolio_summary(token)

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Total Asset Value", f"${portfolio_data.get('total_value', 0):,.2f}")
    st.markdown("*(Note: Portfolio endpoint is currently mocked as per backend state.)*")

with col2:
    render_portfolio_allocation()

import streamlit as st
import datetime
from api_client import api
from components.charts import render_transaction_history_chart, render_category_pie_chart
from components.tables import render_recent_transactions_preview

st.title("📊 Dashboard")

token = st.session_state.get('token')

if not token:
    st.warning("Please log in.")
    st.stop()

# Fetch data
with st.spinner("Loading dashboard data..."):
    try:
        # Get overall stats
        stats = api.get_transaction_stats(token)
        
        # Get custom stats for current month
        now = datetime.datetime.now()
        monthly_stats = api.get_monthly_stats(token, month=now.month, year=now.year)
        
        # Get recent transactions for preview and charts
        transactions = api.get_transactions(token, limit=50) # fetch up to 50 for good charts
        recent = transactions[:5] # preview list only needs 5
        
    except Exception as e:
        st.error(f"Failed to load dashboard data: {str(e)}")
        st.stop()

# --- Key Metrics ---
st.markdown("### Financial Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Balance", 
        value=f"${stats.get('net_balance', 0):,.2f}",
        delta=f"This Month: ${monthly_stats.get('net_balance', 0):,.2f}"
    )
with col2:
    st.metric(
        label="Total Income", 
        value=f"${stats.get('total_income', 0):,.2f}",
        delta=f"This Month: ${monthly_stats.get('total_income', 0):,.2f}"
    )
with col3:
    st.metric(
        label="Total Expenses", 
        value=f"${stats.get('total_expenditure', 0):,.2f}",
        delta=f"This Month: ${monthly_stats.get('total_expenditure', 0):,.2f}",
        delta_color="inverse"
    )

st.divider()

# --- Charts and Tables Layout ---
col_charts, col_preview = st.columns([2, 1])

with col_charts:
    st.markdown("### Cash Flow Trend")
    render_transaction_history_chart(transactions)
    
    st.markdown("### Spending by Category")
    render_category_pie_chart(transactions)

with col_preview:
    st.markdown("### Recent Activity")
    render_recent_transactions_preview(recent)
    
    # A link shortcut disguised as a button
    if st.button("View All Transactions", use_container_width=True):
        st.switch_page("pages/transactions.py")

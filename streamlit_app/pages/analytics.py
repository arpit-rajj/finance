import streamlit as st
import pandas as pd
from api_client import api

st.title("🤖 AI Analytics")

token = st.session_state.get('token')

if not token:
    st.warning("Please log in.")
    st.stop()

st.markdown("Discover insights powered by our AI categorization engine.")

with st.spinner("Gathering AI insights..."):
    # Mocking this for now as per api_client setup
    ai_predictions = api.get_ai_predictions(token)
    transactions = api.get_transactions(token, limit=100)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Insights")
    
    # We can perform some local analytics on the fetched data
    df = pd.DataFrame(transactions)
    if df.empty:
        st.info("No data available to analyze.")
    else:
        # Check for AI categorized stuff based on our models
        if 'is_ai_categorized' in df.columns:
            ai_categorized = df[df['is_ai_categorized'] == True]
            if not ai_categorized.empty:
                st.success(f"{len(ai_categorized)} transactions automatically categorized by AI!")
                st.dataframe(
                    ai_categorized[['description', 'amount', 'category_id', 'ai_confidence']],
                    use_container_width=True
                )
            else:
                st.info("No AI categorized transactions yet.")
        
        # Check for items that need review
        if 'needs_review' in df.columns:
            needs_review = df[df['needs_review'] == True]
            if not needs_review.empty:
                st.warning(f"⚠️ {len(needs_review)} transactions have low AI confidence and need manual review.")
                st.dataframe(
                    needs_review[['description', 'amount', 'ai_confidence']],
                    use_container_width=True
                )

with col2:
    st.markdown("### Smart Predictions")
    for insight in ai_predictions.get("insights", []):
        st.info(f"💡 {insight}")

    # E.g., calculate largest expense this month over all transactions fetched
    if not df.empty and 'amount' in df.columns:
        expenses = df[df['amount'] < 0]
        if not expenses.empty:
            biggest_expense = expenses.loc[expenses['amount'].idxmin()]
            st.markdown(f"**Largest Expense Detection:**\nYou spent `{abs(biggest_expense['amount'])}` on `{biggest_expense['description']}`.")


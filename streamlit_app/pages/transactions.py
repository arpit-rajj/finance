import streamlit as st
import datetime
from api_client import api
from components.tables import render_transaction_table

st.title("📝 Transactions")

token = st.session_state.get('token')

if not token:
    st.warning("Please log in.")
    st.stop()

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Transaction History")
    
    # Filters
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        search_query = st.text_input("Search Description")
    with f_col2:
        sort_by = st.selectbox("Sort direction", options=["desc", "asc"])
    with f_col3:
        limit = st.number_input("Limit", min_value=10, max_value=500, value=50, step=10)

    with st.spinner("Fetching transactions..."):
        try:
            transactions = api.get_transactions(
                token=token, 
                limit=limit, 
                search=search_query if search_query else None,
                sort_by=sort_by
            )
            render_transaction_table(transactions)
        except Exception as e:
            st.error(f"Error loading transactions: {str(e)}")


with col2:
    st.markdown("### Add Transaction")
    
    with st.form("add_transaction_form"):
        # We need a description and amount
        amount = st.number_input("Amount", step=1.0)
        desc = st.text_input("Description (E.g. Walmart grocieries)")
        # Categories might come from an endpoint, but for now we let it be optional/None
        cat_id_raw = st.number_input("Category ID (0 for AI guess)", value=0, step=1)
        
        submit = st.form_submit_button("Create", type="primary")
        
        if submit:
            if not desc:
                st.error("Description is required.")
            elif amount == 0:
                st.error("Amount cannot be 0.")
            else:
                try:
                    cat_id = None if cat_id_raw == 0 else int(cat_id_raw)
                    new_txn = api.create_transaction(token, amount, desc, cat_id)
                    st.success(f"Added: {new_txn.get('description')}")
                    st.rerun() # Refresh the page to see the new transaction
                except Exception as e:
                    st.error(f"Failed to add transaction: {str(e)}")


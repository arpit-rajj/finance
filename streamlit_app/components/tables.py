import streamlit as st
import pandas as pd
from typing import List, Dict, Any

def render_transaction_table(transactions: List[Dict[str, Any]]):
    """Render a clean, formatted dataframe for transactions."""
    if not transactions:
        st.info("No transactions to display.")
        return

    df = pd.DataFrame(transactions)
    
    # Format dates
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M')
    
    # Select columns to display
    display_cols = ['date', 'description', 'amount']
    rename_cols = {'date': 'Date', 'description': 'Description', 'amount': 'Amount'}
    
    if 'category_id' in df.columns:
        display_cols.append('category_id')
        rename_cols['category_id'] = 'Category ID'
        
    if 'is_ai_categorized' in df.columns:
        display_cols.append('is_ai_categorized')
        rename_cols['is_ai_categorized'] = 'AI Categorized'
        
    if 'needs_review' in df.columns:
        display_cols.append('needs_review')
        rename_cols['needs_review'] = 'Needs Review'
        
    df_display = df[display_cols].rename(columns=rename_cols)
    
    # Style the dataframe
    def style_amount(val):
        try:
            amount = float(val)
            color = 'green' if amount > 0 else 'red'
            return f'color: {color}'
        except:
            return ''

    def style_review(val):
        if val is True:
            return 'background-color: rgba(255, 165, 0, 0.2);' # Orange tint
        return ''

    styled_df = df_display.style.map(style_amount, subset=['Amount'])
    
    if 'Needs Review' in df_display.columns:
        styled_df = styled_df.map(style_review, subset=['Needs Review'])
        
    # Format the amount column to look like currency
    styled_df = styled_df.format({'Amount': '${:,.2f}'})

    # Use container width for better layout
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

def render_recent_transactions_preview(transactions: List[Dict[str, Any]], limit: int = 5):
    """A smaller, minimal table for the dashboard overview."""
    if not transactions:
        st.write("No recent activity.")
        return
        
    preview = transactions[:limit]
    df = pd.DataFrame(preview)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%b %d')
    df_display = df[['date', 'description', 'amount']].rename(
        columns={'date': 'Date', 'description': 'Description', 'amount': 'Amount'}
    )
    
    st.dataframe(
        df_display.style.format({'Amount': '${:,.2f}'}), 
        use_container_width=True, 
        hide_index=True
    )

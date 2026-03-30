import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any

def render_transaction_history_chart(transactions: List[Dict[str, Any]]):
    """Render a bar or line chart showing transactions over time by day."""
    if not transactions:
        st.info("No transaction data available for chart.")
        return

    df = pd.DataFrame(transactions)
    # Convert string dates to datetime
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    # Group by date and calculate daily sums
    # Positive amount -> Income, Negative amount -> Expense
    df['type'] = df['amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')
    df['abs_amount'] = df['amount'].abs()
    
    daily_summary = df.groupby(['date', 'type'])['abs_amount'].sum().reset_index()

    fig = px.bar(
        daily_summary, 
        x='date', 
        y='abs_amount', 
        color='type',
        title="Income & Expenses Over Time",
        labels={'date': 'Date', 'abs_amount': 'Amount', 'type': 'Transaction Type'},
        color_discrete_map={'Income': '#00CC96', 'Expense': '#EF553B'},
        barmode='group'
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        margin=dict(t=50, l=10, r=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)


def render_category_pie_chart(transactions: List[Dict[str, Any]]):
    """Render a pie chart showing expenses by category (if categories exist)."""
    # Assuming the API returns a 'category' nested object or 'category_id'
    # Fallback to 'description' or 'is_ai_categorized' for demo purposes
    if not transactions:
        return
        
    df = pd.DataFrame(transactions)
    # Filter expenses only
    expenses = df[df['amount'] < 0].copy()
    if expenses.empty:
        st.info("No expense data available for categorization chart.")
        return
        
    expenses['abs_amount'] = expenses['amount'].abs()
    
    # Try to extract category name, or use an AI flag, or description fallback
    def get_category_name(row):
        if pd.notna(row.get('category_id')):
            return f"Category {int(row['category_id'])}"
        elif row.get('is_ai_categorized'):
            return "AI Categorized"
        else:
            return "Uncategorized"

    expenses['Category'] = expenses.apply(get_category_name, axis=1)
    
    summary = expenses.groupby('Category')['abs_amount'].sum().reset_index()
    
    fig = px.pie(
        summary, 
        values='abs_amount', 
        names='Category', 
        title="Expenses Breakdown",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Teal
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, l=10, r=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_portfolio_allocation():
    """Placeholder chart for the portfolio page."""
    # Data is simulated since there is no portfolio endpoint
    data = {"Asset": ["Stocks", "Bonds", "Crypto", "Cash"], "Value": [45000, 15000, 8000, 12000]}
    df = pd.DataFrame(data)
    fig = px.pie(
        df, values="Value", names="Asset", title="Asset Allocation", hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig.update_layout(
        margin=dict(t=50, l=10, r=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)

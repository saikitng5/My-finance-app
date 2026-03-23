import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. SETTINGS & THEME
st.set_page_config(page_title="Personal Finance Pro", layout="wide")

# 2. PASSWORD PROTECTION
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    
    if not st.session_state["password_correct"]:
        st.title("🔒 Private Finance Dashboard")
        pwd = st.text_input("Enter Access Key:", type="password")
        if st.button("Login"):
            if pwd == "1234": # CHANGE THIS TO YOUR DESIRED PASSWORD
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Invalid Password")
        return False
    return True

if check_password():
    # 3. SIDEBAR INPUTS (Income & Spending)
    st.sidebar.header("📊 Data Entry")
    
    with st.sidebar.expander("Income & Expenses"):
        inc = st.number_input("Monthly Income ($)", value=50000, step=1000)
        exp = st.number_input("Monthly Spending ($)", value=30000, step=1000)
        frequency = st.selectbox("Frequency", ["Monthly", "Annually"])
        years = st.slider("Projection Years", 1, 30, 10)

    with st.sidebar.expander("Balance Sheet"):
        assets = st.number_input("Total Assets ($)", value=1000000, step=10000)
        liabs = st.number_input("Total Liabilities ($)", value=200000, step=10000)

    # 4. CALCULATIONS
    net_worth = assets - liabs
    monthly_savings = inc - exp
    savings_rate = (monthly_savings / inc) * 100 if inc > 0 else 0
    liquidity_ratio = assets / exp if exp > 0 else 0
    debt_ratio = (liabs / assets) * 100 if assets > 0 else 0

    # 5. DASHBOARD LAYOUT
    st.title("🏦 Financial Command Center")
    st.markdown("---")

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Net Worth", f"${net_worth:,.0f}")
    col2.metric("Monthly Savings", f"${monthly_savings:,.0f}")
    col3.metric("Savings Rate", f"{savings_rate:.1f}%")
    col4.metric("Debt Ratio", f"{debt_ratio:.1f}%")

    # 6. COMMENTARY & RATIOS
    st.subheader("📋 Financial Health Check")
    c1, c2 = st.columns(2)
    
    with c1:
        st.write(f"**Liquidity Ratio:** {liquidity_ratio:.1f}")
        if liquidity_ratio > 6:
            st.success("Strong: You have over 6 months of runway.")
        else:
            st.warning("Caution: Aim for at least 6 months of expenses in liquid assets.")
            
    with c2:
        st.write(f"**Solvency Note:**")
        if debt_ratio < 40:
            st.info("Your debt levels are healthy relative to your assets.")
        else:
            st.error("High Debt: Focus on deleveraging to protect your net worth.")

    # 7. VISUALIZATIONS
    st.markdown("---")
    st.subheader("📈 Performance & Projections")
    
    # Projection Logic
    months = np.arange(years * 12)
    future_wealth = [net_worth + (monthly_savings * m) for m in months]
    proj_df = pd.DataFrame({"Month": months, "Projected Net Worth": future_wealth})

    fig = px.area(proj_df, x="Month", y="Projected Net Worth", 
                  title="Wealth Accumulation Forecast",
                  template="plotly_dark") # Coding-style dark interface
    st.plotly_chart(fig, use_container_width=True)

    # Asset vs Liability Chart
    bal_data = pd.DataFrame({
        "Category": ["Assets", "Liabilities"],
        "Amount": [assets, liabs]
    })
    fig2 = px.bar(bal_data, x="Category", y="Amount", color="Category", 
                  template="plotly_dark", barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

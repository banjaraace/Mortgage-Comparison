import streamlit as st

st.title("Mortgage App Debug: Hello World!")

# Scenario container
if "scenarios" not in st.session_state:
    st.session_state.scenarios = []

st.header("Add a Scenario")

with st.form("add_scenario"):
    name = st.text_input("Scenario Name")

    property_price = st.number_input("Property Price ($)", min_value=0.0, value=400000.0)
    down_payment_percent = st.number_input("Down Payment (%)", min_value=0.0, value=20.0)
    
    # Calculate values for display only
    down_payment_amount = property_price * (down_payment_percent / 100)
    loan_amount = property_price - down_payment_amount

    st.write(f"**Calculated Down Payment:** ${down_payment_amount:,.2f}")
    st.write(f"**Calculated Loan Amount:** ${loan_amount:,.2f}")

    annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.0)
    years = st.number_input("Loan Term (Years)", min_value=1, value=30)

    extra_payment = st.number_input("Extra Monthly Payment ($)", min_value=0.0, value=0.0)
    extra_payment_months = st.number_input("Number of Months to Apply Extra Payment", min_value=0, value=0)

    submit = st.form_submit_button("Add Scenario")

if submit and name:
    st.success(f"Scenario '{name}' submitted! (Calculations are temporarily disabled)")


# All calculation and display code is removed for this test.

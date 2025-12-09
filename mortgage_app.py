import streamlit as st
import pandas as pd
# from io import BytesIO
# import openpyxl
# from openpyxl.utils import get_column_letter

st.title("Mortgage Scenario Comparison Tool")

# Scenario container
if "scenarios" not in st.session_state:
    st.session_state.scenarios = []

st.header("Add a Scenario")

with st.form("add_scenario"):
    name = st.text_input("Scenario Name")

    property_price = st.number_input("Property Price ($)", min_value=0.0, value=400000.0)
    down_payment_percent = st.number_input("Down Payment (%)", min_value=0.0, value=20.0)
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
    st.session_state.scenarios.append({
        "name": name,
        "property_price": property_price,
        "down_payment_percent": down_payment_percent,
        "down_payment_amount": down_payment_amount,
        "loan_amount": loan_amount,
        "annual_rate": annual_rate,
        "years": years,
        "extra_payment": extra_payment,
        "extra_payment_months": extra_payment_months
    })
    st.success(f"Scenario '{name}' added!")

# ---------------------- Mortgage Calculation ----------------------------

def calculate_schedule(loan_amount, annual_rate, years, extra_payment, extra_payment_months):
    monthly_rate = annual_rate / 100 / 12
    total_months = int(years * 12)

    if monthly_rate > 0:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** total_months) / ((1 + monthly_rate) ** total_months - 1)
    else:
        monthly_payment = loan_amount / total_months

    balance = loan_amount
    amortization = []

    for month in range(1, total_months + 1):

        if month <= extra_payment_months:
            applied_extra = extra_payment
        else:
            applied_extra = 0.0

        interest = balance * monthly_rate
        principal = monthly_payment - interest
        principal += applied_extra

        if principal > balance:
            principal = balance
            monthly_payment_adjusted = interest + principal
        else:
            monthly_payment_adjusted = monthly_payment + applied_extra

        balance -= principal

        amortization.append({
            "Month": month,
            "Interest": round(interest, 2),
            "Principal": round(principal - applied_extra, 2),
            "Extra Payment": round(applied_extra, 2),
            "Total Payment": round(monthly_payment_adjusted, 2),
            "Remaining Balance": round(balance, 2)
        })

        if balance <= 0:
            break

    df = pd.DataFrame(amortization)

    totals = {
        "total_interest": df["Interest"].sum(),
        "total_principal": df["Principal"].sum(),
        "total_extra": df["Extra Payment"].sum(),
        "total_paid": df["Total Payment"].sum(),
        "months": len(df)
    }

    return df, totals, monthly_payment


# ---------------------- Excel Export with Formulas ----------------------------

# def create_excel(scenario, df, totals, monthly_payment):
#     output = BytesIO()
#     wb = openpyxl.Workbook()
#     ws = wb.active
#     ws.title = "Mortgage Scenario"

#     # Scenario Details
#     details = {
#         "Scenario Name": scenario["name

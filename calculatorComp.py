# file name: calculatorComp.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Mortgage Repayments Calculator")

st.write("### Input Data")
col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value", min_value=0, value=500000)
deposit = col1.number_input("Deposit", min_value=0, value=100000)
interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value=5.5)
loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)

# Calculate the repayments.
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display the repayments.
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repayment Details")

col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Payments", value=f"${total_payments:,.0f}")
col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")

# Crear un dataframe con el calendario de pagos.
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)  # Calcular el año dentro del préstamo
    schedule.append(
        {
            "Month": i,
            "Year": year,
            "Monthly Payment": monthly_payment,
            "Interest Payment": interest_payment,
            "Principal Payment": principal_payment,
            "Remaining Balance": remaining_balance,
        }
    )

# Crear DataFrame con el calendario de pagos
df = pd.DataFrame(schedule, columns=["Month", "Year", "Monthly Payment", "Interest Payment", "Principal Payment", "Remaining Balance"])

# Display the DataFrame as a chart
st.write("#### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)

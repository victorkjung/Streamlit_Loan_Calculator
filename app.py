import streamlit as st
import numpy as np
import pandas as pd
import base64

# Function to calculate amortization schedule
def amortization_schedule(loan_amount, interest_rate, years):
    # Monthly interest rate
    monthly_interest_rate = interest_rate / (100 * 12)
    # Number of payments
    payment_num = years * 12
    # Calculate monthly payment
    monthly_payment = loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** (-payment_num))

    # Initialize amortization schedule
    schedule = pd.DataFrame(columns=['Month', 'Payment', 'Principal', 'Interest', 'Ending Balance'])
    balance = loan_amount

    for i in range(int(payment_num)):
        interest = balance * monthly_interest_rate
        principal = monthly_payment - interest
        balance = balance - principal

        schedule = schedule.append({
            "Month": i + 1,
            "Payment": monthly_payment,
            "Principal": principal,
            "Interest": interest,
            "Ending Balance": balance,
        }, ignore_index=True)

    return monthly_payment, schedule

# Streamlit code
st.title(f"Loan \U0001F4C8 Calculator")
st.title(f"\U0001F64B What is our monthly payment?")

# Data inputs for the loan calculator
loan_amount = st.text_input('Loan Amount', value='50,000')
# Remove thousands separator and convert to float
loan_amount = float(loan_amount.replace(',', ''))
interest_rate = st.number_input('Annual Interest Rate', value=5.0)
years = st.number_input('Loan Period in Years', value=5, format='%d')
calculate = st.button('Calculate Now')

if calculate:
    monthly_payment, schedule = amortization_schedule(loan_amount, interest_rate, years)

    # Display the monthly payment
    st.markdown(f'Your Monthly Loan Payment is: **{monthly_payment:,.2f}**')

    # Format the schedule for display
    schedule["Payment"] = schedule["Payment"].apply(lambda x: '{:,.2f}'.format(x))
    schedule["Principal"] = schedule["Principal"].apply(lambda x: '{:,.2f}'.format(x))
    schedule["Interest"] = schedule["Interest"].apply(lambda x: '{:,.2f}'.format(x))
    schedule["Ending Balance"] = schedule["Ending Balance"].apply(lambda x: '{:,.2f}'.format(x))

    # Display the amortization schedule
    st.dataframe(schedule)

    # Convert DataFrame to CSV and make it downloadable
    csv = schedule.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings
    href = f'<a href="data:file/csv;base64,{b64}" download="schedule.csv">Click Here to download as CSV file</a> (click link and save as &lt;some_name&gt;.csv)'
    st.markdown(href, unsafe_allow_html=True)
    



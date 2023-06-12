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

        # Add a new row to the schedule DataFrame with the following values:
        # Month: i + 1
        # Payment: monthly_payment
        # Principal: principal
        # Interest: interest
        # Ending Balance: balance
        schedule.loc[len(schedule)] = {
            "Month": i + 1,
            "Payment": monthly_payment,
            "Principal": principal,
            "Interest": interest,
            "Ending Balance": balance,
        }

    return monthly_payment, schedule

# Streamlit code
st.sidebar.title("Loan Calculator")

# Add a description to the sidebar
st.sidebar.write("Welcome to the Loan Calculator. This tool helps you calculate the monthly payment for a loan and provides an amortization schedule.")

# Add instructions to the sidebar
st.sidebar.subheader("Instructions:")
st.sidebar.write("1. Enter the loan amount, annual interest rate, and loan period in years.")
st.sidebar.write("2. Click on the '**Calculate Now**' button.")
st.sidebar.write("3. The monthly payment and amortization schedule will be displayed.")
st.sidebar.write("4. You can download the amortization schedule as a **CSV file**.")

# About developer section
st.sidebar.subheader("About the developer")
st.sidebar.write("Victor Jung is a serial entrepreneur and technology hobbyist. He is passionate about building innovative solutions and leveraging technology to solve real-world problems. With a diverse background in business and technology, Victor has successfully launched and managed multiple ventures.")

st.sidebar.write("This loan calculator was developed using PyCharm, a powerful integrated development environment (IDE), and GitHub Co-Pilot, an AI-powered coding assistant. The collaboration between Victor and GitHub Co-Pilot streamlined the programming process, ensuring efficient code generation and error correction.")

# Guidance for loan calculator
st.sidebar.subheader("Guidance on Loan Payments")
st.sidebar.write("The loan calculator provided can give you an estimate of your potential monthly payment for a loan. However, it's important to note that actual loan payments can vary based on various factors, such as the lender's calculation methods, compounding interest, and other specific loan terms.")

st.sidebar.write("To get the most accurate payment estimate, it's recommended to consult with your lender or financial advisor. They can provide personalized guidance based on your unique financial situation and the specific terms of your loan.")

st.sidebar.write("Please use this loan calculator as a reference and starting point for understanding the potential monthly payment of your loan.")

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
    st.markdown(f'<h4>Your Monthly Loan Payment is: ${monthly_payment:,.2f}</h4>', unsafe_allow_html=True)
 
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

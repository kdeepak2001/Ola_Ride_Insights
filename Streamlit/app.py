import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ola Ride Insights", layout="wide")

# Load CSV Data
@st.cache_data
def load_data():
    return pd.read_csv("../Data/OLA_cleaned.csv")

df = load_data()

# Sidebar Navigation
page = st.sidebar.selectbox(
    "Select Page",
    ["Insights Dashboard", "Project Outcome & Explanation"]
)

# ===============================
# PAGE 1: INSIGHTS DASHBOARD
# ===============================
if page == "Insights Dashboard":

    st.title("🚗 Ola Ride Insights Dashboard")

    total_rides = len(df)
    successful_rides = len(df[df["Booking_Status"] == "Success"])
    revenue = df[df["Booking_Status"] == "Success"]["Booking_Value"].sum()
    driver_cancel = df["Canceled_Rides_by_Driver"].notna().sum()
    customer_cancel = df["Canceled_Rides_by_Customer"].notna().sum()
    success_rate = round((successful_rides / total_rides) * 100, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rides", total_rides)
    col2.metric("Successful Rides", successful_rides)
    col3.metric("Success Rate %", f"{success_rate}%")

    col4, col5 = st.columns(2)
    col4.metric("Driver Cancellations", driver_cancel)
    col5.metric("Customer Cancellations", customer_cancel)

    st.divider()

    st.subheader("Revenue Trend Over Time")
    revenue_trend = (
        df[df["Booking_Status"] == "Success"]
        .groupby("Date")["Booking_Value"]
        .sum()
    )
    st.line_chart(revenue_trend)

    st.subheader("Ride Volume by Vehicle Type")
    vehicle_data = df["Vehicle_Type"].value_counts()
    st.bar_chart(vehicle_data)

    st.subheader("Revenue by Payment Method")
    payment_data = (
        df[df["Booking_Status"] == "Success"]
        .groupby("Payment_Method")["Booking_Value"]
        .sum()
    )
    st.bar_chart(payment_data)

# ===============================
# PAGE 2: PROJECT OUTCOME
# ===============================
if page == "Project Outcome & Explanation":

    st.title("📘 Project Explanation & Business Outcome")

    st.subheader("Domain Introduction")
    st.write("Ride-sharing & Mobility Analytics focuses on analyzing transportation data to improve operational efficiency and customer satisfaction.")

    st.subheader("Project Introduction")
    st.write("This project analyzes Ola ride data using SQL, Power BI, and Streamlit to derive actionable business insights.")

    st.subheader("Objective")
    st.write("The objective is to understand ride trends, cancellations, revenue, and ratings to improve service quality and profitability.")

    st.subheader("EDA Findings")
    st.write("""
    - 62% ride success rate.
    - Driver cancellations significantly higher than customer cancellations.
    - Revenue heavily dependent on successful bookings.
    """)

    st.subheader("Business Suggestions")
    st.write("""
    - Reduce driver cancellations through incentive mechanisms.
    - Promote digital payments for operational efficiency.
    - Introduce loyalty programs to increase repeat bookings.
    """)
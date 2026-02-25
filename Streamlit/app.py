import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ola Ride Insights", layout="wide")

# Load CSV Data
@st.cache_data
def load_data():
   return pd.read_csv("Data/OLA_cleaned.csv")

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

    st.title(" Ola Ride Insights Dashboard")

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

    st.title(" Executive Project Outcome Report")

    st.markdown("## Domain Overview")
    st.write("""
    The ride-sharing and mobility analytics domain focuses on optimizing transportation services 
    through data-driven decision-making. Companies like Ola rely on operational data to enhance 
    efficiency, reduce cancellations, and maximize revenue while maintaining customer satisfaction.
    """)

    st.markdown("## Project Objective")
    st.write("""
    The primary objective of this project was to analyze Ola ride data to uncover operational inefficiencies, 
    revenue patterns, cancellation trends, and service quality indicators. The goal is to provide actionable 
    business recommendations backed by analytical insights.
    """)

    st.markdown("## Key Analytical Findings")

    st.markdown("""
    - **Ride Success Rate:** 62% of total bookings were successfully completed.
    - **Operational Risk Area:** Driver cancellations (18K+) are significantly higher than customer cancellations (10K+).
    - **Revenue Insight:** ₹35M+ revenue generated from successful rides.
    - **Digital Adoption:** UPI and digital payment methods contribute major revenue share.
    - **Service Quality:** Average ratings remain stable (~4.0), indicating consistent customer satisfaction.
    """)

    st.markdown("## Business Impact")

    st.markdown("""
    - Reducing driver cancellations by even 10% can significantly increase revenue.
    - Promoting digital payments can streamline operations and reduce cash handling risk.
    - Loyalty programs can improve repeat ride frequency and retention.
    """)

    st.markdown("## Strategic Recommendations")

    st.markdown("""
    1. Implement performance-based incentives for drivers to reduce cancellations.
    2. Launch targeted UPI cashback campaigns to boost digital transactions.
    3. Introduce driver accountability metrics to improve reliability.
    4. Monitor cancellation patterns using real-time dashboards for faster intervention.
    """)

    st.markdown("---")
    st.markdown("### Final Conclusion")
    st.write("""
    This project demonstrates how structured SQL analysis, Power BI visualization, 
    and Streamlit deployment can transform raw ride data into meaningful strategic insights. 
    The solution provides a scalable framework for operational monitoring and revenue optimization 
    within the ride-sharing ecosystem.
    """)
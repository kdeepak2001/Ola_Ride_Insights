import streamlit as st
import mysql.connector
import pandas as pd
import os

st.set_page_config(page_title="Ola Ride Insights", layout="wide")

# -------------------------------
# DATABASE CONNECTION (SECURE)
# -------------------------------
def get_data(query):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="ola_project"
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df


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

    # KPIs
    total_rides = get_data("SELECT COUNT(*) as total FROM ola_rides")
    successful_rides = get_data("SELECT COUNT(*) as success FROM ola_rides WHERE Booking_Status='Success'")
    revenue = get_data("SELECT SUM(Booking_Value) as revenue FROM ola_rides WHERE Booking_Status='Success'")
    driver_cancel = get_data("SELECT COUNT(*) as d FROM ola_rides WHERE Canceled_Rides_by_Driver IS NOT NULL")
    customer_cancel = get_data("SELECT COUNT(*) as c FROM ola_rides WHERE Canceled_Rides_by_Customer IS NOT NULL")

    success_rate = round((successful_rides['success'][0] / total_rides['total'][0]) * 100, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rides", int(total_rides['total'][0]))
    col2.metric("Successful Rides", int(successful_rides['success'][0]))
    col3.metric("Success Rate %", f"{success_rate}%")

    col4, col5 = st.columns(2)
    col4.metric("Driver Cancellations", int(driver_cancel['d'][0]))
    col5.metric("Customer Cancellations", int(customer_cancel['c'][0]))

    st.divider()

    # Revenue Trend
    st.subheader("Revenue Trend Over Time")
    revenue_trend = get_data("""
        SELECT Date, SUM(Booking_Value) as revenue
        FROM ola_rides
        WHERE Booking_Status='Success'
        GROUP BY Date
        ORDER BY Date
    """)
    st.line_chart(revenue_trend.set_index("Date"))

    # Vehicle Distribution
    st.subheader("Ride Volume by Vehicle Type")
    vehicle_data = get_data("""
        SELECT Vehicle_Type, COUNT(*) as count
        FROM ola_rides
        GROUP BY Vehicle_Type
    """)
    st.bar_chart(vehicle_data.set_index("Vehicle_Type"))

    # Payment Revenue
    st.subheader("Revenue by Payment Method")
    payment_data = get_data("""
        SELECT Payment_Method, SUM(Booking_Value) as revenue
        FROM ola_rides
        WHERE Booking_Status='Success'
        GROUP BY Payment_Method
    """)
    st.bar_chart(payment_data.set_index("Payment_Method"))# ===============================
# PAGE 2: PROJECT OUTCOME
# ===============================
if page == "Project Outcome & Explanation":

    st.title(" Project Explanation & Business Outcome")

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
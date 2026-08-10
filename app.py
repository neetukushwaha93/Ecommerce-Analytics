import streamlit as st
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# ==============================
# Page Settings
# ==============================

st.set_page_config(
    page_title="Ecommerce Analytics",
    page_icon="🛒",
    layout="wide"
)

# ==============================
# MySQL Connection
# ==============================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ecommerce_db"
)

# ==============================
# SQL Query
# ==============================

query = """
SELECT
    o.order_id,
    o.order_date,
    p.product_name,
    p.category,
    oi.quantity,
    p.price,
    (oi.quantity * p.price) AS sales_amount
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'Completed';
"""

# ==============================
# Load Data
# ==============================

df = pd.read_sql(query, connection)

connection.close()

# Convert numeric columns
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce")

df["order_date"] = pd.to_datetime(df["order_date"])

# ==============================
# Title
# ==============================

st.title("🛒 Ecommerce Sales Analytics")
st.write("Ecommerce Sales Dashboard using Python + MySQL")

# ==============================
# Sidebar Filter
# ==============================

st.sidebar.header("Filters")

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df["category"].unique().tolist())
)

if selected_category == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["category"] == selected_category].copy()

# ==============================
# KPI Cards
# ==============================

total_sales = filtered_df["sales_amount"].sum()
total_orders = filtered_df["order_id"].nunique()
total_products = filtered_df["product_name"].nunique()
average_sales = filtered_df["sales_amount"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"₹{total_sales:,.0f}"
)

col2.metric(
    "Total Orders",
    total_orders
)

col3.metric(
    "Products",
    total_products
)

col4.metric(
    "Average Sales",
    f"₹{average_sales:,.0f}"
)

# ==============================
# Charts - 2 Columns
# ==============================

col1, col2 = st.columns(2)

# Category Sales
with col1:

    st.subheader("Sales by Category")

    category_sales = (
        filtered_df.groupby("category")["sales_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)


# Top 5 Products
with col2:

    st.subheader("Top 5 Products")

    product_sales = (
        filtered_df.groupby("product_name")["sales_amount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    st.bar_chart(product_sales)

# ==============================
# Monthly Sales
# ==============================

st.subheader("Monthly Sales")

monthly_sales = (
    filtered_df.groupby(
        filtered_df["order_date"].dt.to_period("M")
    )["sales_amount"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

st.line_chart(monthly_sales)

# ==============================
# Sales Data
# ==============================

st.subheader("Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ==============================
# Download CSV
# ==============================

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Sales Data",
    data=csv_data,
    file_name="ecommerce_sales_data.csv",
    mime="text/csv"
)
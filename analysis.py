import mysql.connector
import pandas as pd


# MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="ecommerce_db"
)

print("Database connected successfully!")


# SQL query
query = """
SELECT
    o.order_id,
    o.order_date,
    c.customer_name,
    c.city,
    p.product_name,
    p.category,
    oi.quantity,
    p.price,
    (oi.quantity * p.price) AS sales_amount
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'Completed';
"""


# SQL data → Pandas DataFrame
df = pd.read_sql(query, connection)


print("\n----- FIRST 5 RECORDS -----")
print(df.head())


print("\n----- TOTAL RECORDS -----")
print(len(df))


print("\n----- COLUMNS -----")
print(df.columns)


print("\n----- TOTAL SALES -----")
print(df["sales_amount"].sum())


print("\n----- AVERAGE SALES -----")
print(df["sales_amount"].mean())


# Close connection
connection.close()



print("\n===== CATEGORY ANALYSIS =====")

category_sales = (
    df.groupby("category")["sales_amount"]
    .sum()
    .sort_values(ascending=False)
)

print(category_sales)


print("\n===== PRODUCT ANALYSIS =====")

product_sales = (
    df.groupby("product_name")["sales_amount"]
    .sum()
    .sort_values(ascending=False)
)

print(product_sales)


print("\n===== CITY ANALYSIS =====")

city_sales = (
    df.groupby("city")["sales_amount"]
    .sum()
    .sort_values(ascending=False)
)

print(city_sales)


print("\n===== TOP CUSTOMER =====")

customer_sales = (
    df.groupby("customer_name")["sales_amount"]
    .sum()
    .sort_values(ascending=False)
)

print(customer_sales.head(5))
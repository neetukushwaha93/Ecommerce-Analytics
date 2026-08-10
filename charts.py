import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# MySQL Connection

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ecommerce_db"
)

# SQL Query

query = """
SELECT
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

# Load Data

cursor = connection.cursor()
cursor.execute(query)

data = cursor.fetchall()

columns = [
    "order_date",
    "product_name",
    "category",
    "quantity",
    "price",
    "sales_amount"
]

df = pd.DataFrame(data, columns=columns)

cursor.close()
connection.close()

print("\nData loaded successfully!")
print(df.head())

# Convert Numeric Columns

df["quantity"] = pd.to_numeric(
    df["quantity"], errors="coerce"
)

df["price"] = pd.to_numeric(
    df["price"], errors="coerce"
)

df["sales_amount"] = pd.to_numeric(
    df["sales_amount"], errors="coerce"
)

# Remove invalid sales values
df = df.dropna(subset=["sales_amount"])

print("\nData Types:")
print(df.dtypes)

# 1. Category Sales Chart

category_sales = (
    df.groupby("category", as_index=True)["sales_amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nCategory Sales:")
print(category_sales)

plt.figure(figsize=(8, 5))

plt.bar(
    category_sales.index,
    category_sales.values
)

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales Amount")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()

# 2. Top 5 Product Sales

product_sales = (
    df.groupby("product_name", as_index=True)["sales_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\nTop 5 Products:")
print(product_sales)

plt.figure(figsize=(8, 5))

plt.bar(
    product_sales.index,
    product_sales.values
)

plt.title("Top 5 Products by Sales")
plt.xlabel("Product")
plt.ylabel("Sales Amount")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

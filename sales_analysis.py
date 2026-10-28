import pandas as pd

# read excel file
df = pd.read_excel("Sales_Data_Raw.xlsx")

# show first 5 rows
print(df.head())

# check dataset information
print(df.info())

# check missing values
print(df.isnull().sum())

# show rows with missing values
print(df[df.isnull().any(axis=1)])

# remove missing rows
df = df.dropna()

# check missing values again
print(df.isnull().sum())

# check duplicate rows
print("Duplicate rows:", df.duplicated().sum())

# remove duplicate rows
df = df.drop_duplicates()

# check duplicates after removing
print("Duplicate rows:", df.duplicated().sum())
print("Rows after removing duplicates:", len(df))

# check negative quantity
print(df[df["Quantity"] < 0])

# check negative sales
print(df[df["Sales"] < 0])

# remove negative sales
df = df[df["Sales"] >= 0]

print("Rows after removing invalid sales:", len(df))

# change order date into date format
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

print(df["Order_Date"].dtype)
print(df["Order_Date"].isnull().sum())

# remove extra spaces and fix text format
df["Product"] = df["Product"].str.strip().str.title()
df["Category"] = df["Category"].str.strip().str.title()
df["Region"] = df["Region"].str.strip().str.title()

# check cleaned text
print(df[["Product", "Category", "Region"]].head(10))

# check profit calculation
df["Calculated_Profit"] = (df["Sales"] - df["Cost"]).round(2)

print(df[df["Profit"].round(2) != df["Calculated_Profit"]])

# remove temporary column
df = df.drop(columns=["Calculated_Profit"])

# check final columns
print(df.columns)

# save cleaned data
df.to_excel("Sales_Data_Cleaned.xlsx", index=False)

print("Cleaned dataset saved successfully!")
# basic sales details
print("Total Sales:", df["Sales"].sum())
print("Total Profit:", df["Profit"].sum())
print("Total Orders:", df["Order_ID"].nunique())
print("Total Quantity:", df["Quantity"].sum())
# sales by product
product_sales = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)

# show top 5 products
print(product_sales.head(5))
# sales by region
region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)

# show sales of each region
print(region_sales)
# get month from order date
df["Month"] = df["Order_Date"].dt.strftime("%B")

# sales by month
monthly_sales = df.groupby("Month")["Sales"].sum()

# show monthly sales
print(monthly_sales)

# get month number
df["Month_Number"] = df["Order_Date"].dt.month

# arrange monthly sales in correct order
monthly_sales = df.groupby(["Month_Number", "Month"])["Sales"].sum().reset_index()
monthly_sales = monthly_sales.sort_values("Month_Number")

# show monthly sales
print(monthly_sales)
# sales by category
category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

# show category sales
print(category_sales)
# profit by product
product_profit = df.groupby("Product")["Profit"].sum().sort_values(ascending=False)

# show top 5 profitable products
print(product_profit.head(5))
# profit by region
region_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)

# show profit of each region
print(region_profit)
# check quantity and sales relationship
quantity_sales = df[["Quantity", "Sales"]]

# show first 10 rows
print(quantity_sales.head(10))
# check correlation between quantity and sales
correlation = df["Quantity"].corr(df["Sales"])

print("Quantity and Sales correlation:", correlation)
# calculate average order value
average_order_value = df["Sales"].sum() / df["Order_ID"].nunique()

print("Average Order Value:", round(average_order_value, 2))
# calculate overall profit margin
profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100

print("Overall Profit Margin:", round(profit_margin, 2), "%")
# profit by category
category_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)

# show profit of each category
print(category_profit)
# calculate profit margin for each product
product_margin = df.groupby("Product").agg({
    "Sales": "sum",
    "Profit": "sum"
})

product_margin["Profit_Margin"] = (
    product_margin["Profit"] / product_margin["Sales"] * 100
)

# show top 5 products by profit margin
print(product_margin.sort_values("Profit_Margin", ascending=False).head(5))
# show bottom 5 products by profit margin
print(product_margin.sort_values("Profit_Margin").head(5))
# save final data for Power BI
df.to_excel("Sales_Data_Final.xlsx", index=False)

print("Final data saved successfully!")
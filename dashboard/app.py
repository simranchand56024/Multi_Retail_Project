import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
from config import db_credentials  # Importing the credentials

st.set_page_config(page_title="Retail Data Analytics Dashboard", layout="wide")

# Database connection function
'''def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="@Amor1908",
        database="ecommerce",
        cursorclass=pymysql.cursors.DictCursor
    )'''
def get_connection():
    return pymysql.connect(
        host=db_credentials['host'],
        user=db_credentials['user'],
        password=db_credentials['password'],
        database=db_credentials['database'],
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to fetch data from MySQL
def fetch_data(query):
    connection = get_connection()
    df = pd.DataFrame()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            df = pd.DataFrame(data)
    finally:
        connection.close()
    return df

# Streamlit App Layout
#st.set_page_config(page_title="Retail Data Analytics Dashboard", layout="wide")
st.sidebar.title("Retail Data Analytics Dashboard")

# Sidebar Navigation
option = st.sidebar.radio("Select Analysis:", [
    "Data Mart Analysis",
    "Aggregation Analysis",
    "KPI Analysis",
    "View Schema",
    "Project Summary"
])

if option == "Data Mart Analysis":
    option = st.selectbox("Choose one..", ("Sales Performance", "Product Category"))
    if option == "Sales Performance":
        st.title("Sales Performance Data Mart")
        df = fetch_data("SELECT * FROM dm_sales_performance order by total_revenue")
        st.dataframe(df)
        df1 = fetch_data("select customer_state,sum(total_revenue) as total_revenue from dm_sales_performance group by customer_state")
        fig = px.bar(df1, x='customer_state', y='total_revenue', title='Total Revenue by State')
        st.plotly_chart(fig, use_container_width=True)

    elif option == "Product Category":
         st.title("Product Category Analysis")
         df = fetch_data("SELECT * FROM dm_product_category_analysis order by product_category_name")
         st.dataframe(df)
         df1 = fetch_data("select product_category_name,sum(total_orders)  as  total_sales from dm_product_category_analysis group by product_category_name limit 20")
         fig = px.bar(df1, x ='product_category_name', y='total_sales', title='Sales by Product Category')
         st.plotly_chart(fig, use_container_width=True)

elif option == "Aggregation Analysis":
    option = st.selectbox("Select one..", ("Total Sales by Customer", "Revenue by Category", "Monthly sales summary", "Daily sales summary"))
    if option == "Daily sales summary":
        df = fetch_data("SELECT * FROM daily_sales_summary order by date")
        st.dataframe(df)
        df1 = fetch_data("SELECT * FROM daily_sales_summary where date between '2023-01-01' and '2023-01-31' order by date")
        fig = px.bar(df1, x='date', y='total_revenue', title='Daily Sales Trend of Jan-2023')
        st.plotly_chart(fig, use_container_width=True)

    elif option == "Monthly sales summary":
         df = fetch_data("SELECT * FROM monthly_sales_summary where year=2021 order by month desc")
         st.dataframe(df)
         fig = px.bar(df, x='month', y='total_revenue', title='Monthly Sales Trend of 2021')
         st.plotly_chart(fig, use_container_width=True)

    elif option == "Revenue by Category":
        df = fetch_data("SELECT * FROM revenue_by_category order by total_revenue desc limit 20")
        st.dataframe(df)
        fig = px.bar(df, x='product_category_name', y='total_revenue', title='Revenue By Category')
        st.plotly_chart(fig, use_container_width=True)
        

    elif option == "Total Sales by Customer":
        df = fetch_data("SELECT * FROM total_sales_by_customer")
        st.dataframe(df)
        fig = px.bar(df, x='customer_id', y='total_orders', title='Total Sales by Customer')
        st.plotly_chart(fig, use_container_width=True)


elif option == "KPI Analysis":
    option = st.selectbox("Select one..", ("Revenue by Payment Method", " Top 5 Best-Selling Product Categories", "Sales By State", "Number of Orders per Year"))
    if option == "Revenue by Payment Method":
        df = fetch_data("SELECT dp.payment_type,  SUM(dp.payment_value) AS total_revenue FROM dim_payments dp GROUP BY dp.payment_type ORDER BY total_revenue DESC")
        st.dataframe(df)
        fig = px.pie(df, names='payment_type', values='total_revenue', title='Revenue by Payment Method',)
        st.plotly_chart(fig, use_container_width=True)

    elif option == " Top 5 Best-Selling Product Categories":
         df = fetch_data("SELECT dpc.product_category_name, SUM(dpc.total_orders) AS total_sales FROM dm_product_category_analysis dpc GROUP BY dpc.product_category_name ORDER BY total_sales DESC LIMIT 5;")
         st.dataframe(df)
         fig = px.bar(df, x='product_category_name', y='total_sales', title='Top 5 Best-Selling Product categories')
         st.plotly_chart(fig, use_container_width=True)

    elif option == "Sales By State":
        df = fetch_data("SELECT customer_state, sum(total_orders) as total_sales from dm_sales_performance group by customer_state order by customer_state")
        st.dataframe(df)
        fig = px.bar(df, x='customer_state', y='total_sales', title='Sales By State')
        st.plotly_chart(fig, use_container_width=True)
        

    elif option == "Number of Orders per Year":
        df = fetch_data("SELECT dd.year AS year, COUNT(fo.order_id) AS total_orders FROM fact_orders fo JOIN dim_dates dd ON fo.purchase_date_id = dd.date_id GROUP BY year")
        st.dataframe(df)
        fig = px.pie(df, names='year', values='total_orders', title='Number of Orders per Year')
        st.plotly_chart(fig, use_container_width=True)

elif option == "View Schema":
    st.title("Star Schema of Sales Project")
    st.image(r"C:\Users\91639\Desktop\Multi retail\dashboard\star_schema.png")


elif option == "Project Summary":
    st.title("Project Summary Report")

    st.markdown("""
    ## **1. Project Overview**  
This project centers around creating a **Retail Data Analytics Dashboard** designed to analyze and visualize data from e-commerce retail operations. It leverages **MySQL** for efficient data storage and utilizes **Streamlit** for developing interactive reports. The dashboard offers vital insights into **sales performance, product trends, and key business KPIs**, all structured within a **star schema-based data warehouse**.

## **2. Data Processing & Storage** 
- **Data Cleaning & Transformation:** Addressed missing data and optimized data types for performance.  
- **Star Schema Design:** Utilized Fact and Dimension tables to enable fast and efficient querying.  
- **Data Loading into MySQL:** Applied **INSERT IGNORE** to avoid duplicate records during insertion.  

## **3. Dashboard Features & Analysis**  
- **Data Mart Analysis:** Insights into sales performance and product category trends.  
- **Aggregation Analysis:** Analyzes revenue patterns, along with sales breakdowns by customer and product category.  
- **KPI Analysis:** Evaluates payment methods, best-selling categories, and sales performance by state.  
- **Schema Visualization:** Provides a graphical view of the underlying data architecture.

## **4. Technologies Used**  
- **Python & Streamlit** for building the interactive dashboard.  
- **MySQL & pymysql** for backend database management.  
- **Pandas & Plotly** for data processing and creating visualizations.  

## **5. Key Outcomes**  
- Fully interactive **Retail Data Analytics Dashboard** with real-time reporting.  
- **Optimized database structure** to support fast queries and large data sets.  
- Provides **actionable insights** into sales performance and key business metrics.  
""")
st.sidebar.markdown("---")
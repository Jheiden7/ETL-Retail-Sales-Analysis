import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

#%% DATA LOADING PHASE
#Load database
data = pd.read_excel("online_retail_II.xlsx", sheet_name = "Year 2009-2010")

#%% PROCESS PHASE AND PREPARATION OF THE FINAL DATA SET
data_new = data.drop(columns=["Description"])
#Remove duplicate data, because they provide sales that are not real
data_new = data_new.drop_duplicates()
#Invalid data
data_new = data_new[data_new["Price"] >= 0]
data_new = data_new[data_new["Quantity"] >= 0]
#data_new = data_new.reset_index(drop=True)

# Page settings
st.set_page_config(layout="wide")
st.title('Online Retail Analysis Dashboard')

# Sidebar for variable and date selection
st.sidebar.header('Chart Settings')
variable = st.sidebar.selectbox('Select the variable to display:', options=['Quantity', 'Price'])
start_date = st.sidebar.date_input('Start date:', value=data_new['InvoiceDate'].min().date())
end_date = st.sidebar.date_input('End date:', value=data_new['InvoiceDate'].max().date())

# Convert to datetime64 and normalize
start_date = pd.to_datetime(start_date).normalize()
end_date = pd.to_datetime(end_date).normalize()

# Filter data by date
filtered_data = data_new[(data_new['InvoiceDate'] >= start_date) & (data_new['InvoiceDate'] <= end_date)]

# VARIABLE TO VISUALIZE 1: Sales by customer
#%% Creation of the Sales column, to know the total price paid in each record of the database
data_new['Sales'] = data_new['Quantity'] * data_new['Price']
#Create copy
data_prefiltrada = data_new
#Remove missing data, because this data, for the particular objective of obtaining the number of sales according to the Customer ID variable
data_new = data_new.dropna()
#Transformation of Customer ID data to string
data_new.loc[:, 'Customer ID'] = data_new['Customer ID'].apply(str)
#Group the numerical data with respect to Customer ID
df_numerico = data_new.select_dtypes(include=[np.number])
dfnuevo = df_numerico.groupby(by=data_new["Customer ID"]).sum()
# Sort Customer ID by Sales, in descending order
dfnuevo = dfnuevo.sort_values(by = 'Sales', ascending = False)

#Chart - Sales by Customer ID
st.header('Sales by Customer ID')
fig, ax = plt.subplots()
ax.bar(x = dfnuevo.index[:10], height = dfnuevo["Sales"].head(10), color='#69b3a2')
ax.set_xlabel('Customer ID')
ax.set_ylabel('Sales')
ax.set_title('Sales by Customer ID')
st.pyplot(fig)

#Select the numerical columns
df_num = data_prefiltrada.select_dtypes(include=[np.number])

#Group by countries, to obtain the total sales for each country
data_paises = df_num.groupby(by = data_new['Country']).sum()
#Order countries by sales, in descending order
data_paises = data_paises.sort_values(by = 'Sales', ascending = False)

#Chart - Sales by Country
st.header('Sales by country')
fig, ax = plt.subplots()
ax.bar(x = data_paises.index[:10], height = data_paises["Sales"].head(10), color='#67b4a2')
ax.set_xlabel('Country')
ax.set_ylabel('Sales')
ax.set_title('Sales by Country')
st.pyplot(fig)

#Separate year, month and day from Invoice Date
data_meses = data_prefiltrada
data_meses['Year'] = pd.to_datetime(data_meses['InvoiceDate']).dt.year
data_meses['Month'] = pd.to_datetime(data_meses['InvoiceDate']).dt.month
data_meses['Day'] = pd.to_datetime(data_meses['InvoiceDate']).dt.day

#Convert integers to string
data_meses['Day'] = data_meses['Day'].astype(str)
data_meses['Month'] = data_meses['Month'].astype(str)
data_meses['Year'] = data_meses['Year'].astype(str)

#Create new columns with the year-month-day and year_month format, to be able to group the sales
data_meses ['Year_Month_Day'] = data_meses['Year'] + '-' + data_meses['Month'] + '-' + data_meses['Day']
data_meses ['Year_Month'] = data_meses['Year'] + '-' + data_meses['Month']

#Group by year-month-day, to obtain the total sales for each date
data_num_mes = data_prefiltrada.select_dtypes(include=[np.number])
data_amd = data_num_mes.groupby(by=data_meses['Year_Month_Day']).sum()

#Organize date by sales, in descending order
data_amd = data_amd.sort_values(by = 'Sales', ascending = False)

#Chart - Sales by Date
st.header('Sales by date')
fig, ax = plt.subplots()
ax.bar(x = data_amd.index[:10], height = data_amd["Sales"].head(10), color='#67b4a2')
ax.set_xlabel('Date (Year - Month)')
ax.set_ylabel('Sales')
ax.set_title('Sales by Date (Year - Month - Day)')
st.pyplot(fig)

#Group by year-month, to obtain the total sales for each date, excluding the day
data_am = data_num_mes.groupby(by=data_meses['Year_Month']).sum()

#Organize date by sales, in descending order
data_am = data_am.sort_values(by = 'Sales', ascending = False)

#Chart - Sales by Date
st.header('Sales by year and month')
fig, ax = plt.subplots()
ax.bar(x = data_am.index[:10], height = data_am["Sales"].head(10), color='#67b4a2')
ax.set_xlabel('Date (Year - Month)')
ax.set_ylabel('Sales')
ax.set_title('Sales by Date (Year - month)')
st.pyplot(fig)

#Dataset for stockcode vs Quantity
data_quantity = df_num.groupby(by = data_prefiltrada['StockCode']).sum()
#Organize StockCode by quantity
data_quantity = data_quantity.sort_values(by = 'Quantity', ascending = False)

#Chart - StockCode vs Quantity
st.header('Quantity sold by product')
fig, ax = plt.subplots()
ax.bar(x = data_quantity.index[:10].astype(str), height = data_quantity["Quantity"].head(10), color='#67b4a2')
ax.set_xlabel('StockCode')
ax.set_ylabel('Quantity')
ax.set_title('Quantity vs StockCode')
st.pyplot(fig)

# Deployment and testing:
# Test the dashboard locally using the instruction in the CLI
# python -m streamlit run dashboard_produccion_online_retail_v2.py
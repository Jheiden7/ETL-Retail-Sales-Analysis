#%% Phase 1. Data Loading
#1.1 Load the database
import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_excel('online_retail_II.xlsx', sheet_name='Year 2009-2010')

#%% Phase 2. Data Preprocessing
# 2.1 Data exploration
# 2.2 Data cleaning and transformation
# Remove rows with missing values and unwanted columns
df.dropna(subset=['Customer ID'], inplace=True)
df = df.drop(columns=['Invoice'],axis = 1)  # Remove 'InvoiceNo'

# Convert 'InvoiceDate' to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Group by 'Customer ID' and count the number of monthly purchases
df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
customer_freq = df.groupby(['Customer ID', 'YearMonth']).size().groupby('Customer ID').mean()

# Create a new label column: 1 if the customer is frequent, 0 if not
threshold = customer_freq.quantile(0.75)  # For example, the 75th percentile as a threshold
customer_freq = customer_freq.apply(lambda x: 1 if x >= threshold else 0)

# Prepare the final DataFrame for the classification model
df['Customer Freq'] = df['Customer ID'].map(customer_freq)
df.dropna(subset=['Customer Freq'], inplace=True)
df['Customer Freq'] = df['Customer Freq'].astype(int)

# Encoding of categorical variables
df['StockCode'] = df['StockCode'].astype(str)
le = LabelEncoder()
df['StockCode'] = le.fit_transform(df['StockCode'])

# Features and labels
X = df[['StockCode', 'Quantity', 'Price']]  # Simplified example of features
y = df['Customer Freq']

#%% PHASE 3: MACHINE LEARNING MODELING
# 3.1 Feature selection and data splitting
# 3.2 Model building and training
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# # 3.3 Model evaluation
from sklearn.metrics import classification_report, confusion_matrix

y_pred = model.predict(X_test)
# print(confusion_matrix(y_test, y_pred))
# print(classification_report(y_test, y_pred))

#%% Phase 4: Creating the Dashboard in Streamlit
# 4.1 Basic structure
import streamlit as st

# Page settings
st.set_page_config(layout="wide")
st.title('Online Retail Analysis Dashboard')

# 3.2 Integration of graphics
import matplotlib.pyplot as plt
import seaborn as sns

# Sidebar for variable and date selection
st.sidebar.header('Chart Settings')
variable = st.sidebar.selectbox('Select the variable to display:', options=['Quantity', 'Price'])
start_date = st.sidebar.date_input('Start date:', value=df['InvoiceDate'].min().date())
end_date = st.sidebar.date_input('End date:', value=df['InvoiceDate'].max().date())

# Convert to datetime64 and normalize
start_date = pd.to_datetime(start_date).normalize()
end_date = pd.to_datetime(end_date).normalize()

# Filter data by date
filtered_data = df[(df['InvoiceDate'] >= start_date) & (df['InvoiceDate'] <= end_date)]

# Chart display
st.header('Data Visualization')
fig, ax = plt.subplots()
ax.plot(filtered_data['InvoiceDate'], filtered_data[variable])
ax.set_title(f'{variable} Chart by Date')
ax.set_xlabel('Date')
ax.set_ylabel(variable)
st.pyplot(fig)

# # dst.subheader('Confusion Matrix')
st.header('Confusion Matrix')
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt='d', ax=ax, cmap='Blues')
ax.set_xlabel('Predicted')
ax.set_ylabel('Actual')
ax.set_title('Confusion Matrix')
st.pyplot(fig)

# # Classification Report
st.header('Classification Report')
report = classification_report(y_test, y_pred, output_dict=True)
df_report = pd.DataFrame(report).transpose()
st.dataframe(df_report)

# 3.3 Deployment and testing
# Test the dashboard locally using the instruction in the CLI:
# python -m streamlit run "Streamlit Dashboards/dashboard_online_retail.py"
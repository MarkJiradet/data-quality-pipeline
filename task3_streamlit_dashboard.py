import streamlit as st
import duckdb
import pandas as pd

# เชื่อมต่อ DuckDB
con = duckdb.connect("ecommerce.duckdb")

# ดึงข้อมูลทั้งหมดมาใช้ filter ได้
df_all = con.execute("SELECT * FROM historical").fetchdf()

# Sidebar Filters
st.sidebar.header("Filters")
categories = st.sidebar.multiselect("Select Categories", options=df_all['category'].unique(), default=list(df_all['category'].unique()))
payments = st.sidebar.multiselect("Select Payment Methods", options=df_all['payment_method'].unique(), default=list(df_all['payment_method'].unique()))
date_range = st.sidebar.date_input("Select Date Range", value=[pd.to_datetime(df_all['timestamp']).min(), pd.to_datetime(df_all['timestamp']).max()])

# Apply filters
df_all['timestamp'] = pd.to_datetime(df_all['timestamp'])
df_filtered = df_all[
    (df_all['category'].isin(categories)) &
    (df_all['payment_method'].isin(payments)) &
    (df_all['timestamp'].dt.date.between(date_range[0], date_range[1]))
]

st.title("🧹 Data Quality Dashboard")

# 1. Summary Stats
st.header("Summary Statistics")
st.write(f"Total Transactions: {len(df_filtered):,}")
st.write(f"Total Amount: ${df_filtered['amount'].sum():,.2f}")

# 2. Status Bar Chart
st.header("Transaction Status Distribution")
status_counts = df_filtered['status'].value_counts().reset_index()
status_counts.columns = ['status', 'count']
st.bar_chart(status_counts.set_index('status'))

# 3. Data Quality Issues Table
st.header("Data Quality Issues")
# 3.1 ยอดติดลบ
neg_amounts = df_filtered[df_filtered['amount'] < 0]
# 3.2 void/cancel ไม่มี completed
void_or_cancel = df_filtered[df_filtered['status'].isin(['void', 'cancel'])]
# ตรวจว่าไม่มี completed ซ้ำ
completed_ids = set(df_filtered[df_filtered['status'] == 'completed']['transaction_id'])
void_without_completed = void_or_cancel[~void_or_cancel['transaction_id'].isin(completed_ids)]

st.subheader("❌ Negative Amounts")
st.dataframe(neg_amounts)

st.subheader("❌ Void/Cancel without Completed")
st.dataframe(void_without_completed)

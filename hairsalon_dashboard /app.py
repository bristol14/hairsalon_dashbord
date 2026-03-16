import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib

plt.rcParams['font.family'] = 'Hiragino Sans'

st.title("2026年3月売上結果")

df = pd.read_excel("hairsalon_sales_1month_varied.xlsx")

stylist = st.selectbox("スタイリストを選択",["全員"] + list(df["スタイリスト"].unique()))

if stylist != "全員":
    df = df[df["スタイリスト"] == stylist]


total_sales = df["合計売上"].sum()
total_customers = df["客数"].sum()
ave_price = total_sales / total_customers
working_days = df ["日付"].nunique()
working_hours = working_days * 8 #実質労働時間を8時間で計算してます
Productivity = total_sales / working_hours 

col1,col2,col3,col4 = st.columns([2,1.5,1.5,2])

with col1:
    st.metric("総売上",f"{total_sales:,.0f}円")

with col2:
    st.metric("総客数",f"{total_customers:,.0f}人") 

with col3:
    st.metric("平均客単価",f"{ave_price:,.0f}円") 

with col4:
    st.metric("1時間あたりの生産性",f"{Productivity:,.0f}円")  


st.subheader("KPI")   

st.subheader("売上データ")

st.dataframe(df)

st.subheader("各スタイリスト売上合計")

stylist_sales = df.groupby("スタイリスト")["合計売上"].sum()
st.bar_chart(stylist_sales )

st.subheader("各スタイリスト技術売上")
technique_sales = df.groupby("スタイリスト")["技術売上"].sum()
st.bar_chart(technique_sales)

st.subheader("各スタイリスト店販売上")
store_sales = df.groupby("スタイリスト")["店販売上"].sum()
st.bar_chart(store_sales)

st.subheader("各スタイリスト入客数")
customers = df.groupby("スタイリスト")["客数"].sum()
st.bar_chart(customers)

st.title("各スタイリスト客単価")
average_price = df.groupby("スタイリスト")["合計売上"].sum() / df.groupby("スタイリスト")["客数"].sum()
st.bar_chart(average_price)

st.title("スタイリスト売上ランキング")
ranking = stylist_sales.sort_values(ascending=False)
st.bar_chart(ranking)

st.subheader("日別売上")
daily_sales = df.groupby("日付")["合計売上"].sum()
st.line_chart(daily_sales)

fig, ax = plt.subplots()
ax.ticklabel_format(style='plain', axis='y')
ax.bar(range(len(ranking)), ranking.values)
ax.set_xticks(range(len(ranking)))
ax.set_xticklabels(ranking.index)
ax.bar(ranking.index, ranking.values)

ax.set_xlabel("スタイリスト")
ax.set_ylabel("売上")
ax.set_title("スタイリスト売上ランキング")

plt.xticks(rotation=0)

st.pyplot(fig)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import numpy as np


# core function

st.title("Dashboard For Rent Bicycles",)
datasets_daily= pd.read_csv("./hour.csv")

datasets_daily.dteday=pd.to_datetime(datasets_daily.dteday)
min_date = datasets_daily["dteday"].min()
max_date = datasets_daily["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("./gambar.png",use_column_width='auto')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date=st.date_input(
        label='Rentang Waktu Rental Sepeda',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    st.subheader("Image Credit")
    st.markdown("URL: [Rental Bike](#https://id.pngtree.com/freepng/vector-illustration-of-a-bicycle-rental-logo-on-a-white-background-vector_10130394.html)")

# secure dates
main = datasets_daily[(datasets_daily["dteday"] >= str(start_date)) & 
                (datasets_daily["dteday"] <= str(end_date))]


# added daily order base on input users
def create_daily_order_rent(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    daily_rent_df.rename(columns={
        "order_id": "instant",
        "total_rent": "cnt"
    }, inplace=True)
    
    return daily_rent_df

#
def customers_visual():
    
    comparision_users=datasets_daily.groupby([datasets_daily.workingday]).agg({
        'instant':'nunique',
        'casual':'sum',
        'registered':"sum",
        'cnt':"sum"
    }).reset_index()


    figure,ax=plt.subplots(figsize=(10,5))


    len_x_data=np.arange(len(comparision_users))
    # # change number for years
    comparision_users.workingday.replace({0:'Hari Libur',1:"Hari Kerja"}, inplace=True)
    ax.bar(len_x_data+.2,comparision_users.casual,.4,label="Not Unregestered")
    ax.bar(len_x_data-.2,comparision_users.registered,.4,label="Registered")

    plt.xticks(len_x_data,comparision_users.workingday)
    plt.legend()
    return figure

def season_visual():
    
    tahun11=datasets_daily[datasets_daily.yr==0].groupby(by="season").cnt.sum().reset_index()
    tahun12=datasets_daily[datasets_daily.yr==1].groupby(by="season").cnt.sum().reset_index()

    tahun11.season.replace({1:'Spring',2:'Summer',3:'Fall',4:'Winter'},inplace=True)

    # find range x
    x=np.arange(len(tahun11))

    fig_season,ax_season= plt.subplots(figsize=(5,5))

    ax_season.bar(x-0.2,tahun11.cnt,0.4,label='Tahun 2011')
    ax_season.bar(x+0.2,tahun12.cnt,0.4,label='Tahun 2012')

    plt.xticks(x,tahun11.season)

    return fig_season

def comparison_visual():

    rent_years=datasets_daily.groupby('yr').cnt.sum().reset_index()
    rent_years.yr.replace({0:'Tahun 2011',1:'tahun 2012'},inplace=True)
    fig,ax=plt.subplots(figsize=(5, 5))
    
    sns.barplot(
        y="cnt", 
        x="yr",
        data=rent_years,
    )
    plt.ylabel(None)
    plt.xlabel(None)

    return  fig
daily_orders_rent_df = create_daily_order_rent(main)
# header
st.header('Dashboard Rent Bicycle :sparkles:')
 
total_orders = daily_orders_rent_df.cnt.sum()
st.metric("Total orders Rent Bicycles", value=total_orders)

# added ploting by input users
rent_bicycle_day=daily_orders_rent_df.groupby(by="dteday").cnt.sum().reset_index()

fig,ax= plt.subplots(figsize=(16,8))

ax.plot(
    rent_bicycle_day.dteday,
    rent_bicycle_day.cnt,
    marker='o',
)

 
st.pyplot(fig)


st.subheader("Comparision Rent Bicycles")

col1,col2=st.columns(2)
with col1:
    # ploting season 
    ploting_season=season_visual()

    st.subheader("By season")
    st.pyplot(ploting_season)



plt.title("Number of Rent Bicycle By Year", loc="center", fontsize=15)
plt.ylabel(None)


with col2:
    ploting_years=comparison_visual()
    st.subheader("By Years")
    st.pyplot(ploting_years)


st.write("Berdasarkan Visualisasi diatas dapat diketahui bahwa penggunaan rental sepeda terjadi peningkatan setiap tahun dan juga penggunaan rental sepda paling tinggi terjadi pada musim gugur  dan paling rendah musim semi")
    

st.header("Pengguna Rental Sepeda")

ploting_users=customers_visual()
st.write("Dapat dilihat berdasarkan visual distribusi penggunaan rental sepeda banyak digunakan pada saat hari kerja")
st.pyplot(ploting_season)
    
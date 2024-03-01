import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from sklearn.cluster import KMeans

sns.set(style='dark')

#Menyiapkan data day_df
day_df = pd.read_csv("Dashboard/day.csv")
day_df.head()

#Menyiapkan data hour_df
hour_df = pd.read_csv("Dashboard/hour.csv")
hour_df.head()

#Mengubah beberapa detail tentang kolom pada day_df
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

day_df.head()

#Mengubah beberapa detail tentang kolom pada hour_df
hour_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count',
    'hr' : 'hour'
}, inplace=True)

hour_df.head()

# Mengubah angka pada day_df menjadi keterangan
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
day_df['weather_cond'] = day_df['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Mengubah angka pada hour_df menjadi keterangan
hour_df['month'] = hour_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
hour_df['season'] = hour_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
hour_df['weekday'] = hour_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
hour_df['weather_cond'] = hour_df['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return weather_rent_df

# Membuat komponen filter
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()
 
with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

#Membuat Dashboard
#Judul
st.header('Bike Sharing Dashboard')

# Fungsi untuk visualisasi berdasarkan musim
def plot_seasonal_sharing():
    season_analysis_day = day_df.iloc[:, [2, 13, 14, 15]]
    season_analysis_day.groupby('season').sum()

    # Mengelompokkan data berdasarkan musim dan menghitung jumlah penggunaan terdaftar dan tidak terdaftar
    seasonal_usage = season_analysis_day.groupby('season')[['registered', 'casual', 'count']].sum().reset_index()

    plt.figure(figsize=(10, 6))

    # Menentukan lebar setiap bar
    bar_width = 0.4

    # Membuat
    season_index = np.arange(len(seasonal_usage['season']))
    plt.bar(
        season_index - bar_width/2,
        seasonal_usage['registered'],
        width=bar_width,
        label='Registered',
        color='tab:blue'
    )

    plt.bar(
        season_index + bar_width/2,
        seasonal_usage['casual'],
        width=bar_width,
        label='Casual',
        color='tab:orange'
    )

    plt.xlabel('Musim')
    plt.ylabel('Total Peminjaman Sepeda')
    plt.title('Jumlah penyewaan sepeda berdasarkan musim')
    plt.xticks(season_index, seasonal_usage['season'])  # Set label sumbu x
    plt.legend()

    # Tampilkan plot
    st.pyplot(plt)

# Fungsi untuk visualisasi rata-rata peminjaman per jam
def plot_hourly_sharing():
    rental_jam = hour_df.groupby('hour')['count'].mean()

    st.bar_chart(rental_jam)
    
# Fungsi untuk visualisasi peminjaman saat hari libur
def plot_holiday_sharing():
    libur = ['Tidak Libur', 'Libur']
    holiday_analysis_day = day_df.iloc[:,[5, 13, 14, 15]]
    holiday_analysis_day['holiday'] = holiday_analysis_day['holiday'].replace([0, 1], libur)
    holiday_analysis_day_result = holiday_analysis_day.groupby('holiday').sum()

    # Mengelompokkan data berdasarkan musim dan menghitung jumlah penggunaan terdaftar dan tidak terdaftar
    holiday_usage = holiday_analysis_day.groupby('holiday')[['registered', 'casual', 'count']].sum().reset_index()

    plt.figure(figsize=(10, 6))

    # Menentukan lebar setiap bar
    bar_width = 0.4

    # Membuat
    holiday_index = np.arange(len(holiday_usage['holiday']))
    plt.bar(
        holiday_index - bar_width/2,
        holiday_usage['registered'],
        width=bar_width,
        label='Registered',
        color='tab:blue'
    )

    plt.bar(
        holiday_index + bar_width/2,
        holiday_usage['casual'],
        width=bar_width,
        label='Casual',
        color='tab:orange'
    )

    plt.xlabel('Hari Libur')
    plt.ylabel('Total Peminjaman Sepeda (Jutaan)')
    plt.title('Jumlah penyewaan sepeda berdasarkan Hari Libur')
    plt.xticks(holiday_index, holiday_usage['holiday'])  # Set label sumbu x
    plt.legend()

    # Tampilkan plot
    st.pyplot(plt)

# Memanggil fungsi untuk setiap visualisasi
st.subheader('Seasonal Sharing')
plot_seasonal_sharing()

st.subheader('Hourly Sharing')
plot_hourly_sharing()

st.subheader('Holiday Sharing')
plot_holiday_sharing()

st.caption('Copyright (c) Dinar Ferdiansyah')

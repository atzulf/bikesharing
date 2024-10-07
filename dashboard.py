import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='dark')

# digunakan untuk menyiapkan berbagai dataframe
def create_day_orders_df(df):
    day_orders_df = df.groupby('weekday')['total_count'].sum().reset_index()
    return day_orders_df

def create_weather_order_avg_df(df):
    weather_order_avg_df = df.groupby('weather')['total_count'].mean().reset_index()
    return weather_order_avg_df

def create_season_order_avg_df(df):
    season_order_avg_df = df.groupby('season')['total_count'].mean().reset_index()
    return season_order_avg_df

def create_hour_order_df(df):
    hour_order_df = df.groupby('hour')['total_count'].sum().reset_index()
    return hour_order_df

# Pemanggilan dataset clean csv
day_df = pd.read_csv("./dashboard/dayclean.csv")
hour_df = pd.read_csv("./dashboard/hourclean.csv")

# Mengubah kolom date menjadi datetime
day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Mengubah tahun menjadi date
day_df['year'] = day_df['date'].dt.year

# Filter data berdasarkan tanggal yang dipilih
min_date = day_df['date'].min()
max_date = day_df['date'].max()

with st.sidebar:
    # Add a company logo (if available)
    st.image("./dashboard/rental3.jpg")
    
    # Memilih tanggal untuk sidebar
    start_date, end_date = st.date_input(
        label='Select Date Range', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

main_day_df = day_df[(day_df['date'] >= str(start_date)) & (day_df['date'] <= str(end_date))]

# mempersiapkan berbagai dataframe yang berbeda
daily_orders_df = create_day_orders_df(main_day_df)
weather_order_avg_df = create_weather_order_avg_df(main_day_df)
season_order_avg_df = create_season_order_avg_df(main_day_df)
hour_order_df = create_hour_order_df(hour_df)

# Merupakan tampilan header
st.header('Bike Sharing Dashboard :sparkles:')

# 1. Menampilkan ringkasan total penyewaan sepeda
st.subheader("Total Bike Rentals Summary")

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_day_df['total_count'].sum()
    st.metric("Total Bike Rentals", value=total_rentals)

with col2:
    total_casual = main_day_df['casual_users'].sum()
    st.metric("Total Casual Rentals", value=total_casual)

with col3:
    total_registered = main_day_df['registered_users'].sum()
    st.metric("Total Registered Rentals", value=total_registered)

# 1. Total penyewaan berdasarkan jam
st.subheader("Total Penyewaan Sepeda berdasarkan Jam")

# Mencari jam penyewaan perbanyak
max_rentals_hour = hour_order_df[hour_order_df['total_count'] == hour_order_df['total_count'].max()]['hour'].values[0]
max_rentals_value = hour_order_df['total_count'].max()
st.write(f"Jam dengan penyewaan sepeda terbanyak: **{max_rentals_hour}** dengan total penyewaan **{max_rentals_value}**.")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="hour", y="total_count", data=hour_order_df, palette="Blues_d", ax=ax)
ax.set_title("Penyewaan berdasarkan Jam")
ax.text(max_rentals_hour, max_rentals_value, 'Tertinggi', color='red', ha='center')
st.pyplot(fig)

# 2. Total penyewaam sepeda berdasarkan hari dalam minggu
st.subheader("Total Rental Sepeda Per Hari dalam 1 Minggu")

# Mencari penyewaan hari terbanyak
max_rentals_day = daily_orders_df[daily_orders_df['total_count'] == daily_orders_df['total_count'].max()]['weekday'].values[0]
max_rentals_value = daily_orders_df['total_count'].max()
st.write(f"Hari dengan penyewaan sepeda terbanyak: **{max_rentals_day}** dengan total penyewaan **{max_rentals_value}**.")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="weekday", y="total_count", data=daily_orders_df, palette="Blues_d", ax=ax)
ax.set_title("Total Rental Sepeda Per Hari dalam 1 Minggu")
ax.text(max_rentals_day, max_rentals_value, 'Tertinggi', color='red', ha='center')
st.pyplot(fig)

# 3. Penyewaan berdasarkan musim
st.subheader("Penyewaan Berdasarkan Musim")

# Mengelompokkan berdasarkan musim
seasonal_rentals = main_day_df.groupby('season', observed=True)['total_count'].sum().reset_index()

# Menampilkan musim dengan penyewaan terbanyak
max_rentals_season = seasonal_rentals[seasonal_rentals['total_count'] == seasonal_rentals['total_count'].max()]['season'].values[0]
max_rentals_value = seasonal_rentals['total_count'].max()
st.write(f"Musim dengan penyewaan sepeda terbanyak: **{max_rentals_season}** dengan total penyewaan **{max_rentals_value}**.")

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(seasonal_rentals['season'], seasonal_rentals['total_count'], color='lightgreen')

# Menambahkan judul pada bar musim
ax.set_xlabel('Season')
ax.set_ylabel('Total rental sepeda')
ax.set_title('Total Bike Rentals per musim')
ax.text(max_rentals_season, max_rentals_value, 'Tertinggi', color='red', ha='center')

st.pyplot(fig)

# 4. Penyewaan sepeda berdasarkan kondisi cuaca
st.subheader("Rata-rata Rental Sepeda Berdasarkan Kondisi Cuaca")

# Mencari kondisi cuaca agar menampilkan total penyewaan sepeda terbanyak
max_rentals_weather = weather_order_avg_df[weather_order_avg_df['total_count'] == weather_order_avg_df['total_count'].max()]['weather'].values[0]
max_rentals_value = weather_order_avg_df['total_count'].max()
st.write(f"Kondisi cuaca dengan penyewaan sepeda terbanyak: **{max_rentals_weather}** dengan rata-rata penyewaan **{max_rentals_value}**.")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="weather", y="total_count", data=weather_order_avg_df, palette="Blues_d", ax=ax)
ax.set_title("Penyewaan Berdasarkan Kondisi Cuaca")
ax.text(max_rentals_weather, max_rentals_value, 'Tertinggi', color='red', ha='center')
st.pyplot(fig)

# 5. Total penyewaan sepeda dalam dua tahun terakhir
st.subheader("Total Penyewaan Sepeda Berdasarkan Tahun")

# Menggabungkan kedua tahun dan menampilkan ke bar
yearly_rentals = main_day_df.groupby('year')['total_count'].sum().reset_index()

# Mencari tahun penyewaaan terbanyak
max_rentals_year = yearly_rentals[yearly_rentals['total_count'] == yearly_rentals['total_count'].max()]['year'].values[0]
max_rentals_value = yearly_rentals['total_count'].max()
st.write(f"Tahun dengan penyewaan sepeda terbanyak: **{max_rentals_year}** dengan total penyewaan **{max_rentals_value}**.")

# Menambahkan hasil ke plot bar
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(yearly_rentals['year'], yearly_rentals['total_count'], color='orange')

# Menambahkan judul tahun
ax.set_xlabel('Year')
ax.set_ylabel('Total Bike Rentals')
ax.set_title('Total Rental sepeda per Tahun')

# Adding data labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

st.pyplot(fig)

st.caption('Bike Sharing Dashboard_Dicoding_Ataka Dzulfikar')

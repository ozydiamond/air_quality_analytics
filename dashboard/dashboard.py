import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# -----------------------
# LOAD DATA
# -----------------------

file_path = 'dashboard/clean_all_df.csv'
if not os.path.exists(file_path):
    st.error(f"File tidak ditemukan: {file_path}")
else:
    all_df = pd.read_csv(file_path)


# -----------------------
# FUNCTION
# -----------------------
def add_date_column(df):
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    return df

def average_daily_pollutants(df):
    return df.groupby('date')[['PM2.5', 'PM10', 'O3', 'SO2', 'NO2', 'CO']].mean().reset_index()

def highest_pollution_day(df):
    daily_pm25 = df.groupby('date')['PM2.5'].mean()
    return daily_pm25.idxmax(), daily_pm25.max()

def average_temp_rain(df):
    return df['TEMP'].mean(), df['RAIN'].mean()

def unhealthy_pm25_days(df, threshold=55.5):
    df['date'] = pd.to_datetime(df['date'])
    daily_pm25 = df.groupby('date')['PM2.5'].mean()
    return daily_pm25[daily_pm25 > threshold].count()

# -----------------------
# SIDEBAR FILTER
# -----------------------
st.sidebar.image("wind.png", width=200)
st.sidebar.header("🔍 Filter Data")

# Station filter
station_list = all_df['station'].unique().tolist()
selected_stations = st.sidebar.multiselect("Pilih Kota/Station", options=station_list, default=station_list)

# Add 'date' column
all_df = add_date_column(all_df)

# Date filter
min_date = all_df['date'].min()
max_date = all_df['date'].max()
selected_date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)

# -----------------------
# DATA FILTERING
# -----------------------
df_filtered = all_df[
    (all_df['station'].isin(selected_stations)) &
    (all_df['date'] >= pd.to_datetime(selected_date_range[0])) &
    (all_df['date'] <= pd.to_datetime(selected_date_range[1]))
]

# -----------------------
# METRICS CALCULATION
# -----------------------
daily_avg_df = average_daily_pollutants(df_filtered)
max_day, max_value = highest_pollution_day(df_filtered)
avg_temp, avg_rain = average_temp_rain(df_filtered)
unhealthy_days = unhealthy_pm25_days(df_filtered)

# -----------------------
# DASHBOARD DISPLAY
# -----------------------
st.title("📊 Dashboard Kualitas Udara")

# --- RATA-RATA POLUTAN ---
st.markdown("### 🔹 Rata-rata Harian Polutan")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

col1.metric("PM2.5", f"{daily_avg_df['PM2.5'].mean():.2f} µg/m³")
col2.metric("PM10", f"{daily_avg_df['PM10'].mean():.2f} µg/m³")
col3.metric("O3", f"{daily_avg_df['O3'].mean():.2f} µg/m³")

col4.metric("SO2", f"{daily_avg_df['SO2'].mean():.2f} µg/m³")
col5.metric("NO2", f"{daily_avg_df['NO2'].mean():.2f} µg/m³")
col6.metric("CO", f"{daily_avg_df['CO'].mean():.2f} µg/m³")

# --- POLUSI TERTINGGI & HARI TIDAK SEHAT ---
st.markdown("### 🔹 Informasi Polusi Penting")
col7, col8 = st.columns(2)
col7.metric("📅 Hari PM2.5 Tertinggi", f"{max_day.date()}", f"{max_value:.2f} µg/m³")
col8.metric("❗ Hari Tidak Sehat (PM2.5 > 55.5)", f"{unhealthy_days} Hari")

# --- CUACA RATA-RATA ---
st.markdown("### 🔹 Cuaca Rata-rata")
col9, col10 = st.columns(2)
col9.metric("🌡️ Suhu Rata-rata", f"{avg_temp:.2f} °C")
col10.metric("🌧️ Curah Hujan", f"{avg_rain:.2f} mm")

# --- LINE CHART PM2.5 per Kota ---
st.markdown("### 📉 Rata-rata Harian PM2.5 per Kota")

if not df_filtered.empty:
    pm25_by_station = (
        df_filtered.groupby(['date', 'station'])['PM2.5']
        .mean()
        .reset_index()
        .dropna()
    )

    fig_pm25 = px.line(
        pm25_by_station,
        x='date',
        y='PM2.5',
        color='station',
        title='Rata-rata Harian PM2.5 per Kota',
        labels={'date': 'Tanggal', 'PM2.5': 'PM2.5 (µg/m³)', 'station': 'Kota'}
    )
    fig_pm25.update_layout(legend_title="Kota")
    st.plotly_chart(fig_pm25, use_container_width=True)
else:
    st.warning("Data PM2.5 tidak tersedia untuk periode yang dipilih.")


# --- LINE CHART Suhu per Kota ---
st.markdown("### 🌡️ Rata-rata Suhu Harian per Kota")

if not df_filtered.empty and 'TEMP' in df_filtered.columns:
    temp_by_station = (
        df_filtered.groupby(['date', 'station'])['TEMP']
        .mean()
        .reset_index()
        .dropna()
    )

    fig_temp = px.line(
        temp_by_station,
        x='date',
        y='TEMP',
        color='station',
        title='Rata-rata Suhu Harian per Kota',
        labels={'date': 'Tanggal', 'TEMP': 'Suhu (°C)', 'station': 'Kota'}
    )
    fig_temp.update_layout(legend_title="Kota")
    st.plotly_chart(fig_temp, use_container_width=True)
else:
    st.warning("Data suhu tidak tersedia untuk periode yang dipilih.")

# --- PM2.5 per STATION ---
st.markdown("### 🌆 Rata-rata PM2.5 per Kota (Station)")
pm25_by_city = df_filtered.groupby('station')['PM2.5'].mean().reset_index().dropna()
pm25_by_city = pm25_by_city.sort_values(by='PM2.5', ascending=True)

fig_horizontal = px.bar(
    pm25_by_city,
    x='PM2.5',
    y='station',
    color='PM2.5',
    color_continuous_scale='Plasma_r',
    orientation='h',
    title='Rata-rata PM2.5 per Station',
    labels={'station': 'Kota (Station)', 'PM2.5': 'Rata-rata PM2.5'}
)

fig_horizontal.update_layout(
    xaxis_title='Rata-rata PM2.5',
    yaxis_title=None,
    coloraxis_colorbar=dict(title="PM2.5"),
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig_horizontal, use_container_width=True)

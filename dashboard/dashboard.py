import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("clean_all_df.csv")
    df["date"] = pd.to_datetime(df[["year", "month", "day"]])
    return df

df = load_data()

# FUNCTION
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
    unhealthy_days = daily_pm25[daily_pm25 > threshold].count()
    total_days = daily_pm25.count()
    return unhealthy_days, total_days



# Sidebar
st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.title("Filter")

# Filter Tanggal
min_date = df["date"].min().date()
max_date = df["date"].max().date()
selected_date = st.sidebar.date_input(
    "Pilih rentang tanggal", [min_date, max_date],
    min_value=min_date, max_value=max_date
)

# Filter Kota
cities = df["station"].unique().tolist()
selected_cities = st.sidebar.multiselect("Pilih kota", cities, default=cities)
if len(selected_cities) == 0:
    st.sidebar.error("⚠️ Anda harus memilih setidaknya satu kota.")
    st.stop()

# Terapkan filter
filtered_df = df[
    (df["station"].isin(selected_cities)) &
    (df["date"] >= pd.to_datetime(selected_date[0])) &
    (df["date"] <= pd.to_datetime(selected_date[1]))
]

# Metrics Calculation
daily_avg_df = average_daily_pollutants(filtered_df)
max_day, max_value = highest_pollution_day(filtered_df)
avg_temp, avg_rain = average_temp_rain(filtered_df)
unhealthy_days, total_days = unhealthy_pm25_days(filtered_df)

# Title
st.title("📊 Air Quality Dashboard - China (2013–2017)")

# Informasi Rata-rata Polutan
st.markdown("### 🔹 Rata-rata Harian Polutan")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

col1.metric("PM2.5", f"{daily_avg_df['PM2.5'].mean():.2f} µg/m³")
col2.metric("PM10", f"{daily_avg_df['PM10'].mean():.2f} µg/m³")
col3.metric("O3", f"{daily_avg_df['O3'].mean():.2f} µg/m³")

col4.metric("SO2", f"{daily_avg_df['SO2'].mean():.2f} µg/m³")
col5.metric("NO2", f"{daily_avg_df['NO2'].mean():.2f} µg/m³")
col6.metric("CO", f"{daily_avg_df['CO'].mean():.2f} µg/m³")

# Polusi tertinggi dan hari tidak sehat
st.markdown("### 🔹 Informasi Polusi Penting")
col7, col8 = st.columns(2)
col7.metric("📅 Hari PM2.5 Tertinggi", f"{max_day.date()}", f"{max_value:.2f} µg/m³")
col8.metric("❗ Hari Tidak Sehat (PM2.5 > 55.5)",
            f"{unhealthy_days} Hari",
            f"Dari total {total_days} hari")


# Visualisasi Tren PM2.5
st.markdown("### Rata-rata Harian PM2.5 per Kota")

if not filtered_df.empty:
    pm25_by_station = (
        filtered_df.groupby(['date', 'station'])['PM2.5']
        .mean()
        .reset_index()
        .dropna()
    )

    fig_pm25 = px.line(
        pm25_by_station,
        x='date',
        y='PM2.5',
        color='station',
        labels={'date': 'Tanggal', 'PM2.5': 'PM2.5 (µg/m³)', 'station': 'Kota'}
    )
    fig_pm25.update_layout(legend_title="Kota")
    st.plotly_chart(fig_pm25, use_container_width=True)
else:
    st.warning("Data PM2.5 tidak tersedia untuk periode yang dipilih.")

# Tren PM2.5 dan PM10 tiap kota pertahun
st.markdown("### Tren Tahunan PM2.5 dan PM10 per Kota")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("#### PM2.5 per Tahun")
    yearly_pm25 = (
        filtered_df.groupby(['year', 'station'])['PM2.5']
        .mean().reset_index().dropna()
    )

    fig_yearly_pm25 = px.line(
        yearly_pm25,
        x='year',
        y='PM2.5',
        color='station',
        markers=True,
        labels={'year': 'Tahun', 'PM2.5': 'Rata-rata PM2.5', 'station': 'Kota'}
    )
    fig_yearly_pm25.update_layout(legend_title="Kota", xaxis=dict(dtick=1))
    st.plotly_chart(fig_yearly_pm25, use_container_width=True)

with col_b:
    st.markdown("#### PM10 per Tahun")
    yearly_pm10 = (
        filtered_df.groupby(['year', 'station'])['PM10']
        .mean().reset_index().dropna()
    )

    fig_yearly_pm10 = px.line(
        yearly_pm10,
        x='year',
        y='PM10',
        color='station',
        markers=True,
        labels={'year': 'Tahun', 'PM10': 'Rata-rata PM10', 'station': 'Kota'}
    )
    fig_yearly_pm10.update_layout(legend_title="Kota", xaxis=dict(dtick=1))
    st.plotly_chart(fig_yearly_pm10, use_container_width=True)


#rata rata PM2.5 per kota seluruh tahun
st.markdown("### Rata-rata PM2.5 per Kota (Station)")
pm25_by_city = filtered_df.groupby('station')['PM2.5'].mean().reset_index().dropna()
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

# Visualisasi Korelasi
st.subheader("Korelasi Polutan dan Cuaca")
corr_cols = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO',
       'O3', 'TEMP', 'PRES', 'DEWP', 'WSPM']
corr_df = filtered_df[corr_cols].dropna().corr()

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_df, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

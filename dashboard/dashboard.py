import numpy as np # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
import streamlit as st # type: ignore

# Helper function


# Trend penyewaan bulanan 

# all users
def create_monthly_trend(df):
    monthly_trend_df = df.groupby(by=["month", "year"]).agg({
        'rent_count': 'mean',
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_trend_df = monthly_trend_df.reindex(ordered_months, fill_value=0)
    return monthly_trend_df

def create_monthly_trend_byCasual(df):
    monthly_trend_byCasual_df = df.groupby(by=["year", "month"]).agg({
        'casual': 'mean',
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_trend_byCasual_df = monthly_trend_byCasual_df.reindex(ordered_months, fill_value=0)
    return monthly_trend_byCasual_df

def create_monthly_trend_byRegistered(df):
    monthly_trend_byRegistered_df = df.groupby(by=["year", "month"]).agg({
        'casual': 'mean',
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_trend_byRegistered_df = monthly_trend_byRegistered_df.reindex(ordered_months, fill_value=0)
    return monthly_trend_byRegistered_df

# Jumlah penyewaan sepeda berdasarkan musim dan cuaca
def create_seasonal(df):
    seasonal_df = days_df.groupby("season")["rent_count"].sum().reset_index()

    return seasonal_df

def create_weathersituation(df):
    days_df["weathersituation"] = pd.Categorical(
    days_df["weathersituation"].replace({1:"Sunny", 2: "Cloudy", 3: "Light Rain/Snow", 4: "Heavy Rain/Thunderstorm"}), categories=["Sunny", "Cloudy", "Light Rain/Snow", "Heavy Rain/Thunderstorm"]
    )

    weathersituation_df = days_df.groupby("weathersituation")["rent_count"].sum().reset_index()

    return weathersituation_df

def create_temperature(df):
    min_temp = 0
    max_temp = 30

    temperature_df = hours_df

    temperature_df["temp_in_celsius"] = (temperature_df["temp"] * (max_temp - min_temp) + min_temp)    

    temperature_df["temp_in_celsius"].astype(float)
    
    return temperature_df

def create_humidity(df):
    humidity_df = hours_df

    humidity_df["humidity_percent"] = (humidity_df["humidity"] * 100)

    humidity_df["humidity_percent"].astype(float)


    return humidity_df


def create_windspeed(df):
    windspeed_df = hours_df
    
    windspeed_df["windspeed_mps"] = (windspeed_df["windspeed"] * windspeed_df["windspeed"])

    windspeed_df["windspeed_mps"].astype(float)

    return windspeed_df

# Bike Rent Usage Schedule
def create_rentSchedule_by_casual(df):
    bins = [0, 6, 12, 18, 24]  # Batas jam
    labels = ['Dini Hari', 'Pagi', 'Siang', 'Malam']
    hours_df['time_of_day'] = pd.cut(hours_df['hour'], bins=bins, labels=labels, right=False)

    rentSchedule_by_casual_df = df.pivot_table(index='weekday', columns='time_of_day', values='casual', aggfunc='mean')

    return rentSchedule_by_casual_df

def create_rentSchedule_by_registered(df):
    bins = [0, 6, 12, 18, 24]  # Batas jam
    labels = ['Dini Hari', 'Pagi', 'Siang', 'Malam']
    hours_df['time_of_day'] = pd.cut(hours_df['hour'], bins=bins, labels=labels, right=False)

    rentSchedule_by_registered_df = df.pivot_table(index='weekday', columns='time_of_day', values='registered', aggfunc='mean')

    return rentSchedule_by_registered_df

# load berkas file csv

days_upload = pd.read_csv('./main_days.csv')
if days_upload is not None:
    days_df = days_upload
else:
    days_df = "./main_days.csv"

hours_upload = pd.read_csv('./main_hours.csv')
if hours_upload is not None:
    hours_df = hours_upload
else:
    hours_df = "./main_hours.csv"
# days_df = pd.read_csv('./main_days.csv')
# hours_df = pd.read_csv('./main_hours.csv')

days_df["datetime"] = pd.to_datetime(days_df["datetime"])

# Membuat sidebar filter pada trend monthly
min_date = pd.to_datetime(days_df['datetime']).dt.date.min()
max_date = pd.to_datetime(days_df['datetime']).dt.date.max()

with st.sidebar:

    st.subheader("Welcome✨")

    sum_rent = days_df.rent_count.sum()
    st.metric("🚴🏾Total Riders", value=sum_rent)
    
    col1, col2 =st.columns(2)

    with col1:
        sum_rent_registered = days_df.registered.sum()
        st.metric("Registered", value=sum_rent_registered)

    with col2:
        sum_rent_casual = days_df.casual.sum()
        st.metric("Casual", value=sum_rent_casual)

    # Mengambil start_date & end_date dari data_input, digunakan untuk memfilter DataFrame
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    

main_df = days_df[(days_df['datetime'] >= str(start_date)) & 
                (days_df['datetime'] <= str(end_date))]



# Panggil helper function
monthly_trend_df = create_monthly_trend(main_df)
monthly_trend_byCasual_df = create_monthly_trend_byCasual(main_df)
monthly_trend_byRegistered_df = create_monthly_trend_byRegistered(main_df)
seasonal_df = create_seasonal(main_df)
weathersituation_df = create_weathersituation(main_df)
temperature_df = create_temperature(hours_df)
humidity_df = create_humidity(hours_df)
windspeed_df = create_windspeed(hours_df)
rentSchedule_by_casual_df = create_rentSchedule_by_casual(hours_df)
rentSchedule_by_registered_df = create_rentSchedule_by_registered(hours_df)



st.header('Dico Bike Rent Dashboard 2011 & 2012 🚲')

# Trend grafik monthly trend
st.subheader('Average Monthly Rent📅')

col1, col2, col3 = st.columns(3)

with col1:
    avg_rent_all = round(main_df.rent_count.mean(),1)
    st.metric("All Users", value=avg_rent_all)

with col2:
    avg_rent_registered = round(main_df.registered.mean(),1)
    st.metric("Registered", value=avg_rent_registered)

with col3:  
    avg_rent_casual = round(main_df.casual.mean(),1)
    st.metric("Casual", value=avg_rent_casual)
 

fig, ax = plt.subplots(figsize=(10,6))
sns.lineplot(
    x='month', 
    y='rent_count', 
    hue='year', 
    data=main_df, 
    marker='o',  
    palette={2011: "darkred", 2012: "salmon"},
    ax=ax
)

sns.lineplot(x='month', y='casual', hue='year', data=main_df, marker='o',  palette={2011: "navy", 2012: "lightblue"}, ax=ax)

sns.lineplot(x='month', y='registered', hue='year', data=main_df, marker='o', palette={2011: "darkgreen", 2012: "limegreen"}, ax=ax)

ax.set_xlabel('Month')
ax.set_ylabel('Rent Total')
ax.set_xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des'])

# Menambahkan judul
plt.title("Monthly Rent Trend by User Type and Year")

# Menambahkan legenda secara manual
custom_lines = [
    plt.Line2D([2011],[2011],color="darkred", marker='o', label="Total Rent (2011)"),
    plt.Line2D([2012],[2012],color="salmon", marker='o', label="Total Rent (2012)"),
    plt.Line2D([2011],[2011],color="navy", marker='o', label="Casual User (2011)"),
    plt.Line2D([2012], [2012],color="lightblue", marker='o', label="Casual User (2012)"),
    plt.Line2D([2011] ,[2011],color="darkgreen", marker='o', label="Registered User (2011)"),
    plt.Line2D([2012],[2012],color="limegreen", marker='o', label="Registered User (2012)"),
]

ax.legend(handles=custom_lines, title="Category-Year", loc="upper right")

plt.tight_layout()
st.pyplot(fig)





# Season and Weather

st.subheader("Season and Weather Situation 🌤")


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Temperature", value=round(temperature_df["temp_in_celsius"][55],4))

with col2:
    st.metric("Humidity", value=humidity_df["humidity_percent"][34])

with col3:  
    st.metric("Windspeed", value=round(windspeed_df["windspeed_mps"][78],3))


# Kondisi Musim dan Cuaca dalam peminjaman sepeda
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

days_df.rename(columns={
    "count": "rent_count"
},inplace=True)

colors=  ["#D3D3D3",  "#D3D3D3","#72BCD4", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    y="rent_count",
    x="season",
    data=days_df,
    estimator="mean",
    palette=colors,
    errorbar=None,
    ax=ax[0]
)
ax[0].set_title("Season", loc="center", fontsize=30)

colors=  ["#72BCD4","#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    y="rent_count",
    x="weathersituation",
    data=days_df,
    estimator="mean",
    palette=colors,
    errorbar=None,
    ax=ax[1]
)
ax[1].set_title("Weather Situation", loc="center", fontsize=30)

st.pyplot(fig)



# Jadwal penggunaan sepeda per hari
st.subheader("Bike Rent Schedule🕐")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(17, 4))


sns.heatmap(rentSchedule_by_casual_df, cmap='Blues', linewidths=0.5, ax=ax[0])
ax[0].set_title('Casual',loc="center", fontsize=30)
ax[0].set_xlabel('Time of Day')
ax[0].set_ylabel('Weekday')
ax[0].set_yticks(ticks=range(1, 8), labels=['Sun','Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])


sns.heatmap(rentSchedule_by_registered_df, cmap='Blues', linewidths=0.5, ax=ax[1])
ax[1].set_title('Registered',loc="center", fontsize=30)
ax[1].set_xlabel('Time of Day')
ax[1].set_ylabel('Weekday')
ax[1].set_yticks(ticks=range(1, 8), labels=['Sun','Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])

st.pyplot(fig)





import numpy as np # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
import streamlit as st # type: ignore

# Helper function

# Trend penyewaan bulanan 

# all users
def create_monthly_trend(df):
    monthly_trend_df = days_df.groupby("month")["rent_count"].mean().reset_index()
    return monthly_trend_df

# Casual User
def create_monthly_trend_byCasual(df):
    monthly_trend_byCasual_df = days_df.groupby("month")["casual"].mean().reset_index()

    return monthly_trend_byCasual_df

def create_monthly_trend_byRegistered(df):
    monthly_trend_byRegistered_df = days_df.groupby("month")["registered"].mean().reset_index()

    return monthly_trend_byRegistered_df

# Jumlah penyewaan sepeda berdasarkan musim dan cuaca
def create_seasonal(df):
    seasonal_df = days_df.groupby("season")["rent_count"].sum().reset_index()

    return seasonal_df

def create_weathersituation(df):
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
days_df = pd.read_csv('dashboard/main_days.csv')
hours_df = pd.read_csv('dashboard/main_hours.csv')


# Panggil helper function
monthly_trend_df = create_monthly_trend(days_df)
seasonal_df = create_seasonal(days_df)
monthly_trend_byCasual_df = create_monthly_trend_byCasual(days_df)
monthly_trend_byRegistered_df = create_monthly_trend_byRegistered(days_df)
weathersituation_df = create_weathersituation(days_df)
temperature_df = create_temperature(hours_df)
humidity_df = create_humidity(hours_df)
windspeed_df = create_windspeed(hours_df)
rentSchedule_by_casual_df = create_rentSchedule_by_casual(hours_df)
rentSchedule_by_registered_df = create_rentSchedule_by_registered(hours_df)


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
    



st.header('Dico Bike Rent Dashboard 2011 & 2012 🚲')

# Trend grafik monthly trend
st.subheader('Average Monthly Rent📅')

col1, col2, col3 = st.columns(3)

with col1:
    avg_rent_all = round(days_df.rent_count.mean(),1)
    st.metric("All Users", value=avg_rent_all)

with col2:
    avg_rent_registered = round(days_df.registered.mean(),1)
    st.metric("Registered", value=avg_rent_registered)

with col3:  
    avg_rent_casual = round(days_df.casual.mean(),1)
    st.metric("Casual", value=avg_rent_casual)
 


fig = plt.figure(figsize=(16,8))
    
plt.fill_between(monthly_trend_df["month"],monthly_trend_df["rent_count"],color="blue", alpha=0.3, label="Total Users")

plt.fill_between(monthly_trend_byCasual_df["month"] ,monthly_trend_byCasual_df["casual"],color="orange", alpha=0.3, label="Casual")

plt.fill_between(monthly_trend_byRegistered_df["month"],monthly_trend_byRegistered_df["registered"],color="green", alpha=0.3, label="Registered")


plt.xlabel('Month')
plt.ylabel('Average')
plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des'])
plt.legend(loc="upper right")
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
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

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

colors=  ["#D3D3D3", "#72BCD4", "#D3D3D3", "#D3D3D3"]

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





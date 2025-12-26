import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_KEY = "4dfa4f1e0205dfff63617a0c22a9a2ae"

st.title("🌦️ Multi-City Weather Dashboard")

# ----------------------------------
# Load city list from CSV
# ----------------------------------
city_df = pd.read_csv("cities_list.csv")
city_list = city_df["City"].tolist()

# ----------------------------------
# Select Multiple Cities
# ----------------------------------
selected = st.multiselect(
    "Select Cities",
    city_list,
)

if st.button("Fetch Weather"):

    if len(selected) == 0:
        st.warning("⚠ Select at least one city.")
        st.stop()

    temp, humidity, pressure, wind = [], [], [], []

    # ------------- API LOOP --------------
    for city in selected:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={API_KEY}&units=metric"
        )
        data = requests.get(url).json()

        if "main" not in data:
            temp.append(None)
            humidity.append(None)
            pressure.append(None)
            wind.append(None)
        else:
            temp.append(data["main"]["temp"])
            humidity.append(data["main"]["humidity"])
            pressure.append(data["main"]["pressure"])
            wind.append(data.get("wind", {}).get("speed", None))

    # ------------- DATAFRAME --------------
    df = pd.DataFrame({
        "City": selected,
        "Temperature (°C)": temp,
        "Humidity (%)": humidity,
        "Pressure (hPa)": pressure,
        "Wind (m/s)": wind
    })

    st.subheader("📋 Weather Table")
    st.dataframe(df)

    # ======================================
    # Remove Rows With None to avoid plot error
    # ======================================
    df_clean = df.dropna()

    if df_clean.empty:
        st.error("❌ No valid weather data found!")
        st.stop()

    # ======================================
    # Dynamic filename
    # ======================================
    clean = [c.lower().replace(" ", "") for c in df_clean["City"].tolist()]
    filename = "_".join(clean)

    # save CSV
    df_clean.to_csv(f"{filename}.csv", index=False)
    st.success(f"CSV saved: {filename}.csv")

    # ======================================
    # GRAPH SECTION
    # ======================================
    st.subheader("📊 Weather Comparison Charts")

    # ----- Temperature -----
    fig1, ax1 = plt.subplots()
    ax1.bar(df_clean["City"], df_clean["Temperature (°C)"])
    ax1.set_ylabel("°C")
    ax1.set_title("Temperature Comparison")
    st.pyplot(fig1)
    fig1.savefig(f"{filename}_temperature.png")

    # ----- Humidity -----
    fig2, ax2 = plt.subplots()
    ax2.bar(df_clean["City"], df_clean["Humidity (%)"])
    ax2.set_ylabel("%")
    ax2.set_title("Humidity Comparison")
    st.pyplot(fig2)
    fig2.savefig(f"{filename}_humidity.png")

    # ----- Pressure -----
    fig3, ax3 = plt.subplots()
    ax3.bar(df_clean["City"], df_clean["Pressure (hPa)"])
    ax3.set_ylabel("hPa")
    ax3.set_title("Pressure Comparison")
    st.pyplot(fig3)
    fig3.savefig(f"{filename}_pressure.png")

    # ----- Wind -----
    fig4, ax4 = plt.subplots()
    ax4.bar(df_clean["City"], df_clean["Wind (m/s)"])
    ax4.set_ylabel("m/s")
    ax4.set_title("Wind Speed Comparison")
    st.pyplot(fig4)
    fig4.savefig(f"{filename}_wind.png")

    st.success("All graphs saved to folder!")

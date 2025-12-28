# Import required libraries
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# OpenWeatherMap API key
API_KEY = "4dfa4f1e0205dfff63617a0c22a9a2ae"

# App title
st.title("🌦️ Multi-City Weather Dashboard")

# Load city list from CSV file (This CSV contains all available city names)
city_df = pd.read_csv("cities_list.csv")
city_list = city_df["City"].tolist()

# Allow user to select multiple cities

selected = st.multiselect(
    "Select Cities",
    city_list,
)

# When user clicks the Fetch Weather button
if st.button("Fetch Weather"):

    # If no city is selected, show warning
    if len(selected) == 0:
        st.warning("⚠ Select at least one city.")
        st.stop()

    # Lists to store weather data
    temp, humidity, pressure, wind = [], [], [], []

    # Fetch weather data for each city
    for city in selected:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={API_KEY}&units=metric"
        )

        # Call API and convert response to JSON
        data = requests.get(url).json()

        # If city data is not found, store None
        if "main" not in data:
            temp.append(None)
            humidity.append(None)
            pressure.append(None)
            wind.append(None)
        else:
            # Store required weather parameters
            temp.append(data["main"]["temp"])
            humidity.append(data["main"]["humidity"])
            pressure.append(data["main"]["pressure"])
            wind.append(data.get("wind", {}).get("speed", None))
            
    # Create a Pandas DataFrame
    df = pd.DataFrame({
        "City": selected,
        "Temperature (°C)": temp,
        "Humidity (%)": humidity,
        "Pressure (hPa)": pressure,
        "Wind (m/s)": wind
    })

    # Display weather table
    st.subheader("📋 Weather Table")
    st.dataframe(df)

    # Remove rows with missing values (so graphs do not crash)
    df_clean = df.dropna()

    if df_clean.empty:
        st.error("❌ No valid weather data found!")
        st.stop()

    # Create dynamic filename using city names
    clean = [c.lower().replace(" ", "") for c in df_clean["City"].tolist()]
    filename = "_".join(clean)

    # Save the clean data to CSV
    df_clean.to_csv(f"{filename}.csv", index=False)
    st.success(f"CSV saved: {filename}.csv")
    
    # Graph Section
    st.subheader("📊 Weather Comparison Charts")

    # ----- Temperature Chart -----
    fig1, ax1 = plt.subplots()
    ax1.bar(df_clean["City"], df_clean["Temperature (°C)"])
    ax1.set_ylabel("°C")
    ax1.set_title("Temperature Comparison")
    st.pyplot(fig1)
    fig1.savefig(f"{filename}_temperature.png")

    # ----- Humidity Chart -----
    fig2, ax2 = plt.subplots()
    ax2.bar(df_clean["City"], df_clean["Humidity (%)"])
    ax2.set_ylabel("%")
    ax2.set_title("Humidity Comparison")
    st.pyplot(fig2)
    fig2.savefig(f"{filename}_humidity.png")

    # ----- Pressure Chart -----
    fig3, ax3 = plt.subplots()
    ax3.bar(df_clean["City"], df_clean["Pressure (hPa)"])
    ax3.set_ylabel("hPa")
    ax3.set_title("Pressure Comparison")
    st.pyplot(fig3)
    fig3.savefig(f"{filename}_pressure.png")

    # ----- Wind Speed Chart -----
    fig4, ax4 = plt.subplots()
    ax4.bar(df_clean["City"], df_clean["Wind (m/s)"])
    ax4.set_ylabel("m/s")
    ax4.set_title("Wind Speed Comparison")
    st.pyplot(fig4)
    fig4.savefig(f"{filename}_wind.png")

    # Final success message
    st.success("All graphs saved to folder!")

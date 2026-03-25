import streamlit as st
import requests
import datetime
import pandas as pd
import plotly.express as px

# -------------------------------
# CONFIG
# -------------------------------
API_KEY = "your_api_key_here"

# -------------------------------
# FUNCTIONS
# -------------------------------
def get_weather(city, units="metric"):
    """Fetch current weather data for a city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
    response = requests.get(url)
    return response.json()

def get_forecast(city, units="metric"):
    """Fetch 5-day forecast data for a city."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}"
    response = requests.get(url)
    return response.json()

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.title("🌦️ Real-Time Weather App")

# Input city
city = st.text_input("Enter city name", "Hyderabad")

# Unit toggle
unit = st.radio("Select unit", ("metric", "imperial"))
unit_label = "°C" if unit == "metric" else "°F"

if city:
    # Current weather
    data = get_weather(city, units=unit)

    if data.get("main"):
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        description = data["weather"][0]["description"].title()
        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        st.subheader(f"Current Weather in {city}")
        st.image(icon_url)
        st.write(f"*Condition:* {description}")
        st.write(f"🌡️ Temperature: {temp}{unit_label}")
        st.write(f"💧 Humidity: {humidity}%")
        st.write(f"🌅 Sunrise: {sunrise}")
        st.write(f"🌇 Sunset: {sunset}")

        # Forecast
        forecast_data = get_forecast(city, units=unit)
        df = pd.DataFrame([
            {
                "datetime": item["dt_txt"],
                "temp": item["main"]["temp"]
            }
            for item in forecast_data["list"]
        ])

        st.subheader("📈 5-Day Forecast")
        fig = px.line(df, x="datetime", y="temp", title=f"Temperature Forecast ({unit_label})")
        st.plotly_chart(fig)

    else:
        st.error("City not found. Please try again.")
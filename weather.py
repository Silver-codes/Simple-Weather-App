import streamlit as st
import requests
import os
import json

with open("descriptions.json", "r", encoding="utf-8") as file:
        weather_dict = json.load(file)

st.title("Weather App")

user_input_city = st.text_input("Enter a city:")
if user_input_city:

    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={user_input_city}&count=5"
    geo_data = requests.get(geo_url).json()
    city_options = []
    for result in geo_data["results"]:
        formatted_name = f"{result['name']}, {result['country']}"
        city_options.append(formatted_name)

    selected_location = st.selectbox("Did you mean:", city_options)

    chosen_city_index = city_options.index(selected_location)

    latitude = geo_data["results"][chosen_city_index]["latitude"]
    longitude = geo_data["results"][chosen_city_index]["longitude"]

    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&timezone=auto")


    data = response.json()
    temperature = data["current_weather"]["temperature"]
    windspeed = data["current_weather"]["windspeed"]
    time = data["current_weather"]["time"]
    if data["current_weather"]["is_day"] == 1:
        day_night = "day"
    else:
        day_night = "night"
    weather_code = data["current_weather"]["weathercode"]
    weather_descritpion = weather_dict[str(weather_code)][day_night]["description"]


    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("latitude: ", latitude)
    with col2:
        st.write("longitude: ", longitude)
    with col3:
        st.write(f"Time of measurement: {time}")

    col1, col2, col3= st.columns(3)
    with col1:
        st.metric(label="Current temperature", value=f"{temperature}°C")
    with col2:
        st.metric(label="Current windspeed", value= f"{windspeed}m/s")
    with col3:
        st.metric(label="Current weather code", value= f"{weather_descritpion}")

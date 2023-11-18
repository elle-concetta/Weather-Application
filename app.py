import datetime
import streamlit as st
import requests
from streamlit_folium import folium_static
import folium

# Insert API key which is pasted in secrets file
api_key = "23f9fc8b-0cda-4723-b605-7a3972ceaf7d"

st.title("Weather and Air Quality")
st.header("Mumbai, India")


@st.cache_data
def fetch_aqi_data(city_req, state_req, country_req):
    aqi_data_url = f"https://api.airvisual.com/v2/city?city={city_req}&state={state_req}&country={country_req}&key={api_key}"
    response = requests.get(aqi_data_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


@st.cache_data
def map_creator(map_lat, map_long):
    m = folium.Map(location=[map_lat, map_long], zoom_start=10)
    folium.Marker([map_lat, map_long], popup="Mumbai", tooltip="Mumbai").add_to(m)
    folium_static(m)


# Hardcoded values for Mumbai, India
city_name = "Mumbai"
state_name = "Maharashtra"
country_name = "India"

aqi_data = fetch_aqi_data(city_name, state_name, country_name)

if aqi_data and aqi_data["status"] == "success":
    data = aqi_data["data"]
    st.write(f"Weather and Air Quality for {city_name}, {state_name}, {country_name}:")

    # Displaying the data
    st.write(f"Temperature: {data['current']['weather']['tp']} °C")
    st.write(f"Humidity: {data['current']['weather']['hu']}%")
    st.write(f"Air Quality Index (AQI): {data['current']['pollution']['aqius']}")

    # Displaying the map
    latitude = data["location"]["coordinates"][1]
    longitude = data["location"]["coordinates"][0]
    map_creator(latitude, longitude)
else:
    st.error("Failed to fetch data for Mumbai, India.")

# Background color picker
st.markdown("<h1 style='text-align: left; color: white;'>Weather Report 🌦️</h1>", unsafe_allow_html=True)

bgcolor = st.color_picker('Customize your background color', '#000000')
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-color: {bgcolor}
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    measurements = st.radio("Measurement preference?", ["Metric", "Imperial"])

with col2:
    try:
        if city_name:
            current_time = datetime.datetime.now().time()
            input_time = st.time_input('Enter a time', value=current_time)

    except Exception as e:
        st.error(f'Error: {e}')

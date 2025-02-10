
import streamlit as st
import pandas as pd
import math
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    return R * (2 * math.asin(math.sqrt(a)))

def find_nearest_store(user_location, stores):
    return min(((store, haversine_distance(user_location[0], user_location[1], store["lat"], store["lon"])) for store in stores), key=lambda x: x[1], default=(None, float('inf')))

def geocode_city(city_name):
    try:
        geolocator = Nominatim(user_agent="store_locator_app")
        location = geolocator.geocode(city_name, timeout=10)
        return (location.latitude, location.longitude) if location else None
    except GeocoderTimedOut:
        return None

def app():
    st.title("Nearest Store Finder by City")
    city = st.text_input("Enter your city:", "New York")
    stores = [
        {"name": "Store A", "lat": 40.7128, "lon": -74.0060},
        {"name": "Store B", "lat": 34.0522, "lon": -118.2437},
        {"name": "Store C", "lat": 41.8781, "lon": -87.6298},
        {"name": "Store D", "lat": 29.7604, "lon": -95.3698},
        {"name": "Store E", "lat": 33.4484, "lon": -112.0740},
        {"name": "Delhi Store", "lat": 28.627393, "lon": 77.171695},
        {"name": "Kanpur Store", "lat": 26.460, "lon": 80.321}
    ]
    
    if st.button("Find Nearest Store") and city:
        user_location = geocode_city(city)
        if user_location:
            st.success(f"Your location: Latitude {user_location[0]:.6f}, Longitude {user_location[1]:.6f}")
            nearest_store, distance = find_nearest_store(user_location, stores)
            if nearest_store:
                st.success(f"Nearest store is **{nearest_store['name']}** at **{distance:.2f} km**.")
                
                store_data = [{"name": store["name"], "lat": store["lat"], "lon": store["lon"], "color": [255, 0, 0] if store["name"] == nearest_store["name"] else [0, 0, 255]} for store in stores]
                store_data.append({"name": "Your Location", "lat": user_location[0], "lon": user_location[1], "color": [0, 255, 0]})
                df_locations = pd.DataFrame(store_data)
                
                layer = pdk.Layer("ScatterplotLayer", data=df_locations, get_position='[lon, lat]', get_color="color", get_radius=20000, pickable=True)
                view_state = pdk.ViewState(latitude=user_location[0], longitude=user_location[1], zoom=5, pitch=0)
                st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"html": "<b>{name}</b>", "style": {"color": "white"}}))
            else:
                st.error("No stores available to determine the nearest location.")
        else:
            st.error("Could not geocode the specified city.")

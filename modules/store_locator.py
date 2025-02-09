# modules/store_locator.py
import streamlit as st
import pandas as pd
import math
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth using the Haversine formula.
    
    Parameters:
        lat1, lon1: Latitude and longitude of point 1 (in decimal degrees)
        lat2, lon2: Latitude and longitude of point 2 (in decimal degrees)
        
    Returns:
        distance (float): Distance between the two points in kilometers.
    """
    R = 6371.0  # Earth radius in kilometers
    # Convert degrees to radians.
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def find_nearest_store(user_location, stores):
    """
    Given the user's location and a list of stores, find the nearest store.
    
    Parameters:
        user_location (tuple): A tuple (latitude, longitude) for the user's location.
        stores (list): A list of dictionaries, each containing:
                        - "name": Store name (str)
                        - "lat": Latitude (float)
                        - "lon": Longitude (float)
                        
    Returns:
        nearest_store (dict): The dictionary for the nearest store.
        min_distance (float): The distance (in kilometers) to the nearest store.
    """
    min_distance = float('inf')
    nearest_store = None
    for store in stores:
        distance = haversine_distance(user_location[0], user_location[1], store["lat"], store["lon"])
        if distance < min_distance:
            min_distance = distance
            nearest_store = store
    return nearest_store, min_distance

def geocode_city(city_name):
    """
    Convert a city name into latitude and longitude using the Nominatim geocoder.
    
    Parameters:
        city_name (str): The name of the city.
        
    Returns:
        (lat, lon) tuple if successful; otherwise, None.
    """
    try:
        geolocator = Nominatim(user_agent="store_locator_app")
        location = geolocator.geocode(city_name, timeout=10)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except GeocoderTimedOut:
        return None

def app():
    st.title("Nearest Store Finder by City")
    st.write(
        "Enter the name of your city below to find the nearest store from our pre-defined list of store locations."
    )
    
    # Pre-defined store locations (example coordinates)
    stores = [
        {"name": "Store A", "lat": 40.7128, "lon": -74.0060},   # New York City
        {"name": "Store B", "lat": 34.0522, "lon": -118.2437},  # Los Angeles
        {"name": "Store C", "lat": 41.8781, "lon": -87.6298},   # Chicago
        {"name": "Store D", "lat": 29.7604, "lon": -95.3698},   # Houston
        {"name": "Store E", "lat": 33.4484, "lon": -112.0740}   # Phoenix
    ]
    
    # User input: City name
    city = st.text_input("Enter your city:", value="New York")
    
    # Button to trigger the search
    if st.button("Find Nearest Store", key="find_nearest_store_by_city"):
        if not city:
            st.error("Please enter a city name.")
        else:
            user_location = geocode_city(city)
            if user_location is None:
                st.error("Could not geocode the specified city. Please try a different name.")
            else:
                st.success(f"Your location: Latitude {user_location[0]:.6f}, Longitude {user_location[1]:.6f}")
                nearest_store, distance = find_nearest_store(user_location, stores)
                if nearest_store:
                    st.success(f"Nearest store is **{nearest_store['name']}** at a distance of **{distance:.2f} km**.")
                else:
                    st.error("No stores available to determine the nearest location.")
                
                # --------------------------
                # Map Visualization using PyDeck
                # --------------------------
                # Prepare data for mapping: add candidate stores and the user's location.
                store_data = []
                for store in stores:
                    # Color the nearest store red; others blue.
                    color = [255, 0, 0] if store["name"] == nearest_store["name"] else [0, 0, 255]
                    store_data.append({
                        "name": store["name"],
                        "lat": store["lat"],
                        "lon": store["lon"],
                        "color": color
                    })
                # Add the user's location with a distinct color (green).
                store_data.append({
                    "name": "Your Location",
                    "lat": user_location[0],
                    "lon": user_location[1],
                    "color": [0, 255, 0]
                })
                
                df_locations = pd.DataFrame(store_data)
                
                layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=df_locations,
                    get_position='[lon, lat]',
                    get_color="color",
                    get_radius=20000,  # Adjust the radius as needed (in meters)
                    pickable=True
                )
                
                # Center the view at the user's location.
                view_state = pdk.ViewState(latitude=user_location[0], longitude=user_location[1], zoom=5, pitch=0)
                tooltip = {"html": "<b>{name}</b>", "style": {"color": "white"}}
                
                deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
                st.pydeck_chart(deck)

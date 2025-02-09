# modules/store_locator.py
import streamlit as st
import pandas as pd
import math
import pydeck as pdk

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
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
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
        nearest_store (dict): The store dictionary of the nearest store.
        min_distance (float): Distance (in kilometers) to the nearest store.
    """
    min_distance = float('inf')
    nearest_store = None
    for store in stores:
        distance = haversine_distance(user_location[0], user_location[1], store["lat"], store["lon"])
        if distance < min_distance:
            min_distance = distance
            nearest_store = store
    return nearest_store, min_distance

def app():
    st.title("Nearest Store Finder")
    st.write("Find the nearest store based on your current location.")

    # --------------------------
    # Pre-defined store locations
    # --------------------------
    # You can update these coordinates with real store data.
    stores = [
        {"name": "Store A", "lat": 40.7128, "lon": -74.0060},   # New York City
        {"name": "Store B", "lat": 34.0522, "lon": -118.2437},  # Los Angeles
        {"name": "Store C", "lat": 41.8781, "lon": -87.6298},   # Chicago
        {"name": "Store D", "lat": 29.7604, "lon": -95.3698},   # Houston
        {"name": "Store E", "lat": 33.4484, "lon": -112.0740}   # Phoenix
    ]
    
    # --------------------------
    # User Input: Current Location
    # --------------------------
    st.header("Your Current Location")
    user_lat = st.number_input("Enter your latitude:", format="%.6f", value=39.0)
    user_lon = st.number_input("Enter your longitude:", format="%.6f", value=-98.0)
    user_location = (user_lat, user_lon)
    
    if st.button("Find Nearest Store"):
        nearest_store, distance = find_nearest_store(user_location, stores)
        if nearest_store:
            st.success(f"Nearest store is **{nearest_store['name']}** at a distance of **{distance:.2f} km**.")
        else:
            st.error("No stores available to determine the nearest location.")

        # --------------------------
        # Map Visualization using PyDeck
        # --------------------------
        # Prepare a DataFrame for all locations (stores and user)
        # Mark store type and set colors:
        #   - Nearest store: Red
        #   - Other stores: Blue
        #   - User location: Green
        store_data = []
        for store in stores:
            store_data.append({
                "name": store["name"],
                "lat": store["lat"],
                "lon": store["lon"],
                "type": "Store",
                "color": [255, 0, 0] if store["name"] == nearest_store["name"] else [0, 0, 255]
            })
        # Add user location
        store_data.append({
            "name": "Your Location",
            "lat": user_lat,
            "lon": user_lon,
            "type": "User",
            "color": [0, 255, 0]
        })
        df_locations = pd.DataFrame(store_data)
        
        # Define the PyDeck layer for displaying points.
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_locations,
            get_position='[lon, lat]',
            get_color="color",
            get_radius=20000,  # Radius in meters; adjust as needed.
            pickable=True
        )
        
        # Center the view roughly at the user's location.
        view_state = pdk.ViewState(latitude=user_lat, longitude=user_lon, zoom=4, pitch=0)
        
        # Define a tooltip to display store names.
        tooltip = {"html": "<b>{name}</b>", "style": {"color": "white"}}
        
        # Create and display the map.
        deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
        st.pydeck_chart(deck)

# For testing this module directly, uncomment the following lines:
# if __name__ == "__main__":
#     app()

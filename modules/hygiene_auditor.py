import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def geocode_city(city_name):
    try:
        geolocator = Nominatim(user_agent="camp_hygiene_app")
        location = geolocator.geocode(city_name, timeout=10)
        return (location.latitude, location.longitude) if location else None
    except GeocoderTimedOut:
        return None

def compute_sanitation_score(refugees, workers, equipment, washrooms, bathrooms, kits):
    if refugees <= 0:
        return 0
    return sum([
        min((50 * workers) / refugees, 1),
        min((20 * equipment) / refugees, 1),
        min((25 * (washrooms + bathrooms)) / refugees, 1),
        1 if kits > 0 else 0
    ]) * 25

def compute_overall_hygiene(water, electricity, food, stay, sanitation):
    return (water + electricity + food + stay + sanitation) / 5.0

def assess_hygiene_compliance(city, refugees, water, electricity, food, stay, workers, equipment, washrooms, bathrooms, kits):
    location = geocode_city(city)
    if not location:
        return None, None, "Could not geocode the specified city."
    sanitation_score = compute_sanitation_score(refugees, workers, equipment, washrooms, bathrooms, kits)
    overall_score = compute_overall_hygiene(water, electricity, food, stay, sanitation_score)
    compliance = "High compliance" if overall_score >= 80 else "Moderate compliance" if overall_score >= 50 else "Low compliance"
    return location, overall_score, compliance

def app():
    st.title("Refugee Camp Hygiene Compliance Auditor")
    city = st.text_input("Enter the city or camp location:", "New York")
    loc = geocode_city(city)
    if loc:
        st.write(f"Geocoded Location: Latitude {loc[0]:.6f}, Longitude {loc[1]:.6f}")
    else:
        st.error("Could not geocode the provided city.")
    
    refugees = st.number_input("Number of Refugees", 1, value=1000)
    water, electricity, food, stay = [st.slider(label, 0, 100, default) for label, default in zip(
        ["Water Availability", "Electricity Availability", "Food Supply Adequacy", "Stay Facilities Adequacy"],
        [80, 70, 75, 65]
    )]
    workers = st.number_input("Number of Sanitation Workers", 0, value=20)
    equipment = st.number_input("Number of Sanitation Equipment", 0, value=50)
    washrooms = st.number_input("Number of Washrooms", 0, value=10)
    bathrooms = st.number_input("Number of Bathrooms", 0, value=10)
    kits = st.number_input("Number of Medicine Kits", 0, value=10)
    
    if st.button("Assess Camp Hygiene Compliance"):
        location, overall_score, compliance = assess_hygiene_compliance(city, refugees, water, electricity, food, stay, workers, equipment, washrooms, bathrooms, kits)
        if location:
            st.write(f"**Overall Hygiene Score:** {overall_score:.2f} / 100")
            st.write(compliance)
        else:
            st.error(compliance)

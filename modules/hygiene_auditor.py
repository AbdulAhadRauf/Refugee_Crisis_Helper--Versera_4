import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# -----------------------------
# Geocoding Function
# -----------------------------
def geocode_city(city_name):
    """
    Convert a city name into latitude and longitude using Nominatim.
    
    Parameters:
        city_name (str): The name of the city.
    
    Returns:
        (lat, lon) tuple if successful; otherwise, None.
    """
    try:
        geolocator = Nominatim(user_agent="camp_hygiene_app")
        location = geolocator.geocode(city_name, timeout=10)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except GeocoderTimedOut:
        return None

# -----------------------------
# Sanitation Component Calculation
# -----------------------------
def compute_sanitation_score(refugees, sanitation_workers, sanitation_equipment, washrooms, bathrooms, medicine_kits):
    """
    Compute a sanitation score (0-100) based on available sanitation and health facilities.
    
    Guidelines:
    - Ideal: At least 1 sanitation worker per 50 refugees.
    - Ideal: At least 1 equipment per 20 refugees.
    - Ideal: At least 1 facility (washroom+bathroom) per 25 refugees.
    - If at least one medicine kit is available, get full score for that component.
    
    The score is computed by first normalizing each component (capped at 1) and then
    multiplying by 25 to yield a score out of 100.
    
    Returns:
        sanitation_score (float): Score between 0 and 100.
    """
    if refugees <= 0:
        return 0
    worker_score = min((50 * sanitation_workers) / refugees, 1)
    equipment_score = min((20 * sanitation_equipment) / refugees, 1)
    facility_score = min((25 * (washrooms + bathrooms)) / refugees, 1)
    medicine_score = 1 if medicine_kits > 0 else 0
    sanitation_score = (worker_score + equipment_score + facility_score + medicine_score) * 25
    return sanitation_score

# -----------------------------
# Overall Hygiene Calculation
# -----------------------------
def compute_overall_hygiene(water, electricity, food, stay, sanitation):
    """
    Compute an overall hygiene score (0-100) as the average of:
      - Water availability (0-100)
      - Electricity availability (0-100)
      - Food supply adequacy (0-100)
      - Stay facilities adequacy (0-100)
      - Sanitation score (0-100)
    """
    overall = (water + electricity + food + stay + sanitation) / 5.0
    return overall

# -----------------------------
# Hygiene Compliance Assessment
# -----------------------------
def assess_hygiene_compliance(city, refugees, water, electricity, food, stay,
                              sanitation_workers, sanitation_equipment, washrooms, bathrooms, medicine_kits):
    """
    Assess hygiene compliance of a refugee camp based on geolocation and various facility statistics.
    
    Parameters:
        city (str): The camp's city name.
        refugees (int): Number of refugees.
        water (int): Water availability score (0-100).
        electricity (int): Electricity availability score (0-100).
        food (int): Food supply adequacy score (0-100).
        stay (int): Stay facilities (shelter/accommodation) adequacy score (0-100).
        sanitation_workers (int): Number of sanitation workers.
        sanitation_equipment (int): Number of sanitation equipment pieces.
        washrooms (int): Number of washrooms.
        bathrooms (int): Number of bathrooms.
        medicine_kits (int): Number of medicine kits.
    
    Returns:
        location (tuple): (latitude, longitude) of the camp if geocoding is successful.
        overall_score (float): Overall hygiene score (0-100).
        compliance (str): Text classification of hygiene compliance.
    """
    # Geocode the city to obtain camp location.
    location = geocode_city(city)
    if location is None:
        return None, None, "Could not geocode the specified city."
    
    # Compute sanitation score.
    sanitation_score = compute_sanitation_score(refugees, sanitation_workers, sanitation_equipment, washrooms, bathrooms, medicine_kits)
    
    # Compute overall hygiene score as the average of five components.
    overall_score = compute_overall_hygiene(water, electricity, food, stay, sanitation_score)
    
    # Classify the hygiene compliance.
    if overall_score >= 80:
        compliance = "High compliance with hygiene standards."
    elif overall_score >= 50:
        compliance = "Moderate compliance. Improvements are needed."
    else:
        compliance = "Low compliance. Immediate action is required."
    
    return location, overall_score, compliance

# -----------------------------
# Streamlit App Interface
# -----------------------------
def app():
    st.title("Refugee Camp Hygiene Compliance Auditor")
    st.write("Assess the hygiene compliance of a refugee camp based on its geolocation and facility statistics.")
    
    st.header("Camp Geolocation")
    city = st.text_input("Enter the city or camp location:", value="New York")
    
    if city:
        loc = geocode_city(city)
        if loc:
            st.write(f"Geocoded Location: Latitude {loc[0]:.6f}, Longitude {loc[1]:.6f}")
        else:
            st.error("Could not geocode the provided city. Please check the city name.")
    
    st.header("Camp Statistics")
    refugees = st.number_input("Number of Refugees", min_value=1, value=1000, step=1)
    
    st.subheader("Basic Facilities (Rate from 0 to 100)")
    water = st.slider("Water Availability", 0, 100, 80)
    electricity = st.slider("Electricity Availability", 0, 100, 70)
    food = st.slider("Food Supply Adequacy", 0, 100, 75)
    stay = st.slider("Stay Facilities (Shelter/Accommodation) Adequacy", 0, 100, 65)
    
    st.subheader("Sanitation & Health Facilities")
    sanitation_workers = st.number_input("Number of Sanitation Workers", min_value=0, value=20, step=1)
    sanitation_equipment = st.number_input("Number of Sanitation Equipment", min_value=0, value=50, step=1)
    washrooms = st.number_input("Number of Washrooms", min_value=0, value=10, step=1)
    bathrooms = st.number_input("Number of Bathrooms", min_value=0, value=10, step=1)
    medicine_kits = st.number_input("Number of Medicine Kits", min_value=0, value=10, step=1)
    
    if st.button("Assess Camp Hygiene Compliance"):
        location, overall_score, compliance = assess_hygiene_compliance(
            city, refugees, water, electricity, food, stay,
            sanitation_workers, sanitation_equipment, washrooms, bathrooms, medicine_kits
        )
        if location is None:
            st.error(compliance)  # If geocoding fails, 'compliance' holds the error message.
        else:
            st.write("### Hygiene Compliance Assessment Result:")
            st.write(f"**Overall Hygiene Score:** {overall_score:.2f} / 100")
            st.write(compliance)

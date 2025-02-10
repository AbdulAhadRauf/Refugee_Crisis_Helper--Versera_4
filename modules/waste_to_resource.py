import streamlit as st
import cv2
import numpy as np
from PIL import Image

def classify_waste(image):
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    mean_val = np.mean(gray)
    return "organic" if mean_val < 100 else "metal" if mean_val < 150 else "plastic"

def fetch_recommendations(waste_type):
    recommendations = {
        "plastic": "Consider recycling plastic waste by cleaning and segregating it.",
        "organic": "Organic waste can be composted to produce nutrient-rich fertilizer.",
        "metal": "Metal waste is highly recyclable and can be processed to recover valuable materials."
    }
    return recommendations.get(waste_type, "No recommendations available for this type of waste.")

def app():
    st.title("Waste-to-Resource AI Platform")
    st.write("Upload an image of your waste to get recommendations on how to convert it into useful resources.")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        waste_type = classify_waste(image)
        st.write(f"**Detected Waste Type:** {waste_type.capitalize()}")
        st.write("### Recommendations:")
        st.write(fetch_recommendations(waste_type))

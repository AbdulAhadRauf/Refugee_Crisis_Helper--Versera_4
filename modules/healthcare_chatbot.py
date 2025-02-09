import streamlit as st
from googletrans import Translator

def get_medical_advice(symptoms):
    """
    Simulate symptom analysis and provide medical recommendations.
    In a production system, this function would leverage an ML model or an external API.
    """
    if "fever" in symptoms.lower():
        return ("It appears you may have a fever. Please rest, stay hydrated, "
                "and monitor your temperature. Consult a healthcare professional if it persists.")
    elif "cough" in symptoms.lower():
        return ("A cough can be a symptom of various conditions. Monitor for additional symptoms "
                "such as fever or difficulty breathing, and consider consulting a healthcare provider.")
    else:
        return "For the symptoms described, please consult with a healthcare provider for a proper diagnosis."
    
def app():
    st.title("Multilingual Healthcare Chatbot")
    st.write("Get healthcare advice in your preferred language.")
    
    language = st.selectbox("Select Language", options=["en", "hi", "es", "fr", "de", "zh-cn"], index=0)
    translator = Translator()
    
    user_symptoms = st.text_area("Enter your symptoms:")
    
    if st.button("Get Advice"):
        if user_symptoms:
            advice = get_medical_advice(user_symptoms)
            # Translate the advice to the selected language.
            translation = translator.translate(advice, dest=language)
            st.write(f"**Medical Advice ({language}):**")
            st.write(translation.text)
        else:
            st.error("Please enter your symptoms to get advice.")





#  ####< if we were to afford an AI API >
#  ### or deploy it in our pc itself
# import os
# import streamlit as st
# from googletrans import Translator
# import requests
# # from dotenv import load_dotenv

# # # Load environment variables from the .env file
# # load_dotenv()

# # Retrieve sensitive information from environment variables
# PERPLEXITY_API_URL = os.getenv("PERPLEXITY_API_URL")
# PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# def get_medical_advice_perplexity(symptoms):
#     """
#     Use Perplexity AI API to generate medical advice based on the provided symptoms.
#     """
#     prompt = (
#         f"Provide detailed and empathetic medical advice for the following symptoms: {symptoms}. "
#         "Include care recommendations and any necessary warnings."
#     )
    
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {PERPLEXITY_API_KEY}"
#     }
    
#     payload = {
#         "prompt": prompt,
#         "max_tokens": 150,
#         "temperature": 0.7,
#     }
    
#     try:
#         response = requests.post(PERPLEXITY_API_URL, json=payload, headers=headers)
#         response.raise_for_status()
#         result = response.json()
#         advice = result.get("text", "No advice returned from API.")
#         return advice
#     except Exception as e:
#         return f"Error contacting Perplexity AI: {e}"

# def app():
#     st.title("Multilingual Healthcare Chatbot")
#     st.write("Get healthcare advice in your preferred language using Perplexity AI.")
    
#     language = st.selectbox("Select Language", options=["en", "es", "fr", "de", "zh-cn"], index=0)
#     translator = Translator()
#     user_symptoms = st.text_area("Enter your symptoms:")
    
#     if st.button("Get Advice"):
#         if user_symptoms:
#             advice = get_medical_advice_perplexity(user_symptoms)
#             translation = translator.translate(advice, dest=language)
#             st.write(f"**Medical Advice ({language}):**")
#             st.write(translation.text)
#         else:
#             st.error("Please enter your symptoms to get advice.")


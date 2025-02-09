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

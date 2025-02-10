import os
import streamlit as st
import google.generativeai as genai
from googletrans import Translator
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(model_name="gemini-2.0-flash", generation_config=generation_config)

def get_medical_advice_ai(symptoms):
    prompt = (
        f"You are a helpful and empathetic healthcare assistant. "
        f"The user has reported the following symptoms: {symptoms}\n\n"
        "Provide short-medium, empathetic, and medically cautious advice. "
        "Include a disclaimer that the advice is not a substitute for professional medical consultation."
    )
    response = model.start_chat(history=[]).send_message(prompt)
    return response.text

def app():
    st.title("Multilingual AI Healthcare Chatbot")
    st.write("Enter your symptoms to receive AI-generated healthcare advice in your preferred language.")
    
    language_options = {
        "English": "en", "Hindi": "hi", "Spanish": "es", "French": "fr", "German": "de", "Chinese (Simplified)": "zh-cn"
    }
    
    selected_language_full = st.selectbox("Select Target Language", list(language_options.keys()), index=0)
    target_language = language_options[selected_language_full]
    user_symptoms = st.text_area("Enter your symptoms:")
    
    if st.button("Get Advice") and user_symptoms:
        advice = get_medical_advice_ai(user_symptoms)
        if advice.strip():
            if selected_language_full != "English":
            
                try:
                    translation = Translator().translate(advice, dest=target_language).text
                    if translation.strip():
                        st.write(f"**Medical Advice ({selected_language_full}):**")
                        st.write(translation)
                except Exception:
                    st.error("Error translating the advice.")
            else:
                st.write("**Raw AI Medical Advice:**")
                st.write(advice)
                
        else:
            st.error("No advice returned. Please try again.")

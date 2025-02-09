import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import google.generativeai as genai
from googletrans import Translator

# Configure the Gemini API using the environment variable GEMINI_API_KEY.
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Set up generation configuration parameters.
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the Gemini model instance.
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

def get_medical_advice_ai(symptoms):
    """
    Generate healthcare advice based on the user's symptoms using the Gemini API.
    
    Parameters:
        symptoms (str): The description of the user's symptoms.
        
    Returns:
        advice (str): AI-generated healthcare advice.
    """
    # Construct the prompt for the Gemini API.
    prompt = (
        f"You are a helpful and empathetic healthcare assistant. "
        f"The user has reported the following symptoms: {symptoms}\n\n"
        "Provide detailed, empathetic, and medically cautious advice. "
        "Include a disclaimer that the advice is not a substitute for professional medical consultation."
    )
    
    # Start a new chat session (with an empty history) and send the prompt.
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    
    # Retrieve the advice text from the response.
    advice = response.text
    return advice

def app():
    st.title("Multilingual AI Healthcare Chatbot")
    st.write(
        "Enter your symptoms to receive AI-generated healthcare advice in your preferred language.\n\n"
        "Please note that this advice is for demonstration purposes only and should not replace professional medical consultation."
    )
    
    # Define a dictionary mapping full language names to language codes.
    language_options = {
        "English": "en",
        "Hindi": "hi",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Chinese (Simplified)": "zh-cn"
    }
    
    # Let the user select a language by its full name.
    selected_language_full = st.selectbox("Select Target Language", options=list(language_options.keys()), index=0)
    target_language = language_options[selected_language_full]
    
    # Get the user's symptom description.
    user_symptoms = st.text_area("Enter your symptoms:")
    
    if st.button("Get Advice", key="get_advice_button"):
        if user_symptoms:
            # Generate advice using the Gemini API.
            advice = get_medical_advice_ai(user_symptoms)
            if advice is None or advice.strip() == "":
                st.error("No advice was returned from the Gemini API. Please try again later.")
            else:
                st.write("**Raw AI Medical Advice:**")
                st.write(advice)
                
                # Translate the advice into the selected language.
                translator = Translator()
                try:
                    translation = translator.translate(advice, dest=target_language)
                    # Ensure that a valid translation was returned.
                    if translation.text is None or translation.text.strip() == "":
                        st.error("Translation returned no text. Please try again.")
                    else:
                        st.write(f"**Medical Advice ({selected_language_full}):**")
                        st.write(translation.text)
                except Exception as e:
                    pass
                    # st.error("Error translating the advice: " + str(e))
        else:
            st.error("Please enter your symptoms to get advice.")

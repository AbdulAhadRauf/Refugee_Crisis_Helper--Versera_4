import streamlit as st
from googletrans import Translator
from gtts import gTTS
import io
import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai


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

def get_cultural_insights(country):
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
        f"The user wants to know some cultural traditions about {country}\n\n"
        "Provide short, empathetic, and ethiclaly cautious cultural information . "
    )
    
    # Start a new chat session (with an empty history) and send the prompt.
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    
    # Retrieve the advice text from the response.
    cultural_advice = response.text
    try:
        return cultural_advice
    except:
        return "Cultural insights for this region are not available. Please try another country."





def translate_text(text, dest_language):
    return Translator().translate(text, dest=dest_language).text

def text_to_speech(text, lang='en'):
    audio_bytes = io.BytesIO()
    gTTS(text=text, lang=lang).write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

def app():
    st.title("AI-Powered Cultural Integration Hub")
    st.write("Gain cultural insights, etiquette tips, and translation services to enhance cross-cultural understanding.")
    
    st.header("Cultural Insights")
    country = st.text_input("Enter a country for cultural insights:", value="USA")
    if st.button("Get Cultural Insights"):
        insights = get_cultural_insights(country)
        st.write("### Cultural Insights:")
        st.write(insights)
        if st.checkbox("Listen to Cultural Insights"):
            st.audio(text_to_speech(insights, lang='en'), format='audio/mp3')
    
    st.header("Translation Service")
    text_to_translate = st.text_area("Enter text to translate:")
    target_language = st.selectbox("Select target language", ["en", "hi", "es", "fr", "de", "zh-cn"], index=0)
    output_format = st.radio("Select output format", ["Text", "Speech", "Both"], index=0)
    
    if st.button("Translate Text") and text_to_translate:
        translated = translate_text(text_to_translate, target_language)
        if output_format in ["Text", "Both"]:
            st.write(f"### Translated Text ({target_language}):")
            st.write(translated)
        if output_format in ["Speech", "Both"]:
            st.audio(text_to_speech(translated, lang=target_language), format='audio/mp3')

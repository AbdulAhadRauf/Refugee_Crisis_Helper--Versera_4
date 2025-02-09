# modules/cultural_integration.py
import streamlit as st
from googletrans import Translator
from gtts import gTTS
import io

def get_cultural_insights(country):
    """
    Provide cultural insights and etiquette tips for the specified country.
    In a production system, this data might be fetched from a dedicated database or API.
    """
    insights = {
        "France": "In France, greetings often involve a handshake or a light kiss on the cheek. Politeness and formality are valued.",
        "Japan": "In Japan, bowing is customary. Removing shoes before entering a home or certain establishments is standard practice.",
        "India": "In India, using your right hand for eating or handing over items is considered polite. Respect for cultural diversity is key.",
        "USA": "In the USA, a firm handshake and direct eye contact are common in professional settings. Casual interactions are often informal."
    }
    return insights.get(country, "Cultural insights for this region are not available. Please try another country.")

def translate_text(text, dest_language):
    """
    Translate text to the destination language using the Google Translate API.
    """
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text

def text_to_speech(text, lang='en'):
    """
    Convert the given text to speech using gTTS and return the audio as bytes.
    
    Parameters:
        text (str): The text to be converted into speech.
        lang (str): The language code (e.g., 'en', 'es'). Default is English.
    
    Returns:
        BytesIO: An in-memory bytes buffer containing the audio data in MP3 format.
    """
    tts = gTTS(text=text, lang=lang)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

def app():
    st.title("AI-Powered Cultural Integration Hub")
    st.write("Gain cultural insights, etiquette tips, and translation services to enhance cross-cultural understanding.")
    
    # ---------------- Cultural Insights Section ---------------- #
    st.header("Cultural Insights")
    country = st.text_input("Enter a country for cultural insights (e.g., France, Japan, India, USA):", value="USA")
    if st.button("Get Cultural Insights"):
        insights = get_cultural_insights(country)
        st.write("### Cultural Insights:")
        st.write(insights)
        
        # Option to output speech for cultural insights.
        if st.checkbox("Listen to Cultural Insights"):
            # Convert insights to speech (using English as default).
            audio_bytes = text_to_speech(insights, lang='en')
            st.audio(audio_bytes, format='audio/mp3')
    
    # ---------------- Translation Service Section ---------------- #
    st.header("Translation Service")
    text_to_translate = st.text_area("Enter text to translate:")
    target_language = st.selectbox("Select target language", options=["en","hi", "es", "fr", "de", "zh-cn"], index=0)
    output_format = st.radio("Select output format", options=["Text", "Speech", "Both"], index=0)
    
    if st.button("Translate Text"):
        if text_to_translate:
            # Translate the text.
            translated = translate_text(text_to_translate, target_language)
            
            # Display text output if required.
            if output_format in ["Text", "Both"]:
                st.write(f"### Translated Text ({target_language}):")
                st.write(translated)
            
            # Generate and play audio if required.
            if output_format in ["Speech", "Both"]:
                # Note: The gTTS language codes may differ slightly from Google Translate.
                audio_bytes = text_to_speech(translated, lang=target_language)
                st.audio(audio_bytes, format='audio/mp3')
        else:
            st.error("Please enter text to translate.")

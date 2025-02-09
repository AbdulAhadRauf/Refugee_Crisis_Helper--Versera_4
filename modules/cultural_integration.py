import streamlit as st
from googletrans import Translator

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

def app():
    st.title("AI-Powered Cultural Integration Hub")
    st.write("Gain cultural insights, etiquette tips, and translation services to enhance cross-cultural understanding.")
    
    # Cultural Insights Section
    st.header("Cultural Insights")
    country = st.text_input("Enter a country for cultural insights (e.g., France, Japan, India, USA):", value="USA")
    if st.button("Get Cultural Insights"):
        insights = get_cultural_insights(country)
        st.write("### Cultural Insights:")
        st.write(insights)
    
    # Translation Service Section
    st.header("Translation Service")
    text_to_translate = st.text_area("Enter text to translate:")
    target_language = st.selectbox("Select target language", options=["en", "hi", "es", "fr", "de", "zh-cn"], index=0)
    if st.button("Translate Text"):
        if text_to_translate:
            translated = translate_text(text_to_translate, target_language)
            st.write(f"### Translated Text ({target_language}):")
            st.write(translated)
        else:
            st.error("Please enter text to translate.")

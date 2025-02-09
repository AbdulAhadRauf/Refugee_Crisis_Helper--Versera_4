# app.py
import streamlit as st
from modules import food_optimizer, healthcare_chatbot, waste_to_resource, cultural_integration, hygiene_auditor

def main():
    st.sidebar.title("Refugee Campaign AI Platform")
    module_choice = st.sidebar.selectbox(
        "Choose a Module",
        [
            "AI-Driven Food Distribution Optimizer",
            "Multilingual Healthcare Chatbot",
            "Waste-to-Resource AI Platform",
            "AI-Powered Cultural Integration Hub",
            "Hygiene Compliance Auditor"
        ]
    )
    
    if module_choice == "AI-Driven Food Distribution Optimizer":
         food_optimizer.app()
    elif module_choice == "Multilingual Healthcare Chatbot":
         healthcare_chatbot.app()
    elif module_choice == "Waste-to-Resource AI Platform":
         waste_to_resource.app()
    elif module_choice == "AI-Powered Cultural Integration Hub":
         cultural_integration.app()
    elif module_choice == "Hygiene Compliance Auditor":
         hygiene_auditor.app()

if __name__ == "__main__":
    main()

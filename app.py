# app.py
import streamlit as st
from modules import auth, food_optimizer, healthcare_chatbot, waste_to_resource, cultural_integration, hygiene_auditor, store_locator

def main():
    # Initialize the database (creates tables if not present)
    auth.init_db()
    
    # Check for user authentication. If not logged in, show login/register form.
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        auth.login()
        return  # Do not load the rest of the app until the user is logged in.

    # Once authenticated, show the main application
    st.sidebar.title("Refugee Campaign AI Platform")
    module_choice = st.sidebar.selectbox(
        "Choose a Module",
        [
            "Multilingual Healthcare Chatbot",
            "Waste-to-Resource AI Platform",
            "AI-Powered Cultural Integration Hub",
            "AI-Driven Food Distribution Optimizer",
            "Hygiene Compliance Auditor",
            "Store Locator"
        ]
    )
    
    # Display logged-in user information in the sidebar.
    st.sidebar.write(f"Logged in as: {st.session_state.get('username', 'Unknown')}")

    # Load the appropriate module based on the user's selection.
    if module_choice == "Multilingual Healthcare Chatbot":
         healthcare_chatbot.app()
    elif module_choice == "Waste-to-Resource AI Platform":
         waste_to_resource.app()
    elif module_choice == "AI-Driven Food Distribution Optimizer":
         food_optimizer.app()
    elif module_choice == "AI-Powered Cultural Integration Hub":
         cultural_integration.app()
    elif module_choice == "Hygiene Compliance Auditor":
         hygiene_auditor.app()
    elif module_choice == "Store Locaator":
         store_locator.app()

if __name__ == "__main__":
    main()

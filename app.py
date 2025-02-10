import streamlit as st
from modules import auth, food_optimizer, healthcare_chatbot, waste_to_resource, cultural_integration, hygiene_auditor, store_locator

def main():
    auth.init_db()
    
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        auth.login()
        return

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
    
    st.sidebar.write(f"Logged in as: {st.session_state.get('username', 'Unknown')}")
    
    module_mapping = {
        "Multilingual Healthcare Chatbot": healthcare_chatbot.app,
        "Waste-to-Resource AI Platform": waste_to_resource.app,
        "AI-Driven Food Distribution Optimizer": food_optimizer.app,
        "AI-Powered Cultural Integration Hub": cultural_integration.app,
        "Hygiene Compliance Auditor": hygiene_auditor.app,
        "Store Locator": store_locator.app
    }
    
    module_mapping.get(module_choice, lambda: None)()

if __name__ == "__main__":
    main()

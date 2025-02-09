import streamlit as st

def assess_hygiene_compliance(data):
    """
    Simulate hygiene compliance assessment.
    In a real system, this might involve processing sensor data or image analysis.
    """
    try:
        score = float(data)
    except ValueError:
        return "Invalid input. Please enter a numeric score between 0 and 100."
    
    if score >= 80:
        return "High compliance with hygiene standards."
    elif score >= 50:
        return "Moderate compliance. Improvements are needed."
    else:
        return "Low compliance. Immediate action is required."
    
def app():
    st.title("Hygiene Compliance Auditor")
    st.write("Assess hygiene compliance based on input data.")
    
    data = st.text_input("Enter hygiene compliance score (0-100):", value="75")
    
    if st.button("Assess Compliance"):
        result = assess_hygiene_compliance(data)
        st.write("### Assessment Result:")
        st.write(result)

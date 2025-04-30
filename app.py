import streamlit as st
import pandas as pd

st.title("PredictFlow.ai")
st.write("Upload equipment sensor data (CSV with timestamp, temperature, vibration, pressure)")

uploaded_file = st.file_uploader("Choose CSV file")
if uploaded_file:
    try:
        data = pd.read_csv(uploaded_file)
        st.success("File loaded successfully!")
        st.write("First 5 rows:", data.head())
        
        # Simple mock analysis
        if "temperature" in data.columns:
            risk = "HIGH" if data["temperature"].mean() > 90 else "LOW"
            st.warning(f"⚠️ Predicted failure risk: {risk}")
        else:
            st.info("ℹ️ Add 'temperature' column for better predictions")
            
    except Exception as e:
        st.error(f"Error: {str(e)}. Please check your CSV format.")

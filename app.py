import streamlit as st
import pandas as pd

st.title("PredictFlow.ai (Demo)")
uploaded_file = st.file_uploader("Upload equipment data (CSV)")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.success(f"Analyzed {len(data)} records!")
    st.write("⚠️ Mock prediction: Pump #3 has 87% failure risk")

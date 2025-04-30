import streamlit as st
import pandas as pd
import requests

st.title("PredictFlow.ai LIVE")
st.write("""
Upload equipment sensor data (CSV with timestamp + at least one of:
temperature, vibration, pressure, current)
""")

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/jbrownlee/Dummy-Predictive-Maintenance"
headers = {"Authorization": "Bearer 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"}  # ← Paste your token here

def predict(data):
    response = requests.post(API_URL, headers=headers, json={"inputs": data.to_dict()})
    return response.json()

uploaded_file = st.file_uploader("Choose CSV")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.success(f"Analyzing {len(data)} records...")
    
    # Get AI predictions
    predictions = predict(data.head())  # Analyze first 5 rows
    st.warning(f"🔴 Critical alerts: {len(predictions['failures'])}")
    st.write(predictions)

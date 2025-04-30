import streamlit as st
import pandas as pd
import requests
import time

st.title("PredictFlow.ai LIVE")
st.write("Upload equipment sensor data (CSV)")

# Hugging Face Setup (replace with your token)
API_URL = "https://api-inference.huggingface.co/models/jbrownlee/Dummy-Predictive-Maintenance"
headers = {"Authorization": "Bearer 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"}  # ← Replace!

def safe_predict(data):
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": data.to_dict()})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

uploaded_file = st.file_uploader("Choose CSV")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.success(f"Analyzing {len(data)} records...")
    
    # Show loading spinner
    with st.spinner("AI is analyzing..."):
        predictions = safe_predict(data.head())  # Test first 5 rows
        
    if "failures" in predictions:
        st.warning(f"🔴 Critical alerts: {len(predictions['failures']}")  # Added closing )
        st.json(predictions)
    elif "error" in predictions:
        st.error(predictions["error"])
    else:
        st.info("⚠️ Unexpected response format. Showing raw output:")
        st.write(predictions)

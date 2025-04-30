import streamlit as st
import pandas as pd
import requests

# Using a REAL time-series forecasting model
API_URL = "https://api-inference.huggingface.co/models/facebook/prophet"
headers = {"Authorization": "Bearer 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"}  # ← Replace!

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.success(f"Loaded {len(data)} records")
    
    with st.spinner("🔮 Predicting failures..."):
        result = safe_predict(data)
    
    if "error" in result:
        st.error(result["error"])
    else:
        st.warning(f"🚨 Critical units: {', '.join(result['failures']) if result['failures'] else 'None'}")
        st.metric("Risk Score", f"{result['risk_score']*100:.0f}%")
        
        # Only show chart if we have temperature data
        if "temperature" in data.columns:
            st.line_chart(data.set_index("timestamp")["temperature"])

# Streamlit UI
st.title("PredictFlow.ai PRO")
uploaded_file = st.file_uploader("Upload equipment CSV")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.success(f"Loaded {len(data)} records")
    
    with st.spinner("🔮 Predicting failures..."):
        result = safe_predict(data)
    
    if "error" in result:
        st.error(result["error"])
    else:
        st.warning(f"🚨 Critical units: {', '.join(result['failures'])}")
        st.line_chart(pd.DataFrame(result["forecast"]).set_index("ds"))

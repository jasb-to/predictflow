import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ======================
# APP CONFIGURATION
# ======================
st.set_page_config(page_title="PredictFlow.ai", layout="wide")
st.title("🔧 PredictFlow.ai - Predictive Maintenance")
st.write("Upload equipment sensor data (CSV format)")

# ======================
# PREDICTION ENGINE
# ======================
def safe_predict(data):
    """Local mock predictions (fallback)"""
    failures = []
    
    # Temperature checks (threshold: 90°C)
    if "temperature" in data.columns:
        hot_units = data[data["temperature"] > 90].index.tolist()
        failures.extend([f"pump_{i+1}" for i in hot_units])
    
    # Vibration checks (threshold: 5.0)
    if "vibration" in data.columns:
        vibrating_units = data[data["vibration"] > 5.0].index.tolist()
        failures.extend([f"motor_{i+1}" for i in vibrating_units])
    
    risk_score = min(0.99, 
        (0.7 if len(failures) > 0 else 0.2) + 
        (0.3 * data.get("temperature", 85).mean() / 100)
    )
    
    return {
        "failures": failures,
        "risk_score": risk_score,
        "alert": "CRITICAL" if risk_score > 0.8 else "WATCH",
        "source": "Mock Data"
    }

def ai_predict(data):
    """Real AI prediction (replace URL with your model later)"""
    try:
        API_URL = "https://api-inference.huggingface.co/models/your-model-name"
        headers = {"Authorization": "Bearer YOUR_HF_TOKEN"}
        
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": data.to_dict()},
            timeout=10  # Prevents hanging
        )
        
        if response.status_code == 200:
            return {
                **response.json(),
                "source": "AI Model"
            }
        return safe_predict(data)  # Fallback if API fails
    
    except Exception as e:
        st.toast(f"⚠️ AI failed: {str(e)}")
        return safe_predict(data)  # Fallback to mock

# ======================
# USER INTERFACE
# ======================
uploaded_file = st.file_uploader(
    "Choose CSV file",
    type=["csv"],
    help="Requires columns: timestamp, temperature, vibration"
)

if uploaded_file:
    try:
        data = pd.read_csv(uploaded_file)
        
        # Auto-detect timestamp column
        time_col = next((col for col in data.columns if "time" in col.lower()), None)
        
        with st.spinner("🔮 Analyzing equipment health..."):
            result = ai_predict(data)  # Try AI first
            
        # Results Dashboard
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Risk Score", 
                     f"{result['risk_score']*100:.0f}%", 
                     result['alert'])
            
            if result['failures']:
                st.error(f"🚨 Critical units: {', '.join(result['failures'])}")
            else:
                st.success("✅ All units normal")
                
            st.caption(f"Source: {result.get('source', 'Unknown')}")

        with col2:
            if "temperature" in data.columns:
                st.subheader("Temperature Trend")
                if time_col:
                    st.line_chart(data.set_index(pd.to_datetime(data[time_col]))["temperature"])
                else:
                    st.line_chart(data["temperature"])
                
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Sample CSV format:")
        st.code("""timestamp,temperature,vibration\n2023-01-01,85,4.2\n2023-01-02,91,5.1""")

else:
    st.info("ℹ️ Please upload a CSV file to begin analysis")

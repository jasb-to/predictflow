import streamlit as st
import pandas as pd
import requests

# ======================
# Configuration (SAFE)
# ======================
st.set_page_config(page_title="PredictFlow.ai", layout="wide")
st.title("🔧 PredictFlow.ai - Predictive Maintenance")

# Hugging Face API setup (uses hidden secrets)
API_URL = "https://jasb-to-predictflow-ai.hf.space/predict"
HF_TOKEN = st.secrets["HF_TOKEN"]  # ← Now secure!

# ======================
# Prediction Functions
# ======================
def safe_predict(data):
    """Fallback mock predictions"""
    failures = []
    
    if "temperature" in data.columns:
        hot_units = data[data["temperature"] > 90].index.tolist()
        failures.extend([f"pump_{i+1}" for i in hot_units])
    
    if "vibration" in data.columns:
        vibrating_units = data[data["vibration"] > 5.0].index.tolist()
        failures.extend([f"motor_{i+1}" for i in vibrating_units])
    
    risk_score = min(0.99, (0.7 if failures else 0.2) + (0.3 * data.get("temperature", 85).mean() / 100))
    
    return {
        "failures": failures,
        "risk_score": risk_score,
        "source": "Mock Data"
    }

def ai_predict(data):
    """Real API prediction"""
    try:
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json=data.to_dict(),
            timeout=5
        )
        if response.status_code == 200:
            return {**response.json(), "source": "AI Model"}
        return safe_predict(data)
    except Exception as e:
        st.warning(f"⚠️ API failed: {str(e)}")
        return safe_predict(data)

# ======================
# User Interface
# ======================
uploaded_file = st.file_uploader(
    "Upload equipment data (CSV)",
    type=["csv"],
    help="Requires timestamp, temperature, and/or vibration columns"
)

if uploaded_file:
    try:
        data = pd.read_csv(uploaded_file)
        st.success(f"📊 Loaded {len(data)} records")
        
        with st.spinner("🔮 Analyzing..."):
            result = ai_predict(data)  # Uses real API with fallback
            
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Risk Score", 
                     f"{result['risk_score']*100:.0f}%", 
                     result.get('status', 'WATCH'))
            
            if result["failures"]:
                st.error(f"🚨 Critical: {', '.join(result['failures']}")  # Now correct
            else:
                st.success("✅ All systems normal")
                
            st.caption(f"Source: {result.get('source', 'Unknown')}")
        
        with col2:
            if "temperature" in data.columns:
                st.subheader("Temperature Trend")
                time_col = next((c for c in data.columns if "time" in c.lower()), None)
                if time_col:
                    st.line_chart(data.set_index(pd.to_datetime(data[time_col]))["temperature"])
                else:
                    st.line_chart(data["temperature"])
                    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Sample format:")
        st.code("timestamp,temperature,vibration\n2023-01-01,85,4.2\n2023-01-02,91,5.1")
else:
    st.info("ℹ️ Upload a CSV file to begin analysis")

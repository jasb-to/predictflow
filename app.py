import streamlit as st
import pandas as pd

st.title("PredictFlow.ai - Predictive Maintenance")
st.write("Upload equipment sensor data (CSV format)")

# File uploader widget (THIS DEFINES uploaded_file)
uploaded_file = st.file_uploader(
    "Choose CSV file",
    type=["csv"],
    help="Upload timestamped sensor data with temperature/vibration columns"
)

def safe_predict(data):
    """Local mock prediction engine"""
    failures = []
    
    # Temperature checks
    if "temperature" in data.columns:
        hot_units = data[data["temperature"] > 90].index.tolist()
        failures.extend([f"pump_{i+1}" for i in hot_units])
    
    # Vibration checks
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
        "alert": "CRITICAL" if risk_score > 0.8 else "WATCH"
    }

# Main execution flow
if uploaded_file is not None:  # Proper None check
    try:
        data = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(data)} records")
        
        with st.spinner("Analyzing equipment health..."):
            result = safe_predict(data)
        
        # Display results
        st.warning(f"🚨 Critical units: {', '.join(result['failures']) if result['failures'] else 'None'}")
        st.metric("System Risk Score", f"{result['risk_score']*100:.0f}%", result['alert'])
        
        # Visualize temperature if available
        if "temperature" in data.columns:
            st.subheader("Temperature Trend")
            st.line_chart(data.set_index(
                pd.to_datetime(data["timestamp"]) if "timestamp" in data.columns else data.index
            )["temperature"])
            
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
else:
    st.info("ℹ️ Please upload a CSV file to begin analysis")

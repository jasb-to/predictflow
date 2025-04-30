import streamlit as st
import pandas as pd
import io

st.title("PredictFlow.ai (Mac Optimized)")

uploaded_file = st.file_uploader("Upload equipment CSV")
if uploaded_file:
    try:
        # Handles Mac/Windows line endings
        data = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode('utf-8')))
        st.success(f"Analyzed {len(data)} records!")
        
        # Mock analysis
        if "temperature" in data.columns:
            risk = "HIGH" if data["temperature"].mean() > 90 else "LOW"
            st.warning(f"Predicted risk: {risk}")
        st.write(data.head())
        
    except Exception as e:
        st.error(f"Mac formatting issue? Try re-saving as UTF-8 CSV. Error: {str(e)}")

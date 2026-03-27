import streamlit as st
import requests
import json
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Predictive Maintenance",
    page_icon="🔧",
    layout="centered"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

.stApp {
    background-color: #0f1117;
    color: #e0e0e0;
}

h1, h2, h3 {
    font-family: 'IBM Plex Mono', monospace !important;
}

.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid #2a2a2a;
    margin-bottom: 2rem;
}

.hero h1 {
    font-size: 2rem;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin-bottom: 0.3rem;
}

.hero p {
    color: #888;
    font-size: 0.95rem;
    font-family: 'IBM Plex Mono', monospace;
}

.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.8rem;
}

.result-box {
    border-radius: 8px;
    padding: 1.5rem;
    margin-top: 1.5rem;
    text-align: center;
    font-family: 'IBM Plex Mono', monospace;
}

.result-healthy {
    background: #0d2b1e;
    border: 1px solid #1a5c38;
    color: #3ddc84;
}

.result-failure {
    background: #2b0d0d;
    border: 1px solid #5c1a1a;
    color: #ff6b6b;
}

.result-box h2 {
    font-size: 1.4rem;
    margin: 0 0 0.5rem;
}

.result-box p {
    font-size: 0.85rem;
    color: #aaa;
    margin: 0;
}

.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    padding: 0.2rem 0.6rem;
    border-radius: 3px;
    background: #1e1e2e;
    border: 1px solid #333;
    color: #888;
    margin-bottom: 1rem;
}

.stButton > button {
    width: 100%;
    background: #1a1a2e;
    color: #ffffff;
    border: 1px solid #333;
    border-radius: 6px;
    padding: 0.7rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.9rem;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: #ffffff;
    color: #0f1117;
    border-color: #ffffff;
}

div[data-testid="stNumberInput"] label {
    font-size: 0.8rem;
    color: #888;
    font-family: 'IBM Plex Mono', monospace;
}

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Config ────────────────────────────────────────────────────────────────────
API_URL = "https://su40h5dbj7.execute-api.ap-south-1.amazonaws.com/prod/predict"

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔧 Predictive Maintenance</h1>
    <p>AWS SageMaker · XGBoost · Real-time Inference</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="badge">↳ Enter sensor readings below to predict machine health</div>', unsafe_allow_html=True)

# ── Input form ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Sensor Inputs</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    device  = st.number_input("Device ID",   value=266,       step=1)
    metric1 = st.number_input("Metric 1",    value=215630672, step=1000)
    metric2 = st.number_input("Metric 2",    value=55,        step=1)
    metric3 = st.number_input("Metric 3",    value=6,         step=1)
    metric4 = st.number_input("Metric 4",    value=11,        step=1)

with col2:
    metric5 = st.number_input("Metric 5",    value=13,        step=1)
    metric6 = st.number_input("Metric 6",    value=407438,    step=100)
    metric7 = st.number_input("Metric 7",    value=0,         step=1)
    metric8 = st.number_input("Metric 8",    value=0,         step=1)
    metric9 = st.number_input("Metric 9",    value=7,         step=1)

st.markdown("<br>", unsafe_allow_html=True)

# ── Predict button ────────────────────────────────────────────────────────────
if st.button("⚡  Run Prediction"):
    payload = {
        "input": [[
            int(device), int(metric1), int(metric2), int(metric3), int(metric4),
            int(metric5), int(metric6), int(metric7), int(metric8), int(metric9)
        ]]
    }

    with st.spinner("Calling inference endpoint..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=30)
            result = response.json()
            prediction = result.get("prediction", -1)
            alert_sent = result.get("alert_sent", False)

            if prediction == 1:
                st.markdown("""
                <div class="result-box result-failure">
                    <h2>⚠️ Failure Predicted</h2>
                    <p>A machine failure is likely. Email alert has been sent via SNS.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-box result-healthy">
                    <h2>✅ Machine is Healthy</h2>
                    <p>No failure detected. System operating normally.</p>
                </div>
                """, unsafe_allow_html=True)

            # Show raw response
            with st.expander("Raw API Response"):
                st.json(result)

        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#444;">
    Built with AWS SageMaker · Lambda · API Gateway · SNS · Streamlit
</div>
""", unsafe_allow_html=True)

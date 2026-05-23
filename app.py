import streamlit as st
import pandas as pd
import psutil
import time
import random
from datetime import datetime
import plotly.graph_objects as go

# --- CONFIG ---
st.set_page_config(page_title="AI Self-Healing NOC", layout="wide", initial_sidebar_state="expanded")

# --- FUTURISTIC CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&family=Rajdhani&display=swap');
    
    .main { background-color: #050505; color: #e2e8f0; font-family: 'Rajdhani', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff6600; }
    
    .stMetric {
        background: rgba(15, 15, 15, 0.8);
        border: 1px solid rgba(255, 102, 0, 0.3);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(255, 102, 0, 0.1);
    }
    
    div[data-testid="metric-container"] label { color: #ff6600 !important; font-family: 'Orbitron'; font-size: 0.8rem; }
    div[data-testid="metric-container"] div { color: #ffffff !important; font-family: 'Orbitron'; }

    .ai-log-box {
        background-color: #000;
        border: 1px solid #ff660033;
        border-left: 4px solid #ff6600;
        padding: 10px;
        margin-bottom: 5px;
        font-family: 'Courier New';
        font-size: 12px;
        color: #ffaa00;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown("<h1 style='color: #ff6600; text-align: center;'>NOC_AI v4.0</h1>", unsafe_allow_html=True)
menu = st.sidebar.radio("NAVIGATION", ["DASHBOARD", "DEVICES", "AI ENGINE", "SECURITY"])

# --- DATA GENERATOR ---
def get_metrics():
    return {
        "download": round(random.uniform(40, 90), 2),
        "upload": round(random.uniform(10, 30), 2),
        "health": random.randint(95, 100),
        "loss": round(random.uniform(0.1, 0.5), 2),
        "cpu": psutil.cpu_percent()
    }

# --- DASHBOARD PAGE ---
if menu == "DASHBOARD":
    st.markdown("<h2 style='color: #ff6600;'>🛰️ SYSTEM LIVE MONITORING</h2>", unsafe_allow_html=True)
    
    data = get_metrics()
    
    # Top Stats
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("DOWNLOAD SPEED", f"{data['download']} Mbps", "LIVE")
    m2.metric("NETWORK HEALTH", f"{data['health']}%", "OPTIMAL")
    m3.metric("PACKET LOSS", f"{data['loss']}%", "-0.02%")
    m4.metric("CPU LOAD", f"{data['cpu']}%", "STABLE")

    # Graphs
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("### TRAFFIC FLOW")
        chart_data = pd.DataFrame({
            'Time': range(20),
            'Usage': [random.randint(40, 100) for _ in range(20)]
        })
        st.area_chart(chart_data, x='Time', y='Usage', color="#ff6600")

    with c2:
        st.markdown("### AI ENGINE LOGS")
        logs = [
            "Initializing Neural Monitor...",
            "Checking Node-B Path...",
            "Traffic Optimization: Active",
            "No threats detected in segment-7"
        ]
        for log in logs:
            st.markdown(f"<div class='ai-log-box'>> {log}</div>", unsafe_allow_html=True)

# --- DEVICES PAGE ---
elif menu == "DEVICES":
    st.title("📱 CONNECTED DEVICES")
    df = pd.DataFrame([
        {"Device": "Master-Router", "IP": "192.168.1.1", "Usage": "2.1 MB/s", "Status": "Safe"},
        {"Device": "Workstation-01", "IP": "192.168.1.15", "Usage": "0.5 MB/s", "Status": "Safe"},
        {"Device": "Unknown-Node", "IP": "10.0.0.55", "Usage": "45.2 MB/s", "Status": "SUSPICIOUS"},
    ])
    st.table(df)

# --- AUTO REFRESH ---
time.sleep(2)
st.rerun()

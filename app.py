import streamlit as st
import pandas as pd
import time
import random
import psutil
import plotly.graph_objects as go
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Self-Healing NOC", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS (Futuristic Orange & Dark Theme) ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: #e5e5e5; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff6600; }
    .stMetric { background-color: #111; border: 1px solid #ff6600; padding: 15px; border-radius: 10px; box-shadow: 0 0 10px #ff660044; }
    div[data-testid="metric-container"] label { color: #ff6600 !important; font-weight: bold; text-transform: uppercase; }
    .ai-log { background-color: #1a0f00; border-left: 5px solid #ff6600; padding: 10px; margin: 5px 0; font-family: 'Courier New'; color: #ffcc00; }
    h1, h2, h3 { color: #ff6600 !important; text-shadow: 0 0 10px #ff6600; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE FOR LOGS ---
if 'logs' not in st.session_state:
    st.session_state.logs = [{"time": datetime.now().strftime("%H:%M:%S"), "msg": "System Initialized...", "type": "INFO"}]

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("⚡ AI NOC SYSTEM")
page = st.sidebar.radio("Navigate", ["Dashboard", "Device Monitoring", "AI Engine Logs", "Cyber Attack Simulation"])

# --- AI ENGINE LOGIC ---
def ai_healer(packet_loss, download):
    if packet_loss > 2.0:
        msg = f"⚠️ HIGH PACKET LOSS ({packet_loss}%): AI Re-routing traffic to backup path..."
        st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "msg": msg, "type": "ALERT"})
        return "HEALING..."
    if download > 80:
        msg = "🚀 CONGESTION DETECTED: AI Auto-throttling heavy users."
        st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "msg": msg, "type": "OPTIMIZE"})
        return "OPTIMIZING..."
    return "STABLE"

# --- MAIN DASHBOARD ---
if page == "Dashboard":
    st.title("🛰️ AI SELF-HEALING DASHBOARD")
    
    # Real-time Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # System Stats
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    download = round(random.uniform(20, 100), 2)
    packet_loss = round(random.uniform(0.1, 4.0), 2)
    
    status = ai_healer(packet_loss, download)
    
    col1.metric("Download Speed", f"{download} Mbps", f"{random.randint(-5, 5)}%")
    col2.metric("Packet Loss", f"{packet_loss}%", "CRITICAL" if packet_loss > 2 else "NORMAL")
    col3.metric("CPU Load", f"{cpu}%", f"{random.randint(-2, 2)}%")
    col4.metric("AI Status", status)

    # Charts
    st.subheader("Network Traffic Flow (Live)")
    chart_data = pd.DataFrame({
        'Time': range(10),
        'Traffic': [random.randint(20, 100) for _ in range(10)]
    })
    st.line_chart(chart_data, x='Time', y='Traffic', use_container_width=True)

    # AI Logs on Dashboard
    st.subheader("Recent AI Actions")
    for log in st.session_state.logs[:5]:
        st.markdown(f"<div class='ai-log'>[{log['time']}] {log['msg']}</div>", unsafe_allow_html=True)

elif page == "Device Monitoring":
    st.title("📱 Connected Devices")
    devices = pd.DataFrame({
        "Device Name": ["Workstation-01", "Admin-Laptop", "Smart-Switch", "Unknown-Device"],
        "IP Address": ["192.168.1.10", "192.168.1.15", "192.168.1.1", "10.0.0.55"],
        "MAC Address": ["00:1A:2B:3C", "AA:BB:CC:DD", "11:22:33:44", "FF:EE:DD:CC"],
        "Status": ["Safe", "Safe", "Safe", "SUSPICIOUS"],
        "Bandwidth": ["12 Mbps", "45 Mbps", "2 Mbps", "88 Mbps"]
    })
    st.table(devices)
    if st.button("Block Suspicious Device"):
        st.success("AI has successfully blocked IP: 10.0.0.55")

elif page == "AI Engine Logs":
    st.title("🧠 AI Engine Intelligence Logs")
    for log in st.session_state.logs:
        st.markdown(f"<div class='ai-log'><b>{log['type']}</b> | {log['time']} | {log['msg']}</div>", unsafe_allow_html=True)

# --- REFRESH BUTTON (To simulate real-time) ---
time.sleep(1)
if page == "Dashboard":
    st.rerun()

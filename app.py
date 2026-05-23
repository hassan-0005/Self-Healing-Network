import streamlit as st
import pandas as pd
import psutil
import time
import random
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="AI Self-Healing NOC", layout="wide", initial_sidebar_state="expanded")

# --- SESSION STATE (To keep logs alive during refresh) ---
if 'ai_logs' not in st.session_state:
    st.session_state.ai_logs = []
if 'threat_logs' not in st.session_state:
    st.session_state.threat_logs = []

# --- FUTURISTIC CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&family=Rajdhani&display=swap');
    .main { background-color: #050505; color: #e2e8f0; font-family: 'Rajdhani', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 2px solid #ff6600; }
    .stMetric { background: rgba(15, 15, 15, 0.9); border: 1px solid #ff660044; border-radius: 10px; padding: 15px; box-shadow: 0 0 10px #ff660022; }
    div[data-testid="metric-container"] label { color: #ff6600 !important; font-family: 'Orbitron'; font-size: 0.7rem; letter-spacing: 1px; }
    .ai-box { background-color: #000; border-left: 4px solid #ff6600; padding: 12px; margin-bottom: 8px; font-family: 'Courier New'; color: #ffaa00; font-size: 13px; }
    .security-alert { background-color: #220000; border-left: 4px solid #ff0000; padding: 12px; color: #ff5555; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown("<h1 style='color: #ff6600; text-align: center; font-family: Orbitron;'>NOC_AI v4.0</h1>", unsafe_allow_html=True)
menu = st.sidebar.selectbox("MAIN NAVIGATION", ["DASHBOARD", "DEVICE MONITOR", "AI ENGINE LOGS", "SECURITY MONITOR"])

# --- DATA SIMULATION ENGINE ---
def generate_ai_log():
    actions = [
        "⚠️ High Latency Detected: Re-routing traffic to Node-X",
        "🚀 Congestion Spike: Auto-throttling background processes",
        "✅ Path Optimization Complete: Signal Strength +15%",
        "🔄 Connection Reset: Clearing buffer for IP 192.168.1.5",
        "🛡️ AI Guard: Filtering suspicious packet headers"
    ]
    new_log = f"[{datetime.now().strftime('%H:%M:%S')}] {random.choice(actions)}"
    st.session_state.ai_logs.insert(0, new_log)
    if len(st.session_state.ai_logs) > 15: st.session_state.ai_logs.pop()

# --- 1. DASHBOARD PAGE ---
if menu == "DASHBOARD":
    st.markdown("<h2 style='color: #ff6600; font-family: Orbitron;'>🛰️ LIVE SYSTEM OVERVIEW</h2>", unsafe_allow_html=True)
    
    # Live Metrics
    col1, col2, col3, col4 = st.columns(4)
    download = round(random.uniform(50, 95), 2)
    col1.metric("DOWNLOAD SPEED", f"{download} Mbps", f"{random.randint(-5, 5)}%")
    col2.metric("NETWORK HEALTH", "98%", "STABLE")
    col3.metric("PACKET LOSS", f"{round(random.uniform(0.1, 0.4), 2)}%", "-0.01%")
    col4.metric("CPU LOAD", f"{psutil.cpu_percent()}%", "NORMAL")

    # Traffic Graph
    st.markdown("### REAL-TIME TRAFFIC DATA")
    chart_data = pd.DataFrame({'MB/s': [random.randint(40, 100) for _ in range(25)]})
    st.area_chart(chart_data, color="#ff6600")

    # Quick AI Status
    st.markdown("###  AI ENGINE STATUS")
    generate_ai_log()
    for log in st.session_state.ai_logs[:3]:
        st.markdown(f"<div class='ai-box'>{log}</div>", unsafe_allow_html=True)

# --- 2. DEVICE MONITOR PAGE ---
elif menu == "DEVICE MONITOR":
    st.markdown("<h2 style='color: #ff6600; font-family: Orbitron;'>📱 CONNECTED DEVICES</h2>", unsafe_allow_html=True)
    devices = [
        {"Device": "Cisco-Router-01", "IP": "192.168.1.1", "Usage": "2.4 MB/s", "Status": "Active"},
        {"Device": "Workstation-Office", "IP": "192.168.1.15", "Usage": "0.8 MB/s", "Status": "Active"},
        {"Device": "Mobile-Android", "IP": "192.168.1.22", "Usage": "1.2 MB/s", "Status": "Active"},
        {"Device": "Unknown-Device", "IP": "10.0.0.88", "Usage": "52.5 MB/s", "Status": "SUSPICIOUS"},
    ]
    df = pd.DataFrame(devices)
    st.table(df)
    
    if st.button("BLOCK SUSPICIOUS IP"):
        st.error("AI ACTION: IP 10.0.0.88 has been blacklisted.")

# --- 3. AI ENGINE PAGE ---
elif menu == "AI ENGINE LOGS":
    st.markdown("<h2 style='color: #ff6600; font-family: Orbitron;'>🧠 AI SELF-HEALING ENGINE</h2>", unsafe_allow_html=True)
    st.info("The AI Engine is currently monitoring all network nodes and automatically repairing connection drops.")
    
    st.markdown("### FULL ACTIVITY LOG")
    generate_ai_log()
    for log in st.session_state.ai_logs:
        st.markdown(f"<div class='ai-box'>{log}</div>", unsafe_allow_html=True)

# --- 4. SECURITY MONITOR PAGE ---
elif menu == "SECURITY MONITOR":
    st.markdown("<h2 style='color: #ff0000; font-family: Orbitron;'>🛡️ SECURITY & THREAT DETECTION</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Current Threat Level")
        st.markdown("<h1 style='color: red; text-align: center;'>LEVEL: MEDIUM</h1>", unsafe_allow_html=True)
    
    with col2:
        st.subheader("Active Mitigation")
        st.write("✅ Firewall: Enabled")
        st.write("✅ DDoS Protection: Active")
        st.write("✅ Packet Inspection: Running")

    st.markdown("### 🚨 SECURITY ALERTS")
    threats = [
        "DDoS Simulation detected from IP 185.22.xx.xx",
        "Rogue Device 'Kali-Linux' attempted to join subnet",
        "Brute force attempt blocked on Port 22"
    ]
    if random.random() > 0.7:
        st.markdown(f"<div class='security-alert'>[CRITICAL] {random.choice(threats)}</div>", unsafe_allow_html=True)
    else:
        st.success("No active cyber threats detected in the last 10 minutes.")

# --- AUTO REFRESH (Every 2 seconds) ---
time.sleep(2)
st.rerun()

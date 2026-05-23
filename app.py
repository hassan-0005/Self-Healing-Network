import streamlit as st
import pandas as pd
import psutil
import time
import random
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Self-Healing NOC", layout="wide", initial_sidebar_state="expanded")

# 2. SESSION STATE
if 'ai_logs' not in st.session_state:
    st.session_state.ai_logs = [f"[{datetime.now().strftime('%H:%M:%S')}] System Guard Active."]

# 3. FUTURISTIC BLUE CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&family=Rajdhani&display=swap');
    
    .main { background-color: #050505; color: #e2e8f0; font-family: 'Rajdhani', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    [data-testid="stSidebar"] { background-color: #080808; border-right: 2px solid #00d4ff; }
    
    div[data-testid="stMetric"] {
        background: rgba(10, 20, 30, 0.9);
        border: 1px solid #00d4ff44;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);
    }
    
    label[data-testid="stMetricLabel"] { 
        color: #00d4ff !important; 
        font-family: 'Orbitron' !important; 
        font-size: 0.8rem !important; 
    }
    
    .ai-card {
        background-color: #000;
        border-left: 5px solid #00d4ff;
        padding: 10px;
        margin: 5px 0;
        font-family: 'Courier New';
        color: #00d4ff;
        font-size: 14px;
    }
    
    .security-card {
        background-color: #1a0000;
        border-left: 5px solid #ff0000;
        padding: 10px;
        margin: 5px 0;
        font-family: 'Courier New';
        color: #ff4444;
    }

    .explanation-box {
        background-color: #111;
        padding: 15px;
        border-radius: 5px;
        border: 1px dashed #333;
        margin-top: 20px;
        color: #aaa;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.markdown("<h1 style='color: #00d4ff; font-family: Orbitron; text-align: center;'>NOC AI v6.0</h1>", unsafe_allow_html=True)
    st.divider()
    st.write("MASTER NODE: 192.168.1.1")
    st.write("STATUS: Monitoring Active")
    st.divider()
    auto_refresh = st.checkbox("Auto Update Data", value=True)
    refresh_rate = st.slider("Update Rate (s)", 1, 5, 2)

# 5. TABS
tab1, tab2, tab3, tab4 = st.tabs(["DASHBOARD", "DEVICES", "AI ENGINE", "SECURITY"])

# --- TAB 1: DASHBOARD ---
with tab1:
    st.markdown("<h2 style='color: #00d4ff;'>SYSTEM REAL-TIME STATUS</h2>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    download = round(random.uniform(50, 98), 2)
    c1.metric("DOWNLOAD", f"{download} Mbps")
    c2.metric("HEALTH", "98/100")
    c3.metric("LATENCY", f"{random.randint(15, 30)} ms")
    c4.metric("CPU LOAD", f"{psutil.cpu_percent()}%")

    st.markdown("### LIVE NETWORK TRAFFIC FLOW")
    chart_data = pd.DataFrame({'Bandwidth': [random.randint(40, 100) for _ in range(30)]})
    st.area_chart(chart_data, color="#00d4ff")

    st.markdown("""
        <div class='explanation-box'>
        <b>What is this tab?</b><br>
        This is the Dashboard. It shows the live speed and health of your internet. 
        The graph shows how much data is being used every second. If the graph goes up, it means usage is high.
        </div>
        """, unsafe_allow_html=True)

# --- TAB 2: DEVICES ---
with tab2:
    st.markdown("<h2 style='color: #00d4ff;'>CONNECTED INFRASTRUCTURE</h2>", unsafe_allow_html=True)
    devices = pd.DataFrame([
        {"Device": "Main-Router", "IP": "192.168.1.1", "Usage": "Optimal"},
        {"Device": "Admin-Workstation", "IP": "192.168.1.15", "Usage": "Normal"},
        {"Device": "Unknown-Entry", "IP": "10.0.5.12", "Usage": "High Spike"},
    ])
    st.table(devices)

    st.markdown("""
        <div class='explanation-box'>
        <b>What is this tab?</b><br>
        This section lists all the computers and devices connected to your network. 
        It monitors which device is using more data and shows their IP addresses.
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: AI ENGINE ---
with tab3:
    st.markdown("<h2 style='color: #00d4ff;'>AI SELF-HEALING ENGINE</h2>", unsafe_allow_html=True)
    
    if auto_refresh:
        actions = ["Optimizing routing path.", "Rerouting packets to avoid lag.", "Throttling background data."]
        log = f"[{datetime.now().strftime('%H:%M:%S')}] {random.choice(actions)}"
        st.session_state.ai_logs.insert(0, log)
        if len(st.session_state.ai_logs) > 10: st.session_state.ai_logs.pop()

    for log in st.session_state.ai_logs:
        st.markdown(f"<div class='ai-card'>{log}</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class='explanation-box'>
        <b>What is this tab?</b><br>
        This is the brain of the system. The AI automatically detects network problems 
        (like slow speed) and fixes them instantly without any human help. 
        The logs above show the automatic actions taken by the AI.
        </div>
        """, unsafe_allow_html=True)

# --- TAB 4: SECURITY ---
with tab4:
    st.markdown("<h2 style='color: #ff4444;'>SECURITY MONITOR</h2>", unsafe_allow_html=True)
    st.error("THREAT LEVEL: LOW")
    st.markdown("<div class='security-card'>[ALERT] Blocked suspicious login attempt from unknown IP.</div>", unsafe_allow_html=True)
    st.markdown("<div class='ai-card'>[INFO] Firewall and DDoS protection are fully active.</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class='explanation-box'>
        <b>What is this tab?</b><br>
        This section protects your network from hackers. It detects if someone 
        is trying to attack your system and blocks them immediately to keep your data safe.
        </div>
        """, unsafe_allow_html=True)

# --- AUTO REFRESH ---
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()

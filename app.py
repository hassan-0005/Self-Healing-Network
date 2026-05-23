import streamlit as st
import pandas as pd
import psutil
import time
import random
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Self-Healing NOC", layout="wide", initial_sidebar_state="expanded")

# 2. SESSION STATE INITIALIZATION
if 'ai_logs' not in st.session_state:
    st.session_state.ai_logs = [f"[{datetime.now().strftime('%H:%M:%S')}] System Cyber-Guard Active."]
if 'threats' not in st.session_state:
    st.session_state.threats = []

# 3. FUTURISTIC BLUE CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&family=Rajdhani&display=swap');
    
    .main { background-color: #050505; color: #e2e8f0; font-family: 'Rajdhani', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Sidebar styling - BLUE BORDER */
    [data-testid="stSidebar"] { background-color: #080808; border-right: 2px solid #00d4ff; }
    
    /* Metrics / Cards - BLUE GLOW */
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
        text-shadow: 0 0 5px #00d4ff;
    }
    
    /* Custom AI Log Boxes - BLUE THEME */
    .ai-card {
        background-color: #000;
        border-left: 5px solid #00d4ff;
        padding: 10px;
        margin: 5px 0;
        font-family: 'Courier New';
        color: #00d4ff;
        font-size: 14px;
        background: linear-gradient(90deg, rgba(0, 212, 255, 0.05) 0%, transparent 100%);
    }
    
    .security-card {
        background-color: #0a0000;
        border-left: 5px solid #ff0000;
        padding: 10px;
        margin: 5px 0;
        font-family: 'Courier New';
        color: #ff4444;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #111;
        border: 1px solid #00d4ff33;
        border-radius: 5px 5px 0 0;
        color: #888;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00d4ff22 !important;
        border-color: #00d4ff !important;
        color: #00d4ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR - SYSTEM CONTROL
with st.sidebar:
    st.markdown("<h1 style='color: #00d4ff; font-family: Orbitron; text-align: center; text-shadow: 0 0 10px #00d4ff;'>NOC AI v5.0</h1>", unsafe_allow_html=True)
    st.divider()
    st.write("🛰️ **MASTER NODE:** 192.168.1.1")
    st.write("🔵 **STATUS:** Monitoring")
    st.divider()
    auto_refresh = st.checkbox("Live Stream Data", value=True)
    refresh_rate = st.slider("Update Interval (s)", 1, 5, 2)
    if st.button("Purge AI Logs"):
        st.session_state.ai_logs = []

# 5. MAIN TOP NAVIGATION
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💎 DASHBOARD", 
    "📡 DEVICES", 
    "🧠 AI ENGINE", 
    "🛡️ SECURITY", 
    "📊 ANALYTICS"
])

# --- DATA HELPER FUNCTIONS ---
def get_ai_action():
    actions = [
        "Network latency optimized at Segment-A.",
        "Blue-Guard AI: Rerouting packets to avoid congestion.",
        "Security handshake successful for Admin-Node.",
        "Traffic throttling applied to heavy background processes.",
        "Encrypted tunnel established for remote workstation.",
        "AI Engine: Self-healing protocol at 100% efficiency."
    ]
    return f"[{datetime.now().strftime('%H:%M:%S')}] {random.choice(actions)}"

# ---------------------------------------------------------
# TAB 1: DASHBOARD
# ---------------------------------------------------------
with tab1:
    st.markdown("<h2 style='color: #00d4ff;'>REAL-TIME NETWORK OVERVIEW</h2>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    download = round(random.uniform(60, 120), 2)
    c1.metric("DOWNLOAD", f"{download} Mbps", f"{random.randint(-5, 12)}%")
    c2.metric("HEALTH SCORE", "99/100", "OPTIMAL")
    c3.metric("LATENCY", f"{random.randint(15, 35)} ms", "STABLE")
    c4.metric("CPU UTIL", f"{psutil.cpu_percent()}%", "NORMAL")

    st.markdown("### 📈 BANDWIDTH CONSUMPTION (LIVE)")
    # Live chart with BLUE color
    chart_data = pd.DataFrame({'Data Flow': [random.randint(50, 120) for _ in range(30)]})
    st.area_chart(chart_data, color="#00d4ff")

# ---------------------------------------------------------
# TAB 2: DEVICE MONITOR
# ---------------------------------------------------------
with tab2:
    st.markdown("<h2 style='color: #00d4ff;'>CONNECTED INFRASTRUCTURE</h2>", unsafe_allow_html=True)
    devices = pd.DataFrame([
        {"Device": "Cisco-Core-Router", "IP": "192.168.1.1", "Traffic": "Optimal", "Status": "Encrypted"},
        {"Device": "Workstation-Alpha", "IP": "192.168.1.15", "Traffic": "Steady", "Status": "Safe"},
        {"Device": "IoT-Gateway", "IP": "192.168.1.22", "Traffic": "Low", "Status": "Safe"},
        {"Device": "Unknown-Entry", "IP": "10.0.5.12", "Traffic": "SPIKE", "Status": "VERIFYING"},
    ])
    st.dataframe(devices, use_container_width=True)
    
    if st.button("Initiate Hardware Scan"):
        with st.spinner("Analyzing network packets..."):
            time.sleep(1)
            st.info("Scan Complete: 4 Devices identified. No rogue nodes found.")

# ---------------------------------------------------------
# TAB 3: AI ENGINE (Self-Healing)
# ---------------------------------------------------------
with tab3:
    st.markdown("<h2 style='color: #00d4ff;'>AI SELF-HEALING ENGINE</h2>", unsafe_allow_html=True)
    st.write("Autonomous AI monitoring active. System is auto-correcting routing tables and buffer sizes.")
    
    if auto_refresh:
        st.session_state.ai_logs.insert(0, get_ai_action())
        if len(st.session_state.ai_logs) > 20: st.session_state.ai_logs.pop()

    st.markdown("### 📜 AI COGNITIVE LOGS")
    for log in st.session_state.ai_logs:
        st.markdown(f"<div class='ai-card'>{log}</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 4: SECURITY MONITOR
# ---------------------------------------------------------
with tab4:
    st.markdown("<h2 style='color: #ff4444;'>SECURITY THREAT RADAR</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.error("THREAT LEVEL: LOW")
        st.progress(15)
    with col2:
        st.info("CYBER-GUARD: ACTIVE")
        st.write("🛡️ Packet Inspection: 100% Coverage")
    
    st.markdown("### 🚨 SECURITY EVENTS")
    st.markdown("<div class='security-card'>[INFO] Brute force attempt blocked from 192.x.x.x by Blue-Shield.</div>", unsafe_allow_html=True)
    st.markdown("<div class='ai-card'>[INFO] No new critical threats detected in last 24 hours.</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 5: ANALYTICS
# ---------------------------------------------------------
with tab5:
    st.markdown("<h2 style='color: #00d4ff;'>SYSTEM PERFORMANCE ANALYTICS</h2>", unsafe_allow_html=True)
    analytics_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Efficiency': [85, 88, 92, 85, 99, 97, 98]
    })
    st.bar_chart(analytics_data, x='Day', y='Efficiency', color="#007bff")

# --- AUTO REFRESH LOGIC ---
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()

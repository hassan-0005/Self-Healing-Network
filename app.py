import streamlit as st
import pandas as pd
import psutil
import time
import random
import plotly.graph_objects as go
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Self-Healing NOC", layout="wide", initial_sidebar_state="expanded")

# 2. SESSION STATE FOR DATA PERSISTENCE
if 'ohlc_data' not in st.session_state:
    # Initial dummy data for candles
    st.session_state.ohlc_data = pd.DataFrame(columns=['Time', 'Open', 'High', 'Low', 'Close'])
if 'ai_logs' not in st.session_state:
    st.session_state.ai_logs = [f"[{datetime.now().strftime('%H:%M:%S')}] System Cyber-Guard Active."]

# 3. FUTURISTIC BLUE CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&family=Rajdhani&display=swap');
    
    .main { background-color: #050505; color: #e2e8f0; font-family: 'Rajdhani', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #080808; border-right: 2px solid #00d4ff; }
    
    /* Metrics / Cards */
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
    
    /* AI Log Boxes */
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

# 4. DATA SIMULATION FOR CANDLESTICK
def update_traffic_data():
    now = datetime.now().strftime('%H:%M:%S')
    # Generate OHLC values for network traffic
    base = random.randint(60, 90)
    open_val = base + random.uniform(-2, 2)
    close_val = base + random.uniform(-2, 2)
    high_val = max(open_val, close_val) + random.uniform(1, 5)
    low_val = min(open_val, close_val) - random.uniform(1, 5)
    
    new_entry = {
        'Time': now,
        'Open': open_val,
        'High': high_val,
        'Low': low_val,
        'Close': close_val
    }
    
    # Update session state dataframe
    st.session_state.ohlc_data = pd.concat([st.session_state.ohlc_data, pd.DataFrame([new_entry])], ignore_index=True)
    if len(st.session_state.ohlc_data) > 20: # Keep last 20 seconds
        st.session_state.ohlc_data = st.session_state.ohlc_data.iloc[1:]

# 5. SIDEBAR - SYSTEM CONTROL
with st.sidebar:
    st.markdown("<h1 style='color: #00d4ff; font-family: Orbitron; text-align: center;'>NOC AI v6.0</h1>", unsafe_allow_html=True)
    st.divider()
    st.write("MASTER NODE: 192.168.1.1")
    st.write("STATUS: Monitoring Active")
    st.divider()
    auto_refresh = st.checkbox("Live Stream Data", value=True)
    refresh_rate = st.slider("Update Interval (s)", 1, 5, 1)
    if st.button("Purge AI Logs"):
        st.session_state.ai_logs = []

# 6. MAIN TOP NAVIGATION
tab1, tab2, tab3, tab4 = st.tabs([
    "DASHBOARD", 
    "DEVICES", 
    "AI ENGINE", 
    "SECURITY"
])

# ---------------------------------------------------------
# TAB 1: DASHBOARD (Candlestick Chart)
# ---------------------------------------------------------
with tab1:
    st.markdown("<h2 style='color: #00d4ff;'>REAL-TIME NETWORK OVERVIEW</h2>", unsafe_allow_html=True)
    
    update_traffic_data()
    
    c1, c2, c3, c4 = st.columns(4)
    curr = st.session_state.ohlc_data.iloc[-1]
    c1.metric("CURRENT LOAD", f"{round(curr['Close'], 2)} Mbps")
    c2.metric("HEALTH SCORE", "99/100")
    c3.metric("LATENCY", f"{random.randint(15, 30)} ms")
    c4.metric("CPU UTIL", f"{psutil.cpu_percent()}%")

    st.markdown("### NETWORK TRAFFIC CANDLESTICK ANALYSIS")
    
    # Plotly Candlestick Chart
    fig = go.Figure(data=[go.Candlestick(
        x=st.session_state.ohlc_data['Time'],
        open=st.session_state.ohlc_data['Open'],
        high=st.session_state.ohlc_data['High'],
        low=st.session_state.ohlc_data['Low'],
        close=st.session_state.ohlc_data['Close'],
        increasing_line_color='#00d4ff', # Cyan for Up
        decreasing_line_color='#004466'  # Dark Blue for Down
    )])
    
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=400,
        yaxis_title="Bandwidth Usage (Mbps)"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: DEVICES
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

# ---------------------------------------------------------
# TAB 3: AI ENGINE
# ---------------------------------------------------------
with tab3:
    st.markdown("<h2 style='color: #00d4ff;'>AI SELF-HEALING ENGINE</h2>", unsafe_allow_html=True)
    
    if auto_refresh:
        actions = ["Latency optimized at Segment-A.", "Rerouting packets to avoid congestion.", "Throttling applied to heavy processes."]
        new_log = f"[{datetime.now().strftime('%H:%M:%S')}] {random.choice(actions)}"
        st.session_state.ai_logs.insert(0, new_log)
        if len(st.session_state.ai_logs) > 15: st.session_state.ai_logs.pop()

    for log in st.session_state.ai_logs:
        st.markdown(f<div class='ai-card'>{log}</div>, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 4: SECURITY
# ---------------------------------------------------------
with tab4:
    st.markdown("<h2 style='color: #ff4444;'>SECURITY THREAT RADAR</h2>", unsafe_allow_html=True)
    st.error("THREAT LEVEL: LOW")
    st.markdown("<div class='security-card'>[INFO] Brute force attempt blocked from 192.x.x.x by Blue-Shield AI.</div>", unsafe_allow_html=True)

# --- AUTO REFRESH ---
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()

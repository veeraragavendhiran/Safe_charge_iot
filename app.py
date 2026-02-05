import streamlit as st
import serial
import json
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import serial.tools.list_ports
import random
import warnings
from datetime import datetime, timedelta
import math
import base64
import io
import asyncio
from typing import Dict, List, Optional, Tuple
import threading
from scipy import signal

warnings.filterwarnings('ignore')

# Configuration
SERIAL_PORT = 'COM7' 
BAUD_RATE = 115200

# Set page config
st.set_page_config(
    page_title="⚡ SAFE-CHARGE X | QUANTUM GUARDIAN PRO",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# COHESIVE BLUE THEME CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0b0018 0%, #00000f 35%, #0a0022 65%, #120033 100%);
        color: #e5faff;
        background-attachment: fixed;
    }
    
    /* VIBRANT NEON BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, 
            #ff008d 0%, 
            #d400ff 40%, 
            #00d4ff 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 16px 32px !important;
        border-radius: 20px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 12px 35px rgba(212, 0, 255, 0.65),
                    0 0 30px rgba(0, 212, 255, 0.5),
                    inset 0 0 15px rgba(255, 255, 255, 0.15) !important;
        position: relative !important;
        overflow: hidden !important;
        letter-spacing: 1.8px !important;
        text-transform: uppercase !important;
        min-height: 62px !important;
        border: 2px solid rgba(255, 102, 255, 0.6) !important;
        margin: 12px 0 !important;
        width: 100% !important;
    }
    
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -120% !important;
        width: 120% !important;
        height: 100% !important;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.6), 
            transparent) !important;
        transition: left 0.9s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-7px) scale(1.06) !important;
        box-shadow: 0 25px 55px rgba(212, 0, 255, 0.85),
                    0 0 65px rgba(0, 212, 255, 0.75),
                    0 0 90px rgba(255, 0, 255, 0.45) !important;
        border-color: rgba(255, 153, 255, 1) !important;
        background: linear-gradient(135deg, 
            #ff33aa 0%, 
            #e600ff 40%, 
            #00eaff 100%) !important;
    }
    
    .stButton > button:hover::before {
        left: 120% !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.97) !important;
        transition: all 0.12s ease !important;
    }
    
    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, 
            #00f0ff 0%, 
            #00aaff 50%, 
            #aa00ff 100%) !important;
        box-shadow: 0 12px 35px rgba(0, 240, 255, 0.65),
                    0 0 30px rgba(170, 0, 255, 0.5) !important;
        border: 2px solid rgba(0, 255, 255, 0.65) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        box-shadow: 0 25px 55px rgba(0, 240, 255, 0.85),
                    0 0 65px rgba(170, 0, 255, 0.75),
                    0 0 90px rgba(0, 170, 255, 0.45) !important;
        background: linear-gradient(135deg, 
            #33ffff 0%, 
            #33ccff 50%, 
            #cc33ff 100%) !important;
        border-color: rgba(51, 255, 255, 1) !important;
    }
    
    /* Sidebar glow pulse */
    section[data-testid="stSidebar"] .stButton > button {
        animation: buttonGlow 2.2s infinite alternate !important;
        margin: 18px 0 !important;
    }
    
    @keyframes buttonGlow {
        0% {
            box-shadow: 0 12px 35px rgba(212, 0, 255, 0.65),
                        0 0 30px rgba(0, 212, 255, 0.5);
        }
        100% {
            box-shadow: 0 12px 35px rgba(212, 0, 255, 0.9),
                        0 0 45px rgba(0, 212, 255, 0.7),
                        0 0 70px rgba(170, 0, 255, 0.4);
        }
    }
    
    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        background: linear-gradient(90deg, #00ffff, #ff00aa, #aa00ff, #00ffea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 40px rgba(170, 0, 255, 0.7),
                     0 0 20px rgba(0, 255, 255, 0.5);
    }
    
    .glass-panel {
        background: rgba(10, 5, 35, 0.88);
        backdrop-filter: blur(28px) saturate(180%);
        -webkit-backdrop-filter: blur(28px) saturate(180%);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 24px;
        padding: 28px;
        margin: 18px 0;
        box-shadow: 0 15px 50px rgba(0, 170, 255, 0.3),
                    inset 0 0 30px rgba(0, 255, 255, 0.12),
                    0 0 25px rgba(170, 0, 255, 0.2);
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(20, 10, 60, 0.9), rgba(8, 5, 40, 0.9));
        border-radius: 24px;
        padding: 28px;
        border: 2px solid rgba(0, 255, 255, 0.3);
        transition: all 0.45s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 15px 50px rgba(0, 170, 255, 0.28),
                    inset 0 0 25px rgba(255, 0, 255, 0.08);
    }
    
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 18px;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.15rem;
        color: #00ffff;
        padding: 14px 28px;
        background: rgba(0, 255, 255, 0.15);
        border-radius: 18px;
        border: 2px solid rgba(0, 255, 255, 0.4);
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.35),
                    inset 0 0 12px rgba(0, 255, 255, 0.2);
        text-shadow: 0 0 15px rgba(0, 255, 255, 0.7);
    }
    
    /* Emergency buttons */
    .stButton > button:has-text("⏸️") {
        background: linear-gradient(135deg, #ffea00 0%, #ffcc00 50%, #ff9900 100%) !important;
        box-shadow: 0 12px 35px rgba(255, 204, 0, 0.7) !important;
    }
    
    .stButton > button:has-text("🛑") {
        background: linear-gradient(135deg, #ff3366 0%, #ff1a1a 50%, #cc0000 100%) !important;
        box-shadow: 0 12px 35px rgba(255, 51, 102, 0.7) !important;
    }
    
    .stButton > button:has-text("🔄") {
        background: linear-gradient(135deg, #00ffcc 0%, #00ff99 50%, #00cc77 100%) !important;
        box-shadow: 0 12px 35px rgba(0, 255, 204, 0.7) !important;
    }
    
    /* Interference warning */
    .interference-warning {
        background: linear-gradient(135deg, rgba(255, 153, 0, 0.25), rgba(255, 102, 0, 0.2));
        padding: 15px 25px;
        border-radius: 15px;
        margin: 15px 0;
        border: 2px solid rgba(255, 153, 0, 0.5);
        text-align: center;
        animation: pulseWarning 2s infinite;
    }
    
    @keyframes pulseWarning {
        0% { box-shadow: 0 0 0 0 rgba(255, 153, 0, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(255, 153, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 153, 0, 0); }
    }
    
    /* Live dot animation */
    .live-dot {
        width: 12px;
        height: 12px;
        background: linear-gradient(135deg, #00ffff, #ff00aa);
        border-radius: 50%;
        animation: livePulse 2s infinite;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.7);
    }
    
    @keyframes livePulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 255, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 255, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 255, 0); }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# INITIALIZE SESSION STATE
# ============================================
if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = True
    st.session_state.simulation_mode = True
    st.session_state.ser = None
    st.session_state.connection_status = "SIMULATION"
    st.session_state.auto_refresh = True
    
    # Interference tracking
    st.session_state.cloth_applied = False
    st.session_state.spray_applied = False
    st.session_state.interference_detected = False
    st.session_state.interference_start_time = None
    
    # Data Storage
    st.session_state.data_log = pd.DataFrame({
        'timestamp': pd.Series(dtype='datetime64[ns]'),
        'temperature': pd.Series(dtype='float'),
        'predicted_temp': pd.Series(dtype='float'),
        'gas_level': pd.Series(dtype='int'),
        'current': pd.Series(dtype='float'),
        'voltage': pd.Series(dtype='float'),
        'power': pd.Series(dtype='float'),
        'soc': pd.Series(dtype='float'),
        'frequency': pd.Series(dtype='float'),
        'efficiency': pd.Series(dtype='float'),
        'battery_health': pd.Series(dtype='float'),
        'charge_rate': pd.Series(dtype='float'),
        'grid_stability': pd.Series(dtype='float')
    })
    
    # Current Metrics
    st.session_state.current_metrics = {
        'temperature': 28.5,
        'predicted_temp': 29.2,
        'gas_level': 145,
        'current': 9.8,
        'voltage': 415.2,
        'power': 4069.0,
        'soc': 78.5,
        'frequency': 50.0,
        'efficiency': 94.3,
        'battery_health': 98.7,
        'charge_rate': 9.8,
        'grid_stability': 99.2
    }
    
    # System State
    st.session_state.system_state = {
        'status': 'OPTIMAL',
        'theme_color': '#00aaff',
        'danger_level': 0,
        'charging_mode': 'FAST_CHARGE',
        'alerts_active': 0,
        'uptime': 0,
        'data_points': 0,
        'last_update': datetime.now(),
        'emergency_override': False,
        'system_load': 25.0,
        'ai_confidence': 95.3
    }
    
    # Alerts
    st.session_state.alerts = [
        {'time': datetime.now().strftime("%H:%M:%S"), 'type': 'info', 'message': 'System initialized in simulation mode', 'read': False},
        {'time': datetime.now().strftime("%H:%M:%S"), 'type': 'success', 'message': 'All systems operational and ready', 'read': False}
    ]
    
    # Settings
    st.session_state.settings = {
        'refresh_rate': 1.0,
        'alert_threshold_temp': 45.0,
        'alert_threshold_gas': 1000,
        'auto_shutdown': True,
        'data_logging': True,
        'ai_prediction': True,
        'notifications': True
    }
    
    # Performance metrics
    st.session_state.performance = {
        'avg_temperature': 28.5,
        'max_temperature': 35.0,
        'avg_efficiency': 94.3,
        'total_energy': 0.0,
        'safety_score': 98.5
    }

# ============================================
# HELPER FUNCTIONS
# ============================================
def add_alert(message, alert_type="info"):
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    alert = {
        'time': timestamp,
        'type': alert_type,
        'message': message,
        'read': False
    }
    st.session_state.alerts.insert(0, alert)
    if len(st.session_state.alerts) > 20:
        st.session_state.alerts.pop()
    st.session_state.system_state['alerts_active'] = len([a for a in st.session_state.alerts if not a['read']])

def initialize_serial():
    if not st.session_state.simulation_mode and st.session_state.ser is None:
        try:
            st.session_state.ser = serial.Serial(
                SERIAL_PORT, 
                BAUD_RATE, 
                timeout=0.02,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            time.sleep(2)
            st.session_state.connection_status = "LIVE_CONNECTED"
            st.session_state.system_state['status'] = "ACTIVE"
            add_alert("✅ Serial connection established successfully", "success")
            return True
        except Exception as e:
            st.session_state.simulation_mode = True
            st.session_state.connection_status = "SIMULATION"
            add_alert(f"⚠️ Failed to connect to {SERIAL_PORT}: {str(e)[:50]}", "warning")
            return False
    return True

def process_simulation_data():
    current_time = datetime.now()
    time_factor = current_time.timestamp() / 100
    hour_of_day = current_time.hour + current_time.minute / 60
    
    # Temperature simulation
    daily_variation = 5 * math.sin((hour_of_day - 12) * math.pi / 12)
    random_noise = random.uniform(-0.5, 0.5)
    new_temp = 28.0 + daily_variation + random_noise
    st.session_state.current_metrics['temperature'] = max(20, min(65, new_temp))
    
    # AI prediction
    if len(st.session_state.data_log) > 5:
        recent_temps = st.session_state.data_log['temperature'].tail(5).values
        temp_momentum = np.mean(np.diff(recent_temps[-3:])) if len(recent_temps) > 1 else 0
        st.session_state.current_metrics['predicted_temp'] = st.session_state.current_metrics['temperature'] + temp_momentum * 3
    else:
        st.session_state.current_metrics['predicted_temp'] = st.session_state.current_metrics['temperature'] + random.uniform(0, 1.5)
    
    # Gas level
    base_gas = 150 + 50 * math.sin(time_factor / 1000)
    if random.random() < 0.01:
        gas_spike = random.uniform(50, 200)
    else:
        gas_spike = 0
    
    st.session_state.current_metrics['gas_level'] = max(0, int(base_gas + random.uniform(-20, 20) + gas_spike))
    
    # Power system
    load_variation = 0.5 * math.sin(time_factor / 500)
    st.session_state.current_metrics['current'] = 9.8 + load_variation + random.uniform(-0.3, 0.3)
    st.session_state.current_metrics['voltage'] = 415.0 + random.uniform(-3, 3)
    st.session_state.current_metrics['power'] = st.session_state.current_metrics['current'] * st.session_state.current_metrics['voltage']
    
    # Battery simulation
    if st.session_state.current_metrics['soc'] < 95:
        charge_rate = 0.3 if st.session_state.system_state['charging_mode'] == 'FAST_CHARGE' else 0.15
        charge_rate *= (1 + random.uniform(-0.1, 0.1))
        st.session_state.current_metrics['soc'] = min(100, st.session_state.current_metrics['soc'] + charge_rate)
    else:
        st.session_state.current_metrics['soc'] += random.uniform(-0.05, 0.05)
    
    # Other metrics
    st.session_state.current_metrics['frequency'] = 50.0 + random.uniform(-0.1, 0.1)
    st.session_state.current_metrics['efficiency'] = max(85, 94.0 + random.uniform(-0.5, 0.5))
    st.session_state.current_metrics['battery_health'] = max(80, st.session_state.current_metrics['battery_health'] + random.uniform(-0.05, 0.02))
    st.session_state.current_metrics['grid_stability'] = 99.0 + random.uniform(-0.5, 0.5)
    st.session_state.current_metrics['charge_rate'] = st.session_state.current_metrics['current']

def update_data_log():
    new_entry = {
        'timestamp': datetime.now(),
        'temperature': st.session_state.current_metrics['temperature'],
        'predicted_temp': st.session_state.current_metrics['predicted_temp'],
        'gas_level': st.session_state.current_metrics['gas_level'],
        'current': st.session_state.current_metrics['current'],
        'voltage': st.session_state.current_metrics['voltage'],
        'power': st.session_state.current_metrics['power'],
        'soc': st.session_state.current_metrics['soc'],
        'frequency': st.session_state.current_metrics['frequency'],
        'efficiency': st.session_state.current_metrics['efficiency'],
        'battery_health': st.session_state.current_metrics['battery_health'],
        'charge_rate': st.session_state.current_metrics['charge_rate'],
        'grid_stability': st.session_state.current_metrics['grid_stability']
    }
    
    new_df = pd.DataFrame([new_entry])
    if st.session_state.data_log.empty:
        st.session_state.data_log = new_df
    else:
        st.session_state.data_log = pd.concat([st.session_state.data_log, new_df], ignore_index=True)
    
    if len(st.session_state.data_log) > 300:
        st.session_state.data_log = st.session_state.data_log.iloc[-300:]
    
    st.session_state.system_state['data_points'] = len(st.session_state.data_log)
    
    if len(st.session_state.data_log) > 10:
        st.session_state.performance['avg_temperature'] = st.session_state.data_log['temperature'].mean()
        st.session_state.performance['max_temperature'] = st.session_state.data_log['temperature'].max()
        st.session_state.performance['avg_efficiency'] = st.session_state.data_log['efficiency'].mean()

def analyze_safety():
    temp = st.session_state.current_metrics['temperature']
    gas = st.session_state.current_metrics['gas_level']
    
    danger_score = 0
    new_status = 'OPTIMAL'
    new_theme = '#00aaff'
    new_danger_level = 0
    
    # Apply interference effects if active
    actual_temp = temp
    actual_gas = gas
    
    if st.session_state.cloth_applied:
        # Cloth reduces temperature reading by 8-12°C
        temp_reduction = random.uniform(8, 12)
        actual_temp = temp  # Displayed temp (suppressed)
        real_temp = temp + temp_reduction  # Real temp (hidden)
        
        # Use real temp for danger calculation
        temp = real_temp
    
    if st.session_state.spray_applied:
        # Spray reduces gas reading by 30-50%
        gas_reduction_factor = random.uniform(0.3, 0.5)
        actual_gas = gas  # Displayed gas (suppressed)
        real_gas = gas / (1 - gas_reduction_factor)  # Real gas (hidden)
        
        # Use real gas for danger calculation
        gas = real_gas
    
    # Temperature analysis
    if temp >= 55:
        danger_score = 100
        new_status = 'CRITICAL'
        new_theme = '#ff5555'
        new_danger_level = 3
        if st.session_state.cloth_applied:
            add_alert(f'🔥 CRITICAL: Thermal danger HIDDEN by cloth! Real temp: {temp:.1f}°C', 'critical')
        else:
            add_alert('🔥 CRITICAL: Thermal runaway detected!', 'critical')
    elif temp >= 45:
        danger_score = 70 + min(30, (temp - 45) * 3)
        new_status = 'WARNING'
        new_theme = '#ffcc00'
        new_danger_level = 2
        if st.session_state.cloth_applied:
            add_alert(f'⚠️ WARNING: High temperature MASKED by cloth. Real: {temp:.1f}°C', 'warning')
        else:
            add_alert(f'⚠️ WARNING: High temperature ({temp:.1f}°C)', 'warning')
    elif temp >= 35:
        danger_score = 30 + min(40, (temp - 35) * 4)
        new_status = 'ACTIVE'
        new_theme = '#00ff88'
        new_danger_level = 1
    else:
        danger_score = max(0, temp - 20)
    
    # Gas analysis
    if gas >= 2000:
        danger_score = max(danger_score, 100)
        new_status = 'CRITICAL'
        new_theme = '#ff5555'
        new_danger_level = 3
        if st.session_state.spray_applied:
            add_alert(f'☣️ CRITICAL: Gas leak HIDDEN by spray! Real: {gas:.0f} PPM', 'critical')
        else:
            add_alert('☣️ CRITICAL: Gas leak detected!', 'critical')
    elif gas >= 1000:
        gas_danger = 60 + min(40, (gas - 1000) / 25)
        danger_score = max(danger_score, gas_danger)
        if new_danger_level < 2:
            new_status = 'WARNING'
            new_theme = '#ffcc00'
            new_danger_level = 2
        if st.session_state.spray_applied:
            add_alert(f'⚠️ WARNING: Gas levels MASKED by spray. Real: {gas:.0f} PPM', 'warning')
        else:
            add_alert(f'⚠️ WARNING: Elevated gas levels ({gas:.0f} PPM)', 'warning')
    
    # Update displayed values with interference
    if st.session_state.cloth_applied:
        st.session_state.current_metrics['temperature'] = actual_temp
    if st.session_state.spray_applied:
        st.session_state.current_metrics['gas_level'] = actual_gas
    
    # Calculate safety score with interference penalty
    temp_score = max(0, 100 - (temp - 25) * 2)
    gas_score = max(0, 100 - gas / 20)
    efficiency_score = st.session_state.current_metrics['efficiency']
    battery_score = st.session_state.current_metrics['battery_health']
    
    base_safety_score = (temp_score * 0.4 + gas_score * 0.3 + efficiency_score * 0.2 + battery_score * 0.1)
    
    # Apply interference penalty
    interference_penalty = 0
    if st.session_state.cloth_applied:
        interference_penalty += 30
    if st.session_state.spray_applied:
        interference_penalty += 25
    
    safety_score = max(0, base_safety_score - interference_penalty)
    
    # Set interference status
    if st.session_state.cloth_applied or st.session_state.spray_applied:
        new_status = 'INTERFERENCE'
        new_theme = '#ff9900'
        st.session_state.interference_detected = True
    
    # Update system state
    st.session_state.system_state['status'] = new_status
    st.session_state.system_state['theme_color'] = new_theme
    st.session_state.system_state['danger_level'] = new_danger_level
    st.session_state.performance['safety_score'] = safety_score
    
    # Update system load with interference
    interference_load = 25 if (st.session_state.cloth_applied or st.session_state.spray_applied) else 0
    st.session_state.system_state['system_load'] = 25 + random.uniform(-5, 15) + danger_score * 0.3 + interference_load
    
    return danger_score

def create_gauge_chart(value, title, min_val=0, max_val=100, color='#00aaff'):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 16, 'family': 'Orbitron', 'color': '#88aaff'}},
        number={'font': {'size': 28, 'family': 'Orbitron', 'color': color}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 2, 'tickcolor': "#88aaff"},
            'bar': {'color': color},
            'bgcolor': "rgba(15, 30, 60, 0.3)",
            'borderwidth': 2,
            'bordercolor': "rgba(0, 170, 255, 0.3)",
            'steps': [
                {'range': [min_val, max_val * 0.6], 'color': 'rgba(0, 170, 255, 0.2)'},
                {'range': [max_val * 0.6, max_val * 0.8], 'color': 'rgba(255, 200, 0, 0.2)'},
                {'range': [max_val * 0.8, max_val], 'color': 'rgba(255, 50, 50, 0.2)'}
            ],
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#88aaff", 'family': "Exo 2"},
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def process_data():
    if not st.session_state.simulation_mode:
        initialize_serial()
    
    process_simulation_data()
    update_data_log()
    danger_score = analyze_safety()
    
    st.session_state.system_state['uptime'] += 1 / st.session_state.settings['refresh_rate']
    st.session_state.system_state['last_update'] = datetime.now()
    
    return danger_score

# ============================================
# MAIN APP LAYOUT
# ============================================

# Process data
danger_score = process_data()

# Header
col1, col2, col3 = st.columns([2, 3, 2])

with col1:
    st.markdown('<div class="live-indicator"><div class="live-dot"></div> LIVE SYSTEM</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-family: Exo 2; color: #88aaff; font-size: 0.9rem;">{st.session_state.connection_status}</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<h1 class="cyber-title" style="text-align: center; font-size: 3rem;">SAFE-CHARGE X</h1>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-family: Exo 2; color: #88aaff; letter-spacing: 4px; font-size: 1.1rem;">QUANTUM GUARDIAN PRO</div>', unsafe_allow_html=True)

with col3:
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f'<div style="text-align: right; font-family: Orbitron; color: #00aaff; font-size: 1.2rem;">{current_time}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: right; font-family: Exo 2; color: #88aaff; font-size: 0.9rem;">Refresh: {st.session_state.settings["refresh_rate"]:.1f} Hz</div>', unsafe_allow_html=True)

# Interference Warning Banner
if st.session_state.cloth_applied or st.session_state.spray_applied:
    st.markdown('''
    <div class="interference-warning">
        <div style="font-family: Orbitron; color: #ff9900; font-size: 1.3rem; margin-bottom: 8px;">
            ⚠️ SENSOR INTERFERENCE DETECTED
        </div>
        <div style="font-family: Exo 2; color: #ffcc99; font-size: 1rem;">
            Safety score reduced by 25-45 points | Readings may be inaccurate
        </div>
    </div>
    ''', unsafe_allow_html=True)

# Status Banner
status_color = st.session_state.system_state['theme_color']
status_icon = {
    'OPTIMAL': '⚡',
    'ACTIVE': '✅',
    'WARNING': '⚠️',
    'CRITICAL': '🔥',
    'SHUTDOWN': '🛑',
    'INTERFERENCE': '🚨'
}.get(st.session_state.system_state['status'], '⚡')

st.markdown(f'''
<div class="glass-panel">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="font-size: 2.5rem; color: {status_color};">
                {status_icon}
            </div>
            <div>
                <div style="font-family: Orbitron; font-size: 1.8rem; color: {status_color};">
                    {st.session_state.system_state['status']}
                </div>
                <div style="font-family: Exo 2; color: #88aaff;">
                    Last update: {st.session_state.system_state['last_update'].strftime("%H:%M:%S")}
                </div>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="font-family: Exo 2; color: #88aaff; font-size: 0.9rem;">SAFETY SCORE</div>
            <div style="font-family: Orbitron; font-size: 2rem; color: {status_color};">
                {st.session_state.performance["safety_score"]:.1f}/100
            </div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Main Metrics Grid
st.markdown('<br>', unsafe_allow_html=True)

# Row 1
col1, col2, col3, col4 = st.columns(4)

with col1:
    temp_color = '#00aaff'
    temp = st.session_state.current_metrics['temperature']
    if temp > 45:
        temp_color = '#ffcc00'
    if temp > 55:
        temp_color = '#ff5555'
    
    st.markdown(f'''
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <div class="metric-label">CORE TEMPERATURE</div>
                <div class="metric-value">{temp:.1f}°C</div>
            </div>
            <div style="font-size: 1.8rem; color: {temp_color};">🔥</div>
        </div>
        <div style="margin-top: 15px;">
            <div style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden;">
                <div style="width: {min(temp/65*100, 100)}%; height: 100%; background: {temp_color};"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                <span style="font-size: 0.8rem; color: #88aaff;">20°C</span>
                <span style="font-size: 0.8rem; color: #88aaff;">65°C</span>
            </div>
        </div>
        <div style="margin-top: 10px; padding: 8px; background: rgba(0, 170, 255, 0.1); border-radius: 8px;">
            <div style="font-family: Exo 2; color: #00aaff; font-size: 0.9rem;">
                🤖 AI Predict: {st.session_state.current_metrics['predicted_temp']:.1f}°C
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    gas_color = '#00aaff'
    gas = st.session_state.current_metrics['gas_level']
    if gas > 1000:
        gas_color = '#ffcc00'
    if gas > 2000:
        gas_color = '#ff5555'
    
    gas_status = "CLEAN"
    if gas > 2000:
        gas_status = "HAZARDOUS"
    elif gas > 1000:
        gas_status = "POOR"
    elif gas > 500:
        gas_status = "MODERATE"
    
    st.markdown(f'''
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <div class="metric-label">AIR QUALITY</div>
                <div class="metric-value">{gas}</div>
                <div style="font-family: Exo 2; color: {gas_color}; font-size: 0.85rem; margin-top: 5px;">
                    PPM • {gas_status}
                </div>
            </div>
            <div style="font-size: 1.8rem; color: {gas_color};">💨</div>
        </div>
        <div style="margin-top: 15px;">
            <div style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden;">
                <div style="width: {min(gas/3000*100, 100)}%; height: 100%; background: {gas_color};"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                <span style="font-size: 0.8rem; color: #88aaff;">0</span>
                <span style="font-size: 0.8rem; color: #88aaff;">3000</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    power_color = '#00aaff'
    power = st.session_state.current_metrics['power'] / 1000
    
    st.markdown(f'''
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <div class="metric-label">POWER SYSTEM</div>
                <div class="metric-value">{power:.1f} kW</div>
            </div>
            <div style="font-size: 1.8rem; color: {power_color};">⚡</div>
        </div>
        <div style="margin-top: 15px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div style="text-align: center; padding: 10px; background: rgba(0, 170, 255, 0.15); border-radius: 8px;">
                    <div style="font-family: Orbitron; color: #00aaff; font-size: 1.2rem;">
                        {st.session_state.current_metrics['current']:.1f}
                    </div>
                    <div style="font-family: Exo 2; color: #88aaff; font-size: 0.8rem;">CURRENT</div>
                </div>
                <div style="text-align: center; padding: 10px; background: rgba(0, 136, 255, 0.15); border-radius: 8px;">
                    <div style="font-family: Orbitron; color: #0088ff; font-size: 1.2rem;">
                        {st.session_state.current_metrics['voltage']:.0f}
                    </div>
                    <div style="font-family: Exo 2; color: #88aaff; font-size: 0.8rem;">VOLTAGE</div>
                </div>
            </div>
        </div>
        <div style="margin-top: 10px; padding: 8px; background: rgba(0, 170, 255, 0.1); border-radius: 8px;">
            <div style="font-family: Exo 2; color: #00aaff; font-size: 0.9rem;">
                Grid: {st.session_state.current_metrics['frequency']:.1f} Hz • {st.session_state.current_metrics['grid_stability']:.1f}% Stable
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    soc_color = '#00aaff'
    soc = st.session_state.current_metrics['soc']
    if soc < 20:
        soc_color = '#ffcc00'
    if soc < 10:
        soc_color = '#ff5555'
    
    st.markdown(f'''
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <div class="metric-label">BATTERY STATUS</div>
                <div class="metric-value">{soc:.1f}%</div>
            </div>
            <div style="font-size: 1.8rem; color: {soc_color};">🔋</div>
        </div>
        <div style="margin-top: 15px;">
            <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
                <div style="width: {soc}%; height: 100%; background: linear-gradient(90deg, #00aaff, #0088ff);"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                <div style="text-align: center;">
                    <div style="font-family: Exo 2; color: #88aaff; font-size: 0.8rem;">HEALTH</div>
                    <div style="font-family: Orbitron; color: #00aaff; font-size: 1rem;">
                        {st.session_state.current_metrics['battery_health']:.1f}%
                    </div>
                </div>
                <div style="text-align: center;">
                    <div style="font-family: Exo 2; color: #88aaff; font-size: 0.8rem;">EFFICIENCY</div>
                    <div style="font-family: Orbitron; color: #00aaff; font-size: 1rem;">
                        {st.session_state.current_metrics['efficiency']:.1f}%
                    </div>
                </div>
                <div style="text-align: center;">
                    <div style="font-family: Exo 2; color: #88aaff; font-size: 0.8rem;">RATE</div>
                    <div style="font-family: Orbitron; color: #00aaff; font-size: 1rem;">
                        {st.session_state.current_metrics['charge_rate']:.1f}A
                    </div>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)

# Charts Section
if not st.session_state.data_log.empty and len(st.session_state.data_log) > 5:
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature Trend Chart
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            y=st.session_state.data_log['temperature'].tail(50),
            mode='lines',
            name='Temperature',
            line=dict(color=st.session_state.system_state['theme_color'], width=3)
        ))
        
        if st.session_state.settings['ai_prediction']:
            fig_temp.add_trace(go.Scatter(
                y=st.session_state.data_log['predicted_temp'].tail(50),
                mode='lines',
                name='AI Prediction',
                line=dict(color='#ffffff', width=2, dash='dash')
            ))
        
        fig_temp.update_layout(
            title='Temperature Trend',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15, 30, 60, 0.3)',
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor='rgba(0, 170, 255, 0.1)', showticklabels=False),
            yaxis=dict(title='°C', gridcolor='rgba(0, 170, 255, 0.1)', title_font=dict(color='#88aaff'))
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # Current Gauge
        fig_gauge = create_gauge_chart(
            st.session_state.current_metrics['current'],
            "Current Consumption",
            min_val=0,
            max_val=15,
            color=st.session_state.system_state['theme_color']
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

# ============================================
# SIDEBAR CONTROLS
# ============================================
with st.sidebar:
    # Header / Branding
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(120, 0, 255, 0.18), rgba(0, 180, 255, 0.12));
                padding: 24px 20px;
                border-radius: 18px;
                margin-bottom: 28px;
                border: 1px solid rgba(100, 120, 255, 0.35);
                box-shadow: 0 10px 40px rgba(80, 0, 255, 0.28);
                text-align: center;
                backdrop-filter: blur(10px);">
        <h2 style="margin: 0; font-family: 'Orbitron', sans-serif; 
                   background: linear-gradient(90deg, #ff33cc, #aa00ff, #00eaff);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   font-size: 1.85rem; letter-spacing: 2px;
                   text-shadow: 0 0 24px rgba(170, 0, 255, 0.7);">
            ⚡ CONTROL PANEL
        </h2>
        <div style="font-family: 'Exo 2', sans-serif; color: #b3e0ff; font-size: 1rem; 
                    margin-top: 10px; letter-spacing: 1px; opacity: 0.9;">
            Safe-Charge X v3.0<br>QUANTUM GUARDIAN
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Operation Mode
    st.markdown("""
    <div style="font-family: 'Orbitron', sans-serif; color: #ff66cc; 
                font-size: 1.3rem; letter-spacing: 1.5px; margin: 0 0 16px 0;">
        🚀 OPERATION MODE
    </div>
    """, unsafe_allow_html=True)

    mode_col1, mode_col2 = st.columns(2)
    with mode_col1:
        if st.button("LIVE", 
                     use_container_width=True,
                     type="primary" if not st.session_state.simulation_mode else "secondary"):
            st.session_state.simulation_mode = False
            if initialize_serial():
                add_alert("Switched to LIVE mode", "info")
            st.rerun()
    
    with mode_col2:
        if st.button("SIM", 
                     use_container_width=True,
                     type="primary" if st.session_state.simulation_mode else "secondary"):
            st.session_state.simulation_mode = True
            st.session_state.connection_status = "SIMULATION"
            add_alert("Switched to SIMULATION mode", "info")
            st.rerun()

    # Current Mode Status
    current_mode = "LIVE" if not st.session_state.simulation_mode else "SIMULATION"
    mode_color = "#00ffff" if not st.session_state.simulation_mode else "#cc99ff"
    mode_glow  = "#00ffffff60" if not st.session_state.simulation_mode else "#cc99ffff60"

    st.markdown(f"""
    <div style="background: rgba(12, 15, 50, 0.7); 
                padding: 18px; 
                border-radius: 14px; 
                border-left: 5px solid {mode_color};
                box-shadow: 0 8px 30px {mode_glow};
                margin: 20px 0 28px 0; text-align: center;">
        <div style="font-family: 'Exo 2', sans-serif; color: #b3e0ff; font-size: 0.9rem;">
            CURRENT MODE
        </div>
        <div style="font-family: 'Orbitron', sans-serif; color: {mode_color}; 
                    font-size: 1.7rem; margin: 8px 0; letter-spacing: 2px;
                    text-shadow: 0 0 16px {mode_glow};">
            {current_mode}
        </div>
        <div style="font-family: 'Exo 2', sans-serif; color: #99ccff; font-size: 0.85rem; opacity: 0.9;">
            {st.session_state.connection_status}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Emergency Controls
    st.markdown("""
    <div style="font-family: 'Orbitron', sans-serif; color: #ff4d4d; 
                font-size: 1.3rem; letter-spacing: 1.5px; margin: 0 0 16px 0;">
        🚨 EMERGENCY CONTROLS
    </div>
    """, unsafe_allow_html=True)

    emer_col1, emer_col2, emer_col3 = st.columns(3)
    with emer_col1:
        if st.button("⏸️ PAUSE", use_container_width=True, help="Pause all operations"):
            st.session_state.system_state['emergency_override'] = True
            add_alert("System paused by operator", "warning")
            st.rerun()

    with emer_col2:
        if st.button("🛑 STOP", use_container_width=True, help="Emergency shutdown"):
            st.session_state.system_state['status'] = 'SHUTDOWN'
            st.session_state.system_state['theme_color'] = '#ff3366'
            add_alert("EMERGENCY SHUTDOWN ACTIVATED", "critical")
            st.rerun()

    with emer_col3:
        if st.button("🔄 RESET", use_container_width=True, help="Reset system"):
            st.session_state.system_state['emergency_override'] = False
            st.session_state.system_state['status'] = 'ACTIVE'
            st.session_state.system_state['theme_color'] = '#00aaff'
            add_alert("System reset initiated", "info")
            st.rerun()

    st.divider()

    # Interference Simulation
    st.markdown("""
    <div style="font-family: 'Orbitron', sans-serif; color: #ff9900; 
                font-size: 1.2rem; letter-spacing: 1px; margin: 0 0 16px 0;">
        🧪 SENSOR INTERFERENCE TEST
    </div>
    """, unsafe_allow_html=True)
    
    # Current interference status
    interference_active = st.session_state.cloth_applied or st.session_state.spray_applied
    status_color = "#ff9900" if interference_active else "#00cc66"
    status_text = "ACTIVE ⚠️" if interference_active else "INACTIVE ✅"
    
    st.markdown(f"""
    <div style="background: rgba(30, 20, 0, 0.3); 
                padding: 12px; 
                border-radius: 10px; 
                margin-bottom: 15px;
                border: 1px solid {status_color}80;
                text-align: center;">
        <div style="font-family: 'Exo 2', sans-serif; color: #ffcc99; font-size: 0.85rem;">
            INTERFERENCE STATUS
        </div>
        <div style="font-family: 'Orbitron', sans-serif; color: {status_color}; 
                    font-size: 1.1rem; margin-top: 5px;">
            {status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interference control buttons
    int_col1, int_col2 = st.columns(2)
    with int_col1:
        if st.button("🧺 Apply Cloth", 
                     use_container_width=True,
                     help="Simulate cloth covering temperature sensor",
                     type="primary" if st.session_state.cloth_applied else "secondary"):
            st.session_state.cloth_applied = True
            add_alert('🧺 Cloth applied to temperature sensor - Readings suppressed!', 'warning')
            st.rerun()
    
    with int_col2:
        if st.button("💨 Apply Spray", 
                     use_container_width=True,
                     help="Simulate spray affecting gas sensor",
                     type="primary" if st.session_state.spray_applied else "secondary"):
            st.session_state.spray_applied = True
            add_alert('💨 Spray applied near gas sensor - Readings affected!', 'warning')
            st.rerun()
    
    # Clear all interference
    if st.button("🧹 Clear All Interference", 
                 use_container_width=True,
                 help="Remove all sensor interference"):
        st.session_state.cloth_applied = False
        st.session_state.spray_applied = False
        st.session_state.interference_detected = False
        add_alert('✅ All sensor interference cleared', 'success')
        st.rerun()

    st.divider()

    # System Settings
    st.markdown("""
    <div style="font-family: 'Orbitron', sans-serif; color: #66ffff; 
                font-size: 1.25rem; letter-spacing: 1.2px; margin: 0 0 16px 0;">
        ⚙️ SYSTEM SETTINGS
    </div>
    """, unsafe_allow_html=True)

    st.session_state.settings['refresh_rate'] = st.slider(
        "Refresh Rate (Hz)",
        min_value=0.2,
        max_value=10.0,
        value=st.session_state.settings['refresh_rate'],
        step=0.2,
        help="Data update frequency"
    )

    st.markdown('<div style="font-family: Exo 2; color: #b3e0ff; font-size: 0.95rem; margin: 20px 0 12px 0;">ALERT THRESHOLDS</div>', unsafe_allow_html=True)

    thresh_col1, thresh_col2 = st.columns(2)
    with thresh_col1:
        st.session_state.settings['alert_threshold_temp'] = st.number_input(
            "Temp (°C)", min_value=30.0, max_value=70.0,
            value=st.session_state.settings['alert_threshold_temp'],
            step=1.0, key="temp_threshold"
        )

    with thresh_col2:
        st.session_state.settings['alert_threshold_gas'] = st.number_input(
            "Gas (PPM)", min_value=100, max_value=5000,
            value=st.session_state.settings['alert_threshold_gas'],
            step=100, key="gas_threshold"
        )

    toggle_col1, toggle_col2 = st.columns(2)
    with toggle_col1:
        st.session_state.settings['ai_prediction'] = st.toggle("AI Prediction", value=st.session_state.settings['ai_prediction'])
        st.session_state.settings['auto_shutdown'] = st.toggle("Auto Shutdown", value=st.session_state.settings['auto_shutdown'])

    with toggle_col2:
        st.session_state.settings['data_logging'] = st.toggle("Data Logging", value=st.session_state.settings['data_logging'])
        st.session_state.settings['notifications'] = st.toggle("Notifications", value=st.session_state.settings['notifications'])

    st.divider()

    # System Info Display
    col1, col2 = st.columns(2)
    
    with col1:
        # Format uptime
        hours = int(st.session_state.system_state['uptime'] // 3600)
        minutes = int((st.session_state.system_state['uptime'] % 3600) // 60)
        seconds = int(st.session_state.system_state['uptime'] % 60)
        
        st.markdown(f"""
        <div style="background: rgba(0, 50, 100, 0.3); 
                    padding: 15px; 
                    border-radius: 12px; 
                    margin-bottom: 10px;
                    border: 1px solid rgba(0, 200, 255, 0.2);">
            <div style="font-family: 'Exo 2', sans-serif; color: #b3e0ff; font-size: 0.8rem;">
                UPTIME
            </div>
            <div style="font-family: 'Orbitron', sans-serif; color: #00ffff; font-size: 1.2rem; margin-top: 5px;">
                {hours:02d}:{minutes:02d}:{seconds:02d}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(0, 50, 100, 0.3); 
                    padding: 15px; 
                    border-radius: 12px;
                    border: 1px solid rgba(0, 200, 255, 0.2);">
            <div style="font-family: 'Exo 2', sans-serif; color: #b3e0ff; font-size: 0.8rem;">
                DATA POINTS
            </div>
            <div style="font-family: 'Orbitron', sans-serif; color: #00ffff; font-size: 1.2rem; margin-top: 5px;">
                {st.session_state.system_state['data_points']:,}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: rgba(100, 0, 50, 0.3); 
                    padding: 15px; 
                    border-radius: 12px; 
                    margin-bottom: 10px;
                    border: 1px solid rgba(255, 0, 100, 0.2);">
            <div style="font-family: 'Exo 2', sans-serif; color: #ffb3e0; font-size: 0.8rem;">
                ACTIVE ALERTS
            </div>
            <div style="font-family: 'Orbitron', sans-serif; color: #ff66cc; font-size: 1.2rem; margin-top: 5px;">
                {st.session_state.system_state['alerts_active']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(0, 100, 50, 0.3); 
                    padding: 15px; 
                    border-radius: 12px;
                    border: 1px solid rgba(0, 255, 150, 0.2);">
            <div style="font-family: 'Exo 2', sans-serif; color: #b3ffcc; font-size: 0.8rem;">
                SYSTEM LOAD
            </div>
            <div style="font-family: 'Orbitron', sans-serif; color: #00ff88; font-size: 1.2rem; margin-top: 5px;">
                {st.session_state.system_state['system_load']:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # System Status Summary
    status_color = st.session_state.system_state['theme_color']
    status_text = st.session_state.system_state['status']

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(15, 10, 60, 0.8), rgba(30, 10, 90, 0.7)); 
                padding: 20px; border-radius: 16px; margin-top: 20px;
                border: 1px solid {status_color}50; text-align: center;
                box-shadow: 0 12px 45px rgba(100, 0, 255, 0.3);">
        <div style="font-family: 'Exo 2', sans-serif; color: #b3e0ff; font-size: 0.9rem;">
            SYSTEM STATUS
        </div>
        <div style="font-family: 'Orbitron', sans-serif; color: {status_color}; 
                    font-size: 2.1rem; margin: 12px 0; letter-spacing: 2.5px;
                    text-shadow: 0 0 25px {status_color}90;">
            {status_text}
        </div>
        <div style="font-family: 'Exo 2', sans-serif; color: #99ccff; font-size: 0.85rem;">
            Last update: {st.session_state.system_state['last_update'].strftime('%H:%M:%S')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# ALERTS PANEL
# ============================================
st.markdown('<br>', unsafe_allow_html=True)

with st.expander(f"🚨 ACTIVE ALERTS ({st.session_state.system_state['alerts_active']})", expanded=True):
    if st.session_state.alerts:
        for i, alert in enumerate(st.session_state.alerts[:10]):
            alert_color = {
                'critical': '#ff5555',
                'warning': '#ffcc00',
                'info': '#00aaff',
                'success': '#00ff88'
            }.get(alert['type'], '#88aaff')
            
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f'''
                <div style="background: rgba{tuple(int(alert_color[i:i+2], 16) for i in (1, 3, 5)) + (0.15,)};
                           border-left: 4px solid {alert_color};
                           padding: 15px; margin: 8px 0; border-radius: 0 12px 12px 0;">
                    <div style="font-family: 'Exo 2', sans-serif; color: white; font-size: 0.95rem; margin-bottom: 5px;">
                        {alert['message']}
                    </div>
                    <div style="font-family: 'Exo 2', sans-serif; color: {alert_color}; font-size: 0.8rem;">
                        {alert['time']}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                if not alert['read']:
                    if st.button("✓", key=f"read_{i}", help="Mark as read"):
                        alert['read'] = True
                        st.session_state.system_state['alerts_active'] -= 1
                        st.rerun()
                else:
                    st.markdown('<div style="color: #88aaff; text-align: center; padding-top: 20px;">✓</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div style="text-align: center; padding: 40px; background: rgba(0, 170, 255, 0.05); border-radius: 16px;">
            <div style="font-size: 3rem; color: #00aaff; margin-bottom: 10px;">✅</div>
            <div style="font-family: 'Exo 2', sans-serif; color: #88aaff; font-size: 1.1rem; margin-bottom: 10px;">
                All systems operating normally
            </div>
            <div style="font-family: 'Exo 2', sans-serif; color: #88aaff; font-size: 0.9rem;">
                No active alerts detected
            </div>
        </div>
        ''', unsafe_allow_html=True)

# ============================================
# AUTO-REFRESH
# ============================================
sleep_time = max(0.1, 1.0 / st.session_state.settings['refresh_rate'])
time.sleep(sleep_time)
st.rerun()
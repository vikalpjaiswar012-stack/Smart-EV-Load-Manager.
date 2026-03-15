import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- 1. PAGE SETUP & THEME ---
st.set_page_config(page_title="HPCL Smart EV Load Manager", layout="wide")

# HPCL Branding Header
st.markdown("""
    <div style="background-color:#003366;padding:15px;border-radius:10px;border-left:8px solid #ed1c24;">
        <h1 style="color:white;margin:0;">HPCL HPe-Charge | Industrial Load Manager</h1>
        <p style="color:white;margin:5px;">Smart DLM • Dynamic Pricing • Solar Integration</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: INFRASTRUCTURE INPUTS ---
st.sidebar.header("🏢 Station Infrastructure")
grid_limit = st.sidebar.slider("Grid Sanctioned Load (kW)", 50, 250, 100)
base_load = st.sidebar.slider("Outlet Base Load (kW)", 5, 50, 20)

# Functionality 1: Solar Integration
st.sidebar.markdown("---")
st.sidebar.header("☀️ Renewable Input")
solar_gen = st.sidebar.slider("Solar PV Generation (kW)", 0, 40, 15)

# Functionality 2: Charger Demand & SoC
st.sidebar.markdown("---")
st.sidebar.header("🚗 EV Charger Demand")
ev1_req = st.sidebar.number_input("Car 1 Request (kW)", 0, 60, 45)
ev1_soc = st.sidebar.slider("Car 1 Battery % (SoC)", 0, 100, 25)

ev2_req = st.sidebar.number_input("Car 2 Request (kW)", 0, 60, 45)
ev2_soc = st.sidebar.slider("Car 2 Battery % (SoC)", 0, 100, 75)

# --- 3. CORE LOGIC ENGINE ---

# A. Dynamic Pricing Logic
current_hour = datetime.now().hour
is_peak = 18 <= current_hour <= 22  # Peak: 6 PM - 10 PM
base_price = 16.0
price_multiplier = 1.5 if is_peak else 1.0
current_rate = base_price * price_multiplier

# B. Smart Load Balancing Logic (SoC Priority)
# Total Available Power = (Grid - Base) + Solar
total_available = (grid_limit - base_load) + solar_gen
total_demand = ev1_req + ev2_req

if total_demand > total_available:
    # Priority weighting: Car with lower SoC gets more power
    w1 = (100 - ev1_soc)
    w2 = (100 - ev2_soc)
    ev1_final = (w1 / (w1 + w2)) * total_available
    ev2_final = (w2 / (w1 + w2)) * total_available
    sys_status = "🔴 Throttling Active"
else:
    ev1_final, ev2_final = ev1_req, ev2_req
    sys_status = "🟢 System Stable"

# --- 4. DASHBOARD DISPLAY ---

# Top Row: Key Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Rate", f"₹{current_rate}/kWh", "Peak" if is_peak else "Normal")
m2.metric("Solar Contribution", f"{solar_gen} kW")
m3.metric("Total Load", f"{round(base_load + ev1_final + ev2_final, 1)} kW")
m4.metric("Status", sys_status)

st.markdown("---")

# Visual Stacked Bar Chart
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Live Power Allocation")
    fig = go.Figure(data=[
        go.Bar(name='Retail Base Load', x=['Station'], y=[base_load], marker_color='#FF4B4B'),
        go.Bar(name='Car 1 (High Priority)', x=['Station'], y=[ev1_final], marker_color='#00CC96'),
        go.Bar(name='Car 2 (Standard)', x=['Station'], y=[ev2_final], marker_color='#636EFA')
    ])
    # Draw Grid Limit Line
    fig.add_shape(type="line", x0=-0.5, x1=0.5, y0=grid_limit, y1=grid_limit, 
                 line=dict(color="Black", width=3, dash="dash"))
    fig.update_layout(barmode='stack', yaxis_title="Power (kW)")
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("💰 Financial Analytics")
    hourly_rev = (ev1_final + ev2_final) * current_rate
    st.write(f"**Est. Revenue:** ₹{round(hourly_rev, 2)} / hr")
    st.progress(min(1.0, (base_load + ev1_final + ev2_final)/grid_limit))
    st.write(f"Grid Capacity Utilization: {round(((base_load + ev1_final + ev2_final)/grid_limit)*100, 1)}%")

    st.subheader("🛡️ Safety Diagnostics")
    st.json({
        "OCPP_Status": "Connected",
        "Transformer_Temp": "54°C",
        "Ground_Fault": "None",
        "Frequency": "50.02 Hz"
    })

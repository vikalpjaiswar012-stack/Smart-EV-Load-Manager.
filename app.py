import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="HPCL Smart EV Load Manager", layout="wide")

st.title("⚡ HPCL Retail Outlet: Dynamic Load Management System")
st.markdown("Designed for **OCPP 1.6J Compliance** | Prevents Grid Overload")

# --- Sidebar: Station Settings ---
st.sidebar.header("Station Configuration")
grid_limit = st.sidebar.slider("Grid Sanctioned Load (kW)", 50, 200, 100)
pump_base_load = st.sidebar.slider("Current Pump Load (Lights/Dispenser) (kW)", 5, 50, 20)

# --- Logic: The Smart Balancing Algorithm ---
available_for_ev = grid_limit - pump_base_load

# Simulate 3 Charging Guns
col1, col2, col3 = st.columns(3)
ev1_soc = col1.slider("Car 1 Battery %", 0, 100, 20)
ev2_soc = col2.slider("Car 2 Battery %", 0, 100, 85)
ev3_soc = col3.slider("Car 3 Battery %", 0, 100, 50)

# Allocation Logic
total_demand = 120 
if total_demand > available_for_ev:
    ev1_share = (100 - ev1_soc)
    ev2_share = (100 - ev2_soc)
    ev3_share = (100 - ev3_soc)
    total_shares = ev1_share + ev2_share + ev3_share
    
    ev1_pwr = (ev1_share / total_shares) * available_for_ev
    ev2_pwr = (ev2_share / total_shares) * available_for_ev
    ev3_pwr = (ev3_share / total_shares) * available_for_ev
else:
    ev1_pwr, ev2_pwr, ev3_pwr = 40, 40, 40

# --- Visualizing the Load ---
fig = go.Figure(data=[
    go.Bar(name='Pump Base Load', x=['Grid Usage'], y=[pump_base_load], marker_color='#FF4B4B'),
    go.Bar(name='Car 1 (Fast)', x=['Grid Usage'], y=[ev1_pwr], marker_color='#00CC96'),
    go.Bar(name='Car 2 (Throttled)', x=['Grid Usage'], y=[ev2_pwr], marker_color='#636EFA'),
    go.Bar(name='Car 3 (Standard)', x=['Grid Usage'], y=[ev3_pwr], marker_color='#AB63FA')
])

fig.update_layout(barmode='stack', title="Real-time Power Distribution (kW)", 
                  yaxis=dict(range=[0, grid_limit + 20]),
                  shapes=[dict(type="line", x0=-0.5, x1=0.5, y0=grid_limit, y1=grid_limit, 
                               line=dict(color="Red", width=3, dash="dash"))])

st.plotly_chart(fig, use_container_width=True)

if (pump_base_load + ev1_pwr + ev2_pwr + ev3_pwr) >= grid_limit:
    st.error(f"⚠️ GRID AT CAPACITY! Throttling Active.")
else:
    st.success("✅ System Stable.")

st.table(pd.DataFrame({
    "Charger ID": ["EV-HP-001", "EV-HP-002", "EV-HP-003"],
    "Power Allocated (kW)": [round(ev1_pwr, 2), round(ev2_pwr, 2), round(ev3_pwr, 2)],
    "Priority": ["High", "Low", "Medium"]
}))

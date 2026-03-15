import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="HPCL Data-Driven Load Manager", layout="wide")

st.title("⚡ HPCL Smart EV: Real-Time Data Replay")
st.markdown("Replaying historical session data to test **Dynamic Load Balancing** logic.")

# --- Load the Data ---
@st.cache_data
def load_data():
    # Try to load the CSV, otherwise use dummy data for safety
    try:
        df = pd.read_csv("ev_data.csv")
        return df
    except:
        return pd.DataFrame({
            'energy_dispensed_kwh': [10, 25, 40, 15, 30],
            'grid_load_mw': [0.1, 0.2, 0.15, 0.25, 0.1]
        })

df = load_data()

# --- Simulation State ---
if 'row_index' not in st.session_state:
    st.session_state.row_index = 0

# Get current data point
current_row = df.iloc[st.session_state.row_index]
demand_kw = current_row['energy_dispensed_kwh'] 
grid_status = "High Demand" if current_row['grid_load_mw'] > 0.2 else "Normal"

# --- Load Balancing Logic ---
limit = 35 # Assume a fixed safety limit of 35kW for this transformer
actual_power = min(demand_kw, limit)
throttled = demand_kw > limit

# --- Display ---
c1, c2, c3 = st.columns(3)
c1.metric("Historical Demand", f"{round(demand_kw, 1)} kW")
c2.metric("Allocated Power", f"{round(actual_power, 1)} kW")
c3.metric("Grid Status", grid_status)

if throttled:
    st.warning(f"⚠️ LOAD SHEDDING: Original demand was {demand_kw}kW. Throttled to {limit}kW to protect transformer.")
else:
    st.success("✅ Powering vehicle at 100% requested rate.")

# Visualization
st.bar_chart({"Requested": demand_kw, "Delivered": actual_power})

# --- Auto-Step Logic ---
st.session_state.row_index = (st.session_state.row_index + 1) % len(df)
time.sleep(3)
st.rerun()

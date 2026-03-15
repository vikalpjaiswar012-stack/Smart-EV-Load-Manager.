# HPCL Smart EV: Dynamic Load Management (DLM) System

![License](https://img.shields.io/badge/Industry-Oil%20%26%20Gas-blue)
![OCPP](https://img.shields.io/badge/Protocol-OCPP%201.6J-green)
![Python](https://img.shields.io/badge/Tech-Python%20%7C%20Streamlit-orange)

### 📌 Project Overview
As HPCL transitions to an "Energy Company," installing high-power DC Fast Chargers at existing fuel retail outlets presents a major challenge: **Grid Capacity.** This project provides a **Software-Defined Load Balancing** solution that monitors the total power consumption of a petrol pump in real-time. It dynamically throttles the power allocated to EV chargers to ensure the station stays within its sanctioned grid limit, eliminating the need for expensive transformer upgrades.

### 🚀 Key Features
- **Dynamic Power Throttling:** Real-time adjustment of charging speeds based on total outlet load (Lights + Dispensers + EV Chargers).
- **SoC-Based Priority:** Automatically gives higher power to vehicles with lower battery percentages (State of Charge).
- **OCPP 1.6J Simulation:** Uses JSON-based WebSocket logic to simulate industry-standard communication between the charger and the Central Management System (CSMS).
- **Live Dashboard:** Interactive UI for station managers to monitor grid health and charging session status.

### 🛠️ Tech Stack
- **Language:** Python 3.9+
- **Framework:** Streamlit (For the Real-time Dashboard)
- **Visualization:** Plotly & Pandas
- **Communication Protocol:** JSON/WebSockets (Simulating OCPP 1.6J)

### 🏭 Industry Relevance (PSU Context)
- **Operational Safety:** Aligned with **OISD-156** standards for electrical installations in hazardous petroleum zones.
- **Cost Optimization:** Reduces **CAPEX** by 40-60% by utilizing existing transformer capacity.
- **Interoperability:** Built on Open Charge Point Protocols, supporting HPCL's goal of a vendor-neutral charging network.

### 💻 How to Run
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/HPCL-Smart-EV-Load-Manager.git](https://github.com/YOUR_USERNAME/HPCL-Smart-EV-Load-Manager.git)

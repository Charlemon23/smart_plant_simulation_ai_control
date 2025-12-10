import time
import pandas as pd
import streamlit as st

LOG_PATH = "run_log.csv"
REFRESH_INTERVAL = 1  # seconds

st.set_page_config(page_title="Digital Twin Demo", layout="wide")

st.title("AI-Controlled Smart Chemical Plant – Digital Twin Demonstration")

# ---------------------------
# Tabs for full DCS experience
# ---------------------------
tab_overview, tab_trends, tab_actions, tab_kpis = st.tabs(
    ["Overview", "Trends", "Controller Actions", "KPIs"]
)

def load_data():
    try:
        return pd.read_csv(LOG_PATH)
    except:
        return pd.DataFrame(columns=["step", "T", "C", "coolant_flow", "feed_rate"])

while True:
    df = load_data()

    if df.empty:
        st.warning("Waiting for simulation data...")
        time.sleep(REFRESH_INTERVAL)
        continue

    latest = df.tail(1)

    # ----------------------------------------------------
    # TAB 1 — OVERVIEW
    # ----------------------------------------------------
    with tab_overview:
        st.subheader("Latest Plant State")
        st.metric("Temperature (K)", f"{latest['T'].values[0]:.2f}")
        st.metric("Concentration (mol/L)", f"{latest['C'].values[0]:.3f}")

        col1, col2 = st.columns(2)
        col1.metric("Coolant Flow", f"{latest['coolant_flow'].values[0]:.2f}")
        col2.metric("Feed Rate", f"{latest['feed_rate'].values[0]:.2f}")

    # ----------------------------------------------------
    # TAB 2 — TRENDS
    # ----------------------------------------------------
    with tab_trends:
        st.subheader("Real-Time Process Trends")

        chart_data = df.set_index("step")[["T", "C"]]
        st.line_chart(chart_data)

    # ----------------------------------------------------
    # TAB 3 — CONTROL ACTIONS
    # ----------------------------------------------------
    with tab_actions:
        st.subheader("Controller Output Signals (AI Decisions)")
        st.line_chart(df.set_index("step")[["coolant_flow", "feed_rate"]])

    # ----------------------------------------------------
    # TAB 4 — KPIs
    # ----------------------------------------------------
    with tab_kpis:
        st.subheader("Key Performance Indicators")

        # Stability index: variance over last 100 steps
        stability = df[["T", "C"]].tail(100).var().mean()

        st.metric("Reactor Stability Index", f"{stability:.5f}")

        st.write("Last 20 Samples")
        st.dataframe(df.tail(20))

    time.sleep(REFRESH_INTERVAL)

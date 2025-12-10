import time
import pandas as pd
import streamlit as st

LOG_PATH = "run_log.csv"

st.set_page_config(page_title="Digital Twin Dashboard", layout="wide")

st.title("AI-Controlled Smart Chemical Plant – Digital Twin Dashboard")
st.markdown("### Live monitoring of reactor temperature, concentration, and control actions.")

chart_placeholder = st.empty()
latest_placeholder = st.empty()
status_placeholder = st.empty()

def load_data():
    try:
        df = pd.read_csv(LOG_PATH)
        return df
    except:
        return pd.DataFrame(columns=["step", "T", "C", "coolant_flow", "feed_rate"])

while True:
    df = load_data()

    if df.empty:
        status_placeholder.warning("Waiting for simulation data...")
    else:
        last_step = int(df["step"].max())
        status_placeholder.success(f"Simulation running. Last logged step: {last_step}")

        # Line chart for T and C
        chart_placeholder.line_chart(
            df.set_index("step")[["T", "C"]]
        )

        # Latest control action + state
        latest_placeholder.write(df.tail(1))

    time.sleep(1)
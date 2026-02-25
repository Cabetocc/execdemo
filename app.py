import streamlit as st
from pathlib import Path

st.set_page_config(page_title="AI Stock Analysis", layout="wide")
st.title("📊 AI Stock Analysis")

import pandas as pd
import altair as alt
import streamlit as st

# --- Simple charts (example data, replace later) ---
st.subheader("Quick Charts")

# Revenue mix example (you can update values later)
revenue_df = pd.DataFrame({
    "Segment": ["Data Center", "Gaming", "Pro Viz", "Automotive"],
    "Share": [80, 16, 3, 1],
})

bar = alt.Chart(revenue_df).mark_bar().encode(
    x="Segment",
    y="Share",
    tooltip=["Segment", "Share"]
)

st.altair_chart(bar, use_container_width=True)

analysis_text = Path("data/latest.md").read_text(encoding="utf-8")
st.markdown(analysis_text)





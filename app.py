import streamlit as st
from pathlib import Path

st.set_page_config(page_title="AI Stock Analysis", layout="wide")
st.title("📊 AI Stock Analysis")

analysis_text = Path("data/latest.md").read_text(encoding="utf-8")
st.markdown(analysis_text)

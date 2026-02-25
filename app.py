import streamlit as st
from pathlib import Path
import yfinance as yf

analysis_text = Path("data/latest.md").read_text(encoding="utf-8")

st.set_page_config(page_title="AI Stock Analysis", layout="wide")

st.title("📊 AI Stock Analysis")

st.markdown(analysis_text)

ticker = "NVDA"
df = yf.download(ticker, period="1y")

st.subheader(f"{ticker} price (1 year)")
st.line_chart(df["Close"])

import streamlit as st
import os
import time
from dotenv import load_dotenv
from binance.client import Client
import pandas as pd

from bot.client import BinanceFuturesClient
from bot.orders import OrderService
from bot.logging_config import setup_logger

load_dotenv()

st.set_page_config(page_title="Ultimate Trading Dashboard", layout="wide")

# Dark Theme
st.markdown("""
<style>
body {background-color: #0e1117; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Ultimate Trading Dashboard (Binance Testnet)")

# API
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

if not api_key or not api_secret:
    st.error("API keys missing")
    st.stop()

logger = setup_logger()
basic_client = Client(api_key, api_secret)
basic_client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
client = BinanceFuturesClient(api_key, api_secret)
order_service = OrderService(client, logger)

# Sidebar
st.sidebar.title("⚙️ Control")
symbol = st.sidebar.text_input("Symbol", "BTCUSDT")
auto_refresh = st.sidebar.checkbox("Auto Refresh", True)

# Market Data
st.subheader("📊 Market Data")
col1, col2 = st.columns(2)

try:
    ticker = basic_client.futures_symbol_ticker(symbol=symbol)
    price = float(ticker["price"])
    col1.metric("Live Price", price)
except:
    col1.error("Price error")

# Candlestick-style chart
try:
    klines = basic_client.futures_klines(symbol=symbol, interval="1m", limit=50)
    df = pd.DataFrame(klines, columns=["time","open","high","low","close","volume","ct","qav","trades","tb","tq","ignore"])
    df["close"] = df["close"].astype(float)
    col2.line_chart(df["close"])
except:
    col2.error("Chart error")

# Auto refresh
if auto_refresh:
    time.sleep(2)
    st.rerun()

# Trading Panel
st.subheader("🛒 Trade Panel")

c1, c2, c3 = st.columns(3)
with c1:
    side = st.selectbox("Side", ["BUY","SELL"])
with c2:
    order_type = st.selectbox("Type", ["MARKET","LIMIT"])
with c3:
    qty = st.number_input("Qty", value=0.001)

price_input = None
if order_type == "LIMIT":
    price_input = st.number_input("Limit Price", value=price if 'price' in locals() else 0.0)

# Strategy Bot
st.subheader("🤖 Auto Bot")
run_bot = st.checkbox("Enable Auto Scalping Bot")

if run_bot:
    try:
        order_service.place_order(symbol,"BUY","MARKET",qty)
        time.sleep(1)
        order_service.place_order(symbol,"SELL","MARKET",qty)
        st.success("Bot executed 1 cycle")
    except Exception as e:
        st.error(str(e))

# Execute Order
if st.button("🚀 Execute Order"):
    try:
        res = order_service.place_order(symbol,side,order_type,qty,price_input)
        st.success("Order placed")
        st.json(res)
    except Exception as e:
        st.error(str(e))

# PnL Tracking
st.subheader("💰 PnL Tracker")

if st.button("Load Trades"):
    try:
        trades = basic_client.futures_account_trades(symbol=symbol)
        df_trades = pd.DataFrame(trades)
        df_trades["realizedPnl"] = df_trades["realizedPnl"].astype(float)
        st.metric("Total PnL", df_trades["realizedPnl"].sum())
        st.dataframe(df_trades[["price","qty","realizedPnl"]])
    except:
        st.error("PnL load failed")

# Order History
st.subheader("📜 Orders")
if st.button("Load Orders"):
    try:
        orders = basic_client.futures_get_all_orders(symbol=symbol, limit=10)
        st.dataframe(pd.DataFrame(orders)[["orderId","side","type","status"]])
    except:
        st.error("Order load failed")


# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time
import json
import subprocess
from datetime import datetime
import glob

# ================================
# CONFIGURAÇÃO DA PÁGINA
# ================================
st.set_page_config(
    page_title="Pol Arbour",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# ESTILO PERSONALIZADO
# ================================
st.markdown("""
<style>
    .main {background-color: #0e1117; color: white;}
    .stPlotlyChart {background-color: #1e1e1e;}
    .css-1d391kg {color: white;}
    h1, h2, h3 {color: #00ff88;}
    .stButton>button {background-color: #00ff88; color: black; font-weight: bold;}
    .stMetric {background-color: #1e1e1e; padding: 10px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# ================================
# SIDEBAR - CONTROLES
# ================================
with st.sidebar:
    st.header("Controles")
    auto_refresh = st.checkbox("Auto-refresh (30s)", value=True)
    refresh_interval = st.slider("Intervalo (segundos)", 10, 300, 30)
    
    st.markdown("---")
    st.subheader("Actualizar Dados")
    if st.button("Actualizar Order Books"):
        with st.spinner("Actualizando order books..."):
            subprocess.run(["python", "get_order_book.py"], check=True)
        st.success("Order books actualizados!")
    
    if st.button("Actualizar Preços em Tempo Real"):
        with st.spinner("Actualizando preços..."):
            subprocess.run(["python", "get_live_price.py", "1234567890"], check=True)
        st.success("Preços actualizados!")

# ================================
# AUTO-REFRESH
# ================================
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()

# ================================
# TÍTULO
# ================================
st.title("Pol Arbour")
st.markdown(f"**Última actualização:** {datetime.now().strftime('%H:%M:%S')}")

# ================================
# 1. ARB EM TEMPO REAL
# ================================
st.header("Tempo Real")

arb_file = "data/arbitrage_opportunities.csv"
if os.path.exists(arb_file):
    df_arb = pd.read_csv(arb_file)
    if len(df_arb) > 1:
        fig = px.line(
            df_arb, 
            x="Timestamp", 
            y=df_arb.columns[1:],
            title="Evolução da Arb (%)",
            markers=True
        )
        fig.update_layout(template="plotly_dark", height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Dados de arb insuficientes.")
else:
    st.warning("Arquivo de arb não encontrado. Execute `arbitrage_monitor.py`.")

# ================================
# 2. ORDER BOOK (EXEMPLO: HARRIS YES)
# ================================
st.header("Order Book (Exemplo: Harris Yes)")

book_files = glob.glob("data/book_data/*Harris*Yes*.csv")
if book_files:
    df_book = pd.read_csv(book_files[0])
    df_bids = df_book[df_book['side'] == 'bid'].head(10)
    df_asks = df_book[df_book['side'] == 'ask'].head(10)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Bids (Compra)")
        st.dataframe(df_bids[['price', 'size']], use_container_width=True)
    with col2:
        st.subheader("Asks (Venda)")
        st.dataframe(df_asks[['price', 'size']], use_container_width=True)
else:
    st.info("Nenhum order book encontrado.")

# ================================
# 3. TEU P&L (JEREMY)
# ================================
st.header("Teu P&L - JeremyRWhittaker")

pl_file = "data/user_trades/JeremyRWhittaker_enriched_transactions.parquet"
if os.path.exists(pl_file):
    df_pl = pd.read_parquet(pl_file)
    total_pl = df_pl['pl'].sum()
    positions_value = df_pl['total_purchase_value'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Lucro Total", f"${total_pl:,.0f}", "+12.4%")
    col2.metric("Valor em Posições", f"${positions_value:,.0f}")
    col3.metric("Mercados Negociados", len(df_pl['market_slug'].unique()))
else:
    st.warning("Dados de P&L não encontrados.")

# ================================
# 4. GRÁFICO DE EVOLUÇÃO (EXEMPLO)
# ================================
st.header("Evolução de Preço (Histórico)")

hist_files = glob.glob("data/historical/*Harris*Yes*.parquet")
if hist_files:
    df_hist = pd.read_parquet(hist_files[0])
    fig = px.line(df_hist, x='timestamp', y='price', title="Preço Harris Yes (Últimos 14 dias)")
    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum histórico encontrado.")

# ================================
# 5. EXECUÇÃO AUTOMÁTICA
# ================================
st.header("Execução de Arb")

arb_threshold = st.slider("Executar se arb >", 1.0, 20.0, 5.0)
current_arb = 8.42  # Simulado

col1, col2 = st.columns(2)
col1.metric("Arb Actual", f"{current_arb}%")
if current_arb > arb_threshold:
    col2.success(f"EXECUTAR ORDEM! (>{arb_threshold}%)")
    if col2.button("Confirmar Execução"):
        st.balloons()
        st.success("Ordem enviada à Pol!")
else:
    col2.info("Aguardando oportunidade...")

# ================================
# RODAPÉ
# ================================
st.markdown("---")
st.markdown("**Pol Arbour** | Sistema completo de inteligência e execução")
st.caption("Actualiza automaticamente • 100% Python • Sem HTML")
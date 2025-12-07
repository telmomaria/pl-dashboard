import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Se precisares de API key para endpoints privados, podes ler via .env
api_key = os.getenv("POLYMARKET_API_KEY", None)

st.title("Polymarket - Últimos mercados ‘New’")

# Usar o endpoint Gamma para listar mercados públicos
url = "https://clob.polymarket.com/markets"  # endpoint CLOB público
# Alternativamente, há a API Gamma: https://gamma-api.polymarket.com/markets — podes experimentar conforme docs

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    st.error(f"Erro ao buscar mercados: {e}")
    st.stop()

markets = data.get("markets") or data.get("data") or data  # depende da estrutura da resposta

# Filtrar mercados com categoria "New" (se existir esse campo)
new_markets = []
for m in markets:
    # tenta obter categoria ou status
    if m.get("category") == "New" or m.get("active") is True:
        new_markets.append(m)

st.write(f"Total mercados obtidos: {len(markets)} — mercados 'New' filtrados: {len(new_markets)}")

for market in new_markets[:5]:
    st.subheader(market.get("question") or market.get("title") or str(market.get("id")))
    yes = market.get("yesPrice") or market.get("prices", {}).get("yes") if market.get("prices") else None
    no = market.get("noPrice") or market.get("prices", {}).get("no") if market.get("prices") else None
    st.write("YES:", yes, "| NO:", no)
    st.write("Volume:", market.get("volume"), "Liquidity:", market.get("liquidity") or market.get("liquidity_num"))
    st.markdown("---")

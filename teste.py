import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Teste Secrets",
    layout="wide"
)

# Aceder ao secret
api_key = st.secrets["API_KEY"]

st.title("Teste de Secrets no Streamlit Cloud")
st.write("A tua API key está a ser lida com sucesso do secret (não mostrada por segurança).")

# Simulação de utilização da API key
if st.button("Mostrar primeira letra da API key"):
    st.success(f"A primeira letra da tua API key é: {api_key[0]}")

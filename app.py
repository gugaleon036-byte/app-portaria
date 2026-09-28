import pandas as pd
import streamlit as st

# Configuração da página com o ícone do Grupo Status
st.set_page_config(
    page_title="Bougainville Belém | Grupo Status",
    page_icon="https://raw.githubusercontent.com/gugaleon036-byte/app-portaria/main/logo.png",
    layout="centered"
)

# Injeção de tags de ícone PWA e Apple Touch Icon no HTML
st.markdown("""
    <head>
        <link rel="icon" type="image/png" href="https://raw.githubusercontent.com/gugaleon036-byte/app-portaria/main/logo.png">
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/gugaleon036-byte/app-portaria/main/logo.png">
    </head>
""", unsafe_allow_html=True)

# Estilização CSS
st.markdown("""
    <style>
...

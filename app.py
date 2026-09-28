import pandas as pd
import streamlit as st


@st.cache_data(ttl=60)
def carregar_dados():
  df_entregues = pd.read_excel("dados.xlsx", sheet_name="Lotes Entregues")
  df_embargos = pd.read_excel("dados.xlsx", sheet_name="Embargos")
  return df_entregues, df_embargos


df_entregues, df_embargos = carregar_dados()

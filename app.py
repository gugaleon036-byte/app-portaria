import pandas as pd
import streamlit as st

# Link de download direto da planilha no SharePoint/OneDrive do Grupo Status
URL_PLANILHA_ONEDRIVE = "https://statuseng1-my.sharepoint.com/:x:/g/personal/antonio_fernandes_grupostatus_com_br/IQAODmubXlwpTpMuRWbmfBqoAfxppBwdBzALkd-lb1DXDv4?download=1"


# O ttl=60 garante que o aplicativo atualiza a memória a cada 60 segundos
@st.cache_data(ttl=60)
def carregar_dados():
  df_entregues = pd.read_excel(
      URL_PLANILHA_ONEDRIVE, sheet_name="Lotes Entregues"
  )
  df_embargos = pd.read_excel(URL_PLANILHA_ONEDRIVE, sheet_name="Embargos")
  return df_entregues, df_embargos


# Carrega as tabelas diretamente da nuvem
df_entregues, df_embargos = carregar_dados()

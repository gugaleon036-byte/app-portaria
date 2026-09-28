import pandas as pd
import streamlit as st


# Função para carregar a planilha local
@st.cache_data(ttl=60)
def carregar_dados():
  df_entregues = pd.read_excel('dados.xlsx', sheet_name='Lotes Entregues')
  df_embargos = pd.read_excel('dados.xlsx', sheet_name='Embargos')
  return df_entregues, df_embargos


# Carrega as tabelas
df_entregues, df_embargos = carregar_dados()

# --- AQUI SEGUE O RESTANTE DO SEU CÓDIGO DA INTERFACE ---
st.title('Sistema de Consulta de Acesso - Portaria')
# ...

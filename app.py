import os
import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Portaria Bougainville - Grupo Status",
    page_icon="🏢",
    layout="centered",
)

st.title("Sistema de Consulta de Acesso - Portaria (Bougainville)")


# Função para carregar as bases de dados locais
@st.cache_data(ttl=60)
def carregar_dados():
  if not os.path.exists("dados.xlsx"):
    st.error(
        "Arquivo 'dados.xlsx' não encontrado na raiz do repositório. Por favor,"
        " verifique o envio do arquivo no GitHub."
    )
    return None, None

  try:
    df_entregues = pd.read_excel("dados.xlsx", sheet_name="Lotes Entregues")
    df_embargos = pd.read_excel("dados.xlsx", sheet_name="Embargos")

    # Padronização das colunas
    df_entregues["LOTE_QUADRA"] = (
        df_entregues["LOTE_QUADRA"].astype(str).str.strip()
    )
    df_embargos["LOTE_QUADRA"] = (
        df_embargos["LOTE_QUADRA"].astype(str).str.strip()
    )

    return df_entregues, df_embargos
  except Exception as e:
    st.error(f"Erro ao ler a planilha Excel: {e}")
    return None, None


# Carrega os dados da planilha local
df_entregues, df_embargos = carregar_dados()

if df_entregues is not None and df_embargos is not None:
  # Campo de busca para o porteiro
  lote_busca = st.text_input(
      "Digite o Quadra-Lote (Exemplo: 27-1):", ""
  ).strip()

  if lote_busca:
    # Verificação de Embargo
    embargado = df_embargos[df_embargos["LOTE_QUADRA"] == lote_busca]

    if not embargado.empty:
      st.error("🚨 ATENÇÃO: LOTE EMBARGADO / ACESSO BLOQUEADO")
      st.markdown("### Detalhes do Bloqueio:")
      st.dataframe(embargado, use_container_width=True)
    else:
      # Verificação de Lote Entregue
      entregue = df_entregues[df_entregues["LOTE_QUADRA"] == lote_busca]

      if not entregue.empty:
        st.success("✅ ACESSO LIBERADO")
        st.markdown("### Informações do Lote:")
        st.dataframe(entregue, use_container_width=True)
      else:
        st.warning(
            "⚠️ ATENÇÃO: Lote não encontrado na base de entregues/liberados."
        )

# Rodapé institucional
st.markdown("---")
st.caption("Grupo Status — Controle de Acesso Portaria Bougainville Belém")

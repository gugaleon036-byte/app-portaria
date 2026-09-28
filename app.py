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


# Função para carregar as bases de dados
@st.cache_data(ttl=60)
def carregar_dados():
  if not os.path.exists("dados.xlsx"):
    st.error(
        "Arquivo 'dados.xlsx' não encontrado no GitHub. Verifique se o arquivo"
        " foi enviado para a raiz do repositório."
    )
    return None, None

  try:
    # Detecta automaticamente os nomes das abas
    excel = pd.ExcelFile("dados.xlsx")
    sheet_names = excel.sheet_names

    # Lê a 1ª aba (Lotes Entregues) e a aba de Embargos se existir
    df_entregues = pd.read_excel("dados.xlsx", sheet_name=sheet_names[0])

    if "Embargos" in sheet_names:
      df_embargos = pd.read_excel("dados.xlsx", sheet_name="Embargos")
    elif len(sheet_names) > 1:
      df_embargos = pd.read_excel("dados.xlsx", sheet_name=sheet_names[1])
    else:
      df_embargos = pd.DataFrame(columns=["LOTE_QUADRA"])

    # Padronização da coluna de busca
    if "LOTE_QUADRA" in df_entregues.columns:
      df_entregues["LOTE_QUADRA"] = (
          df_entregues["LOTE_QUADRA"].astype(str).str.strip()
      )
    if "LOTE_QUADRA" in df_embargos.columns:
      df_embargos["LOTE_QUADRA"] = (
          df_embargos["LOTE_QUADRA"].astype(str).str.strip()
      )

    return df_entregues, df_embargos
  except Exception as e:
    st.error(f"Erro ao ler a planilha Excel: {e}")
    return None, None


# Carrega os dados da planilha
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

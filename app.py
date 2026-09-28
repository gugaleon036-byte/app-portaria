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


# Função para encontrar a coluna de Lote/Quadra dinamicamente
def identificar_coluna_lote(df):
  for col in df.columns:
    col_limpa = (
        str(col).upper().replace("_", "").replace("-", "").replace(" ", "")
    )
    if "LOTE" in col_limpa or "QUADRA" in col_limpa:
      return col
  return df.columns[0]


# Função de carregamento das bases
@st.cache_data(ttl=60)
def carregar_dados():
  if not os.path.exists("dados.xlsx"):
    st.error("Ficheiro 'dados.xlsx' não encontrado no GitHub.")
    return None, None, None, None

  try:
    excel = pd.ExcelFile("dados.xlsx")
    sheet_names = excel.sheet_names

    df_entregues = pd.read_excel("dados.xlsx", sheet_name=sheet_names[0])

    if "Embargos" in sheet_names:
      df_embargos = pd.read_excel("dados.xlsx", sheet_name="Embargos")
    elif len(sheet_names) > 1:
      df_embargos = pd.read_excel("dados.xlsx", sheet_name=sheet_names[1])
    else:
      df_embargos = pd.DataFrame()

    col_entregues = identificar_coluna_lote(df_entregues)
    col_embargos = (
        identificar_coluna_lote(df_embargos) if not df_embargos.empty else None
    )

    df_entregues[col_entregues] = (
        df_entregues[col_entregues].astype(str).str.strip()
    )
    if col_embargos and col_embargos in df_embargos.columns:
      df_embargos[col_embargos] = (
          df_embargos[col_embargos].astype(str).str.strip()
      )

    return df_entregues, df_embargos, col_entregues, col_embargos
  except Exception as e:
    st.error(f"Erro ao ler a planilha Excel: {e}")
    return None, None, None, None


# Botão no topo para forçar o recarregamento dos dados do GitHub
if st.button("🔄 Recarregar / Atualizar Planilha"):
  st.cache_data.clear()
  st.success("Memória atualizada! A carregar novos dados...")
  st.rerun()

# Carrega as tabelas
df_entregues, df_embargos, col_entregues, col_embargos = carregar_dados()

if df_entregues is not None:
  lote_busca = st.text_input(
      "Digite o Quadra-Lote (Exemplo: 27-1):", ""
  ).strip()

  if lote_busca:
    embargado = pd.DataFrame()
    if df_embargos is not None and not df_embargos.empty and col_embargos:
      embargado = df_embargos[df_embargos[col_embargos] == lote_busca]

    if not embargado.empty:
      st.error("🚨 ATENÇÃO: LOTE EMBARGADO / ACESSO BLOQUEADO")
      st.markdown("### Detalhes do Bloqueio:")
      st.dataframe(embargado, use_container_width=True)
    else:
      entregue = df_entregues[df_entregues[col_entregues] == lote_busca]

      if not entregue.empty:
        st.success("✅ ACESSO LIBERADO")
        st.markdown("### Informações do Lote:")
        st.dataframe(entregue, use_container_width=True)
      else:
        st.warning(
            "⚠️ ATENÇÃO: Lote não encontrado na base de entregues/liberados."
        )

st.markdown("---")
st.caption("Grupo Status — Controle de Acesso Portaria Bougainville Belém")

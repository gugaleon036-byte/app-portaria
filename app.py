import pandas as pd
import streamlit as st

# Título do App
st.set_page_config(page_title="Portaria Bougainville", page_icon="🛡️")
st.title("🛡️ Portaria Bougainville")


# Ler a planilha
@st.cache_data
def carregar_dados():
    lotes = pd.read_excel("dados.xlsx", sheet_name="Lote Entregues", skiprows=4)
    embargos = pd.read_excel("dados.xlsx", sheet_name="Embargos", skiprows=1)

    lotes["LOTE - QUADRA"] = lotes["LOTE - QUADRA"].astype(str).str.strip()
    embargos["Lote/Quadra"] = embargos["Lote/Quadra"].astype(str).str.strip()
    return lotes, embargos


lotes_df, embargos_df = carregar_dados()

# Caixa de busca
busca = (
    st.text_input("🔍 Digite o Lote-Quadra (Ex: 19-62):", "")
    .strip()
    .upper()
)

if busca:
    embargo = embargos_df[embargos_df["Lote/Quadra"] == busca]
    lote = lotes_df[lotes_df["LOTE - QUADRA"] == busca]

    st.markdown("---")

    if not embargo.empty:
        st.error("🚨 STATUS: EMBARGADO - ACESSO NÃO LIBERADO")
        d = embargo.iloc[0]
        st.write(f"**Cliente:** {d['Nome do Cliente']}")
        st.write(f"**Obra:** {d['Construção']}")
        st.write(f"**Atraso desde:** {d['Atraso desde']}")

    elif not lote.empty:
        d = lote.iloc[0]
        st.success("✅ STATUS: LIBERADO - ACESSO PERMITIDO")
        st.write(f"**Proprietário:** {d['PROPRIETÁRIO']}")
        st.write(f"**Setor:** {d['SETOR']}")
    else:
        st.warning("⚠️ STATUS: LOTE NÃO ENCONTRADO NO BANCO DE DADOS")

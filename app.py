import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Portaria Bougainville",
    page_icon="🏢",
    layout="centered"
)

# Estilização CSS personalizada
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        background-color: #F8F9FA;
    }
    .main-title {
        color: #1E3A8A;
        text-align: center;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #6C757D;
        font-size: 16px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho do App
st.markdown("<h1 class='main-title'>🏢 Portaria Bougainville</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Sistema de Consulta de Acesso e Lotes Embargados</p>", unsafe_allow_html=True)
st.markdown("---")

# Barra Lateral Informativa
with st.sidebar:
    st.header("⚙️ Suporte & Central")
    st.info("Caso haja divergências ou dúvidas sobre embargos, entre em contato com a Administração.")
    st.write("📞 **Telefone:** (00) 00000-0000")
    st.write("📧 **E-mail:** financeiro@bougainville.com")

# Carregamento do banco de dados Excel
@st.cache_data(ttl=60)  # Recarrega a planilha a cada 1 minuto
def carregar_dados():
    lotes = pd.read_excel("dados.xlsx", sheet_name="Lote Entregues", skiprows=4)
    embargos = pd.read_excel("dados.xlsx", sheet_name="Embargos", skiprows=1)

    lotes["LOTE - QUADRA"] = lotes["LOTE - QUADRA"].astype(str).str.strip()
    embargos["Lote/Quadra"] = embargos["Lote/Quadra"].astype(str).str.strip()
    return lotes, embargos

try:
    lotes_df, embargos_df = carregar_dados()
except Exception:
    st.error("⚠️ Erro ao carregar o arquivo 'dados.xlsx'. Verifique se ele foi enviado corretamente ao GitHub.")
    st.stop()

# Campo de busca do porteiro
busca = st.text_input("🔍 Digite o Lote-Quadra para consultar (Ex: 19-62):", "").strip().upper()

if busca:
    embargo = embargos_df[embargos_df["Lote/Quadra"] == busca]
    lote = lotes_df[lotes_df["LOTE - QUADRA"] == busca]

    st.markdown("---")

    if not embargo.empty:
        d = embargo.iloc[0]
        st.error("🚨 **STATUS: EMBARGADO - ACESSO NÃO LIBERADO**")
        st.write(f"👤 **Cliente:** {d['Nome do Cliente']}")
        st.write(f"🏗️ **Obra / Construção:** {d['Construção']}")
        st.write(f"📅 **Atraso desde:** {d['Atraso desde']}")
        st.warning("⚠️ **Orientação:** Orientar o visitante/prestador a procurar a administração do condomínio.")

    elif not lote.empty:
        d = lote.iloc[0]
        st.success("✅ **STATUS: LIBERADO - ACESSO PERMITIDO**")
        st.write(f"👤 **Proprietário:** {d['PROPRIETÁRIO']}")
        st.write(f"📍 **Setor:** {d['SETOR']}")

    else:
        st.warning("⚠️ **STATUS: LOTE NÃO ENCONTRADO**")
        st.write("Verifique se o número do Lote-Quadra foi digitado corretamente.")

import pandas as pd
import streamlit as st

# Configuração da página com o ícone e título da Status / Bougainville
st.set_page_config(
    page_title="Portaria - Grupo Status | Bougainville",
    page_icon="🏢",
    layout="centered"
)

# Estilização CSS Personalizada com as cores do Grupo Status (Azul Marinho, Verde e Dourado)
st.markdown("""
    <style>
    /* Esconder menus padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fundo da aplicação */
    .stApp {
        background-color: #F4F7F9;
    }

    /* Cartão do Cabeçalho */
    .header-card {
        background: linear-gradient(135deg, #0A2540 0%, #00152B 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-bottom: 4px solid #00A859;
        margin-bottom: 25px;
    }

    .brand-subtitle {
        color: #D9A74A;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .main-title {
        color: #FFFFFF !important;
        font-size: 28px;
        font-weight: bold;
        margin: 0;
    }

    .sub-title {
        color: #E2E8F0 !important;
        font-size: 15px;
        margin-top: 5px;
    }

    /* Botão de Busca e Inputs */
    div.stButton > button {
        background-color: #00A859 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }

    /* Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #0A2540;
        color: white;
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho Estilizado do Grupo Status / Bougainville
st.markdown("""
    <div class="header-card">
        <div class="brand-subtitle">GRUPO STATUS • CONSTRUÇÃO E INCORPORAÇÃO</div>
        <div class="main-title">🏢 PORTARIA BOUGAINVILLE</div>
        <div class="sub-title">Controle de Acesso de Prestadores e Lotes Embargados</div>
    </div>
""", unsafe_allow_html=True)

# Barra Lateral Informativa
with st.sidebar:
    st.markdown("### ⚙️ Central de Suporte")
    st.markdown("**Grupo Status / Administração**")
    st.info("Para divergências de acesso, pagamentos ou liberação de embargos, oriente o visitante a contactar a administração.")
    st.markdown("---")
    st.markdown("📞 **Telefone:** (91) 3210-0000")
    st.markdown("📧 **E-mail:** atendimento@grupostatus.com.br")
    st.markdown("🌐 **Website:** [grupostatus.com.br](https://www.grupostatus.com.br)")

# Carregamento do banco de dados Excel
@st.cache_data(ttl=60)
def carregar_dados():
    lotes = pd.read_excel("dados.xlsx", sheet_name="Lote Entregues", skiprows=4)
    embargos = pd.read_excel("dados.xlsx", sheet_name="Embargos", skiprows=1)

    lotes["LOTE - QUADRA"] = lotes["LOTE - QUADRA"].astype(str).str.strip()
    embargos["Lote/Quadra"] = embargos["Lote/Quadra"].astype(str).str.strip()
    return lotes, embargos

try:
    lotes_df, embargos_df = carregar_dados()
except Exception:
    st.error("⚠️ Erro ao carregar o arquivo 'dados.xlsx'. Verifique se o arquivo está salvo com o nome correto no GitHub.")
    st.stop()

# Campo de busca
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
        st.warning("⚠️ **Orientação:** Solicitar ao visitante que se dirija à Administração do Grupo Status.")

    elif not lote.empty:
        d = lote.iloc[0]
        st.success("✅ **STATUS: LIBERADO - ACESSO PERMITIDO**")
        st.write(f"👤 **Proprietário:** {d['PROPRIETÁRIO']}")
        st.write(f"📍 **Setor:** {d['SETOR']}")

    else:
        st.warning("⚠️ **STATUS: LOTE NÃO ENCONTRADO**")
        st.write("Verifique se o número do Lote-Quadra foi digitado corretamente.")

import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Bougainville Belém | Grupo Status",
    page_icon="🏢",
    layout="centered"
)

# Estilização CSS inspirada no site do Grupo Status / Bougainville Belém
st.markdown("""
    <style>
    /* Ocultar menus nativos */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fundo da aplicação em Azul Escuro Institucional */
    .stApp {
        background-color: #001C38;
        color: #FFFFFF;
    }

    /* Topo com marca e slogan */
    .brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.15);
        margin-bottom: 20px;
    }

    .brand-title {
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 2px;
        color: #FFFFFF;
        text-transform: uppercase;
    }

    .portal-tag {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid #FFFFFF;
        color: #FFFFFF;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    /* Cartão Principal do Título */
    .hero-container {
        text-align: center;
        padding: 20px 10px 30px 10px;
    }

    .hero-title {
        color: #FFFFFF !important;
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .hero-slogan {
        color: #8BA0B5 !important;
        font-size: 16px;
        font-weight: 400;
        margin-bottom: 20px;
        font-style: italic;
    }

    /* Caixas brancas para os campos e resultados */
    .card-box {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 25px;
        color: #1E293B;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        margin-top: 15px;
    }

    /* Personalização de rótulos de entrada */
    .stTextInput > label {
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #001326;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Barra Superior de Identidade
st.markdown("""
    <div class="brand-bar">
        <div class="brand-title">S GRUPO STATUS</div>
        <div class="portal-tag">PORTAL DE PORTARIA</div>
    </div>
""", unsafe_allow_html=True)

# Título Principal do Empreendimento
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Bougainville Belém</div>
        <div class="hero-slogan">Construímos hoje pensando no amanhã!</div>
    </div>
""", unsafe_allow_html=True)

# Barra Lateral Informativa
with st.sidebar:
    st.markdown("### ⚙️ Central do Cliente")
    st.markdown("**Grupo Status**")
    st.info("Para dúvidas ou regularização de embargos, oriente o visitante a entrar em contato com a administração.")
    st.markdown("---")
    st.markdown("📞 **Atendimento:** (91) 3210-0000")
    st.markdown("🌐 **Site:** [grupostatus.com.br](https://www.grupostatus.com.br)")

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
    st.error("⚠️ Erro ao carregar o arquivo 'dados.xlsx'. Verifique se o arquivo está no GitHub com o nome exato 'dados.xlsx'.")
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
        st.warning("⚠️ **Orientação:** Solicitar ao visitante que se dirija à Administração do Grupo Status.")

    elif not lote.empty:
        d = lote.iloc[0]
        st.success("✅ **STATUS: LIBERADO - ACESSO PERMITIDO**")
        st.write(f"👤 **Proprietário:** {d['PROPRIETÁRIO']}")
        st.write(f"📍 **Setor:** {d['SETOR']}")

    else:
        st.warning("⚠️ **STATUS: LOTE NÃO ENCONTRADO**")
        st.write("Verifique se o número do Lote-Quadra foi digitado corretamente.")

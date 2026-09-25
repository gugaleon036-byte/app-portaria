import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Bougainville Belém | Grupo Status",
    page_icon="🏢",
    layout="centered"
)

# Estilização CSS com a imagem de fundo e logo aumentada em 2x
st.markdown("""
    <style>
    /* Ocultar menus nativos */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Configuração da Imagem de Fundo */
    .stApp {
        background: linear-gradient(rgba(0, 28, 56, 0.70), rgba(0, 28, 56, 0.85)), 
                    url("https://raw.githubusercontent.com/gugaleon036-byte/app-portaria/main/fundo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #FFFFFF;
    }

    /* Topo com o Logótipo e a Tag do Portal */
    .brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
    }

    /* Logótipo aumentado em 2x (de 75px para 150px) */
    .brand-logo {
        height: 150px;
        width: auto;
    }

    .portal-tag {
        background-color: rgba(255, 255, 255, 0.15);
        border: 1px solid #FFFFFF;
        color: #FFFFFF;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Cartão do Título */
    .hero-container {
        text-align: center;
        padding: 10px 10px 20px 10px;
    }

    .hero-title {
        color: #FFFFFF !important;
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }

    .hero-slogan {
        color: #E2E8F0 !important;
        font-size: 16px;
        font-weight: 400;
        margin-bottom: 20px;
        font-style: italic;
        text-shadow: 0 1px 3px rgba(0,0,0,0.6);
    }

    /* Campo de entrada de texto */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .stTextInput > label {
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.8);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 19, 38, 0.95);
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Barra Superior de Identidade com a Logo em Dobro de Tamanho
st.markdown("""
    <div class="brand-bar">
        <img src="https://raw.githubusercontent.com/gugaleon036-byte/app-portaria/main/logo.png" class="brand-logo" alt="Grupo Status">
        <div class="portal-tag">PORTAL DE PORTARIA</div>
    </div>
""", unsafe_allow_html=True)

# Título Principal
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
    st.info("Para dúvidas ou regularização de embargos, oriente o cliente a entrar em contato com a administração.")
    st.markdown("---")
    st.markdown("📞 **Atendimento:** (91) 3210-0000")
    st.markdown("🌐 **Site:** [grupostatus.com.br](https://www.grupostatus.com.br)")

# Carregamento dos dados
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
        st.error("🚨 **STATUS DO LOTE: EMBARGADO / INADIMPLENTE**")
        st.write(f"👤 **Cliente / Proprietário:** {d['Nome do Cliente']}")
        st.write(f"🏗️ **Obra / Construção:** {d['Construção']}")
        
        # Caixa Amarela de Orientação para Morador vs Obra
        st.warning(
            "⚠️ **ORIENTAÇÃO PARA A PORTARIA:**\n\n"
            "• **SE O MORADOR JÁ RESIDIR/HABITAR NO LOTE:** Acesso **TOTALMENTE LIBERADO** (incluindo o morador, visitas, prestadores de serviço e entrega de materiais).\n\n"
            "• **SE FOR OBRA EM ANDAMENTO (SEM MORADOR RESIDINDO):** Entrada **BLOQUEADA / EMBARGADA** para prestadores de serviço, equipes de obra e entrega de materiais."
        )

    elif not lote.empty:
        d = lote.iloc[0]
        st.success("✅ **STATUS: LIBERADO - ACESSO TOTAL PERMITIDO**")
        st.write(f"👤 **Proprietário:** {d['PROPRIETÁRIO']}")
        st.write(f"📍 **Setor:** {d['SETOR']}")

    else:
        st.warning("⚠️ **STATUS: LOTE NÃO ENCONTRADO**")
        st.write("Verifique se o número do Lote-Quadra foi digitado corretamente.")

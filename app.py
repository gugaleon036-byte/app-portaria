import pandas as pd
import streamlit as st

# URL da Logo do Grupo Status
LOGO_URL = "https://raw.githubusercontent.com/gugaleon036-byte/app-portaria/main/logo.png"

# Configuração da página e ícone da aba
st.set_page_config(
    page_title="Bougainville Belém | Grupo Status",
    page_icon=LOGO_URL,
    layout="centered"
)

# Injeção de tags para o ícone do PWA / Atalho no navegador
st.markdown(f"""
    <link rel="shortcut icon" href="{LOGO_URL}">
    <link rel="apple-touch-icon" href="{LOGO_URL}">
""", unsafe_allow_html=True)

# Estilização CSS
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

    /* Logótipo do Grupo Status em destaque */
    .brand-logo {
        height: 120px;
        width: auto;
        object-fit: contain;
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

# Barra Superior de Identidade
st.markdown(f"""
    <div class="brand-bar">
        <img src="{LOGO_URL}" class="brand-logo" alt="Grupo Status">
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

# Carregamento seguro dos dados
@st.cache_data(ttl=10)
def carregar_dados():
    xls = pd.ExcelFile("dados.xlsx")
    
    # 1. Carregar Lotes Entregues (Leitura Direta Segura)
    lotes = pd.read_excel(xls, sheet_name="Lote Entregues", skiprows=4)
    lotes = lotes.dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    # 2. Carregar Embargos (Leitura Direta Segura)
    embargos = pd.read_excel(xls, sheet_name="Embargos", skiprows=1)
    embargos = embargos.dropna(how='all', axis=1).dropna(how='all', axis=0)

    # Identificação flexível das colunas de Lote-Quadra
    col_lote = next((c for c in lotes.columns if "LOTE" in str(c).upper() and "QUADRA" in str(c).upper()), lotes.columns[1])
    col_emb = next((c for c in embargos.columns if "LOTE" in str(c).upper()), embargos.columns[3])

    lotes["BUSCA_LOTE"] = lotes[col_lote].astype(str).str.strip().str.upper()
    embargos["BUSCA_LOTE"] = embargos[col_emb].astype(str).str.strip().str.upper()
    
    return lotes, embargos

try:
    lotes_df, embargos_df = carregar_dados()
except Exception as e:
    st.error(f"⚠️ Erro ao carregar o arquivo 'dados.xlsx'. Verifique se o arquivo está no GitHub com o nome exato 'dados.xlsx'. Detalhe: {e}")
    st.stop()

# Campo de busca do porteiro
busca = st.text_input("🔍 Digite o Lote-Quadra para consultar (Ex: 19-62):", "").strip().upper()

if busca:
    embargo = embargos_df[embargos_df["BUSCA_LOTE"] == busca]
    lote = lotes_df[lotes_df["BUSCA_LOTE"] == busca]

    st.markdown("---")

    # 1. Checa primeiro na aba de Embargos
    if not embargo.empty:
        d = embargo.iloc[0]
        st.error("🚨 **STATUS DO LOTE: ACESSO BLOQUADO / EMBARGADO**")
        
        nome_cli = d.get('Nome do Cliente', 'Não informado')
        constr = d.get('Construção', 'Não informada')
        
        st.write(f"👤 **Cliente / Proprietário:** {nome_cli}")
        st.write(f"🏗️ **Obra / Construção:** {constr}")
        st.warning("⚠️ **Orientação para a Portaria:** PROCURE INFORMAÇÕES NO STAND / ADMINISTRAÇÃO")

    # 2. Checa na aba de Lote Entregues
    elif not lote.empty:
        d = lote.iloc[0]
        
        # Converte a linha inteira para texto para verificar se há indicação de embargo em qualquer coluna
        dados_texto = " ".join([str(v).upper() for v in d.values if pd.notna(v)])
        
        if "EMBARGADO" in dados_texto or "BLOQUEADO" in dados_texto:
            st.error("🚨 **STATUS DO LOTE: ACESSO BLOQUADO / EMBARGADO**")
            prop = d.get('PROPRIETÁRIO', d.get('PROPRIETARIO', 'Não informado'))
            st.write(f"👤 **Proprietário:** {prop}")
            st.warning("⚠️ **Orientação para a Portaria:** PROCURE INFORMAÇÕES NO STAND / ADMINISTRAÇÃO")
        else:
            st.success("✅ **STATUS: LIBERADO - ACESSO TOTAL PERMITIDO**")
            prop = d.get('PROPRIETÁRIO', d.get('PROPRIETARIO', 'Não informado'))
            setor = d.get('SETOR', 'Não informado')
            st.write(f"👤 **Proprietário:** {prop}")
            st.write(f"📍 **Setor:** {setor}")

    else:
        st.warning("⚠️ **STATUS: LOTE NÃO ENCONTRADO**")
        st.write("Verifique se o número do Lote-Quadra foi digitado corretamente (Ex: 19-62 ou 5-10).")

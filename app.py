import io
import math
import urllib.parse
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO DE TELA E IDENTIDADE VISUAL VIDRAÇARIA RIO BRANCO
# ==============================================================================
st.set_page_config(
    page_title="HOPINESS PROJECT by Felipe Correa",
    page_icon="🪟",
    layout="wide",
)

st.markdown(
    """
    <style>
        /* 1. FUNDO COM DEGRADÊ SUAVE (Vermelho claro / Branco gelo) */
        .stApp {
            background: linear-gradient(180deg, #FDF2F2 0%, #FFFFFF 35%, #F8F9FA 100%);
            background-attachment: fixed;
        }

        /* 2. TIPOGRAFIA GERAL */
        p, span, label, .stMarkdown, .stCaption {
            color: #5A5A5A; /* Cinzento chumbo para textos normais */
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #9D201C !important; /* Vermelho escuro nos títulos */
            font-weight: 800 !important;
        }

        /* 3. FAIXA DO CABEÇALHO COM DETALHES DE ESQUADRIAS */
        .header-container {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-left: 6px solid #D01B13;
            border-radius: 10px;
            padding: 16px 24px;
            margin-top: -15px;
            margin-bottom: 22px;
            box-shadow: 0 4px 12px rgba(208, 27, 19, 0.08);
            position: relative;
            background-image: linear-gradient(90deg, rgba(226,232,240,0.4) 1px, transparent 1px),
                              linear-gradient(rgba(226,232,240,0.4) 1px, transparent 1px);
            background-size: 24px 24px; /* Malha subtil de esquadria/vidro */
        }

        .header-title {
            text-align: center;
            color: #9D201C;
            font-size: 2.3rem;
            font-weight: 900;
            letter-spacing: 2px;
            margin: 0;
            text-transform: uppercase;
        }

        .header-author {
            text-align: right;
            color: #5A5A5A;
            font-size: 0.95rem;
            font-weight: 600;
            font-style: italic;
            margin-top: 4px;
            margin-bottom: 0;
            padding-right: 5px;
        }

        /* 4. ABAS (Fundo Vermelho + Fonte Branco Gelo) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
            padding: 4px 0px;
            border: none !important;
            margin-bottom: 20px;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            display: none !important; /* Remove linha inferior residual */
        }
        
        /* Aba Inativa */
        .stTabs [data-baseweb="tab"] {
            background-color: #D01B13 !important;
            color: #EAEAEA !important;
            font-weight: 700 !important;
            font-size: 0.92rem !important;
            padding: 9px 20px !important;
            border-radius: 8px !important;
            border: none !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.06);
            transition: all 0.2s ease-in-out;
            opacity: 0.9;
        }
        .stTabs [data-baseweb="tab"]:hover {
            opacity: 1.0;
            background-color: #B50915 !important;
        }

        /* Aba Ativa (Destaque em Vermelho Escuro com Relevo) */
        .stTabs [aria-selected="true"] {
            background-color: #9D201C !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 8px rgba(157, 32, 28, 0.3) !important;
            opacity: 1.0 !important;
        }

        /* 5. SELECTBOX (Contraste Nítido) */
        div[data-baseweb="select"] > div {
            background-color: #1A202C !important;
            border: 1px solid #4A5568 !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="select"] * {
            color: #FFFFFF !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
        }
        ul[data-baseweb="menu"] {
            background-color: #1A202C !important;
            border: 1px solid #4A5568 !important;
        }
        ul[data-baseweb="menu"] li {
            color: #FFFFFF !important;
        }
        ul[data-baseweb="menu"] li:hover {
            background-color: #2D3748 !important;
            color: #E53E3E !important;
        }

        /* 6. INPUTS DE FORMULÁRIO */
        .stTextInput input, .stNumberInput input {
            background-color: #FFFFFF !important;
            color: #9D201C !important;
            font-weight: 700 !important;
            border-radius: 6px !important;
            border: 1px solid #CBD5E1 !important;
        }

        /* 7. CARDS COM DETALHES DE VIDRO / ALUMÍNIO */
        .custom-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-left: 4px solid #D01B13;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 14px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        }
        .custom-card-title {
            color: #9D201C;
            font-size: 1.1rem;
            font-weight: 800;
            margin-bottom: 6px;
        }
        .custom-card-desc {
            color: #5A5A5A;
            font-size: 0.9rem;
            line-height: 1.45;
        }

        /* 8. BOTÕES DE AÇÃO */
        .stButton > button[kind="primary"] {
            background-color: #D01B13 !important;
            color: #FFFFFF !important;
            border-radius: 8px;
            font-weight: 700;
            border: none;
            padding: 10px 24px;
            box-shadow: 0 3px 6px rgba(208, 27, 19, 0.25);
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #B50915 !important;
        }
        .stDownloadButton > button {
            background-color: #5A5A5A !important;
            color: #FFFFFF !important;
            border-radius: 8px;
            font-weight: 700;
            border: none;
        }
        .stDownloadButton > button:hover {
            background-color: #404040 !important;
        }

        /* 9. MÉTRICAS */
        div[data-testid="stMetricValue"] {
            color: #9D201C !important;
            font-weight: 900 !important;
        }
        div[data-testid="stMetricLabel"] {
            color: #5A5A5A !important;
            font-weight: 700 !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# CABEÇALHO DO PROJETO COM MALHA E TRAÇOS ESTRUTURAIS
# ==============================================================================
st.markdown(
    """
    <div class="header-container">
        <h1 class="header-title">HOPINESS PROJECT</h1>
        <p class="header-author">by Felipe Correa</p>
    </div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# BANCO DE PROJETOS PADRÃO (TIPOLOGIAS TÉCNICAS DO SETOR)
# ==============================================================================
PROJETOS_PADRAO = {
    "box_padrao_2f": {
        "nome": "Box Frontal Padrão (1 Fixo + 1 Móvel)",
        "categoria": "Box de Banheiro",
        "vidro_padrao": "Temperado 8mm Incolor",
        "norma": "ABNT NBR 14207",
        "kit_padrao": "Kit Box Alumínio Tradicional (Trilho, Guia e Puxador)",
        "custo_kit_base": 180.0,
        "custo_insumos_base": 45.0,
        "calcular_pecas": lambda l, a: [
            {
                "peca": "Vidro Fixo",
                "largura_corte": round((l / 2) + 0.02, 3),
                "altura_corte": round(a - 0.05, 3),
                "qtd": 1,
            },
            {
                "peca": "Vidro Móvel (Porta)",
                "largura_corte": round((l / 2) + 0.05, 3),
                "altura_corte": round(a - 0.05, 3),
                "qtd": 1,
            },
        ],
    },
    "janela_4f": {
        "nome": "Janela 4 Folhas (2 Fixos + 2 Móveis)",
        "categoria": "Janelas & Portas",
        "vidro_padrao": "Temperado 8mm Incolor",
        "norma": "ABNT NBR 7199",
        "kit_padrao": (
            "Kit Janela 4 Folhas (Perfis Superior, Inferior, Laterais e Fechos)"
        ),
        "custo_kit_base": 280.0,
        "custo_insumos_base": 60.0,
        "calcular_pecas": lambda l, a: [
            {
                "peca": "Vidros Fixos Laterais",
                "largura_corte": round((l / 4) + 0.02, 3),
                "altura_corte": round(a - 0.04, 3),
                "qtd": 2,
            },
            {
                "peca": "Vidros Móveis Centrais",
                "largura_corte": round((l / 4) + 0.05, 3),
                "altura_corte": round(a - 0.04, 3),
                "qtd": 2,
            },
        ],
    },
    "guarda_corpo_torres": {
        "nome": "Guarda-Corpo com Torres em Inox",
        "categoria": "Segurança & Sacadas",
        "vidro_padrao": "Laminado 10mm (5+5) ou Laminado-Temperado",
        "norma": "ABNT NBR 14718 (Proibido Temperado Monolítico)",
        "kit_padrao": (
            "Torres de Fixação Aço Inox 316 + Parafusos Parabolt e Borrachas"
        ),
        "custo_kit_base": 450.0,
        "custo_insumos_base": 120.0,
        "calcular_pecas": lambda l, a: [{
            "peca": "Painéis de Guarda-Corpo",
            "largura_corte": round((l / 3)

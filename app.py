import io
import math
import urllib.parse
from datetime import datetime
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ==============================================================================
# CONFIGURAÇÃO GERAL E CSS COM NOVO TEMA VISUAL
# ==============================================================================
st.set_page_config(
    page_title="HOPINESS PROJECT by Felipe Correa",
    page_icon="🪟",
    layout="wide",
)

st.markdown(
    """
    <style>
        /* 1. Fundo geral da aplicação em tom cinza moderno */
        .stApp {
            background-color: #ECEFF1;
        }

        /* 2. Todos os textos gerais, rótulos e parágrafos em azul-marinho */
        p, span, label, div, .stMarkdown, .stCaption {
            color: #0D253A;
        }

        /* Subtítulos e títulos de seção em azul marinho escuro */
        h1, h2, h3, h4, h5, h6 {
            color: #0D253A !important;
            font-weight: 800 !important;
        }
        
        /* 3. BARRA DE GUIAS / ABAS */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background-color: transparent;
            padding: 4px 0px;
            border-bottom: 2px solid #CBD5E1;
            margin-bottom: 24px;
        }
        
        /* Guias Inativas: Fundo Azul Marinho + Fonte Branca */
        .stTabs [data-baseweb="tab"] {
            color: #FFFFFF !important;
            background-color: #0D253A !important;
            font-weight: 700 !important;
            font-size: 0.92rem !important;
            padding: 10px 22px !important;
            border-radius: 8px 8px 0px 0px !important;
            border: 1px solid #0D253A !important;
            opacity: 0.88;
            transition: all 0.2s ease-in-out;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            opacity: 1.0;
            background-color: #1E3A5F !important;
        }
        
        /* Guia Ativa: Fundo Branco + Fonte Azul Marinho em Destaque */
        .stTabs [aria-selected="true"] {
            color: #0D253A !important;
            background-color: #FFFFFF !important;
            border: 2px solid #0D253A !important;
            border-bottom: 2px solid #FFFFFF !important;
            margin-bottom: -2px !important;
            box-shadow: 0 -2px 8px rgba(13, 37, 58, 0.15) !important;
            opacity: 1.0 !important;
        }
        
        /* Cards Informativos (fundo branco para contraste perfeito com a página cinza) */
        .custom-card {
            background-color: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 16px;
            box-shadow: 0 2px 6px rgba(13, 37, 58, 0.06);
        }
        .custom-card-title {
            color: #0D253A;
            font-size: 1.12rem;
            font-weight: 800;
            margin-bottom: 8px;
        }
        .custom-card-desc {
            color: #1E3A5F;
            font-size: 0.92rem;
            line-height: 1.5;
        }
        
        /* Botões Primários */
        .stButton > button[kind="primary"] {
            background-color: #0D253A !important;
            color: #FFFFFF !important;
            border-

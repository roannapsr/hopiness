import base64
from datetime import datetime
import io
import math
import os
import urllib.parse
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
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# CONFIGURAÇÃO DE TELA
# ==============================================================================
st.set_page_config(
    page_title="HOPINESS PROJECT by Felipe Correa",
    page_icon="🪟",
    layout="wide",
)

# 1. CARREGAMENTO DA LOGO (vdr.jpeg)
logo_b64 = ""
for img_name in ["vdr.jpeg", "vdr.jpg", "logo.png", "logo.jpeg"]:
  if os.path.exists(img_name):
    with open(img_name, "rb") as f:
      logo_b64 = base64.b64encode(f.read()).decode("utf-8")
    break

# Se achou a logo, monta a imagem limpa sem borda branca; senão, monta o selo circular cinza com o prédio vermelho
if logo_b64:
  logo_render_html = f'<img src="data:image/jpeg;base64,{logo_b64}" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; display: block; border: none; mix-blend-mode: multiply;">'
else:
  logo_render_html = """
    <div style="width: 66px; height: 66px; background-color: #5A5A5A; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; border: none;">
        <div style="display: flex; gap: 2px; align-items: flex-end; height: 26px; margin-bottom: 2px;">
            <div style="width: 8px; height: 18px; background-color: #D01B13;"></div>
            <div style="width: 8px; height: 26px; background-color: #B50915;"></div>
            <div style="width: 8px; height: 14px; background-color: #9D201C;"></div>
        </div>
        <span style="color: #FFFFFF; font-size: 7px; font-weight: 900; letter-spacing: 0.5px;">RIO BRANCO</span>
    </div>
    """

# ==============================================================================
# CONTROLE DE ESTADO DA ABA SELECIONADA
# ==============================================================================
if "aba_ativa" not in st.session_state:
  st.session_state["aba_ativa"] = "projetos"

# Query params para permitir troca instantânea via HTML
query_params = st.query_params
if "aba" in query_params:
  st.session_state["aba_ativa"] = query_params["aba"]

aba_atual = st.session_state["aba_ativa"]

# ==============================================================================
# CSS FORÇADO NO BODY E NO CONTAINER DO STREAMLIT
# ==============================================================================
st.markdown(
    """
<style>
    /* 1. FUNDO REAL COM DEGRADÊ EM TODO O SISTEMA */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(180deg, #FDE8E7 0%, #FFFFFF 32%, #F8F9FA 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* Remove padding superior desnecessário do Streamlit */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Cartões e Métricas */
    .metric-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 15px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
        margin-bottom: 15px;
    }
    .metric-label {
        color: #5A5A5A;
        font-size: 0.92rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .metric-val {
        color: #9D201C;
        font-size: 1.85rem;
        font-weight: 900;
        margin: 0;
    }
    
    /* Formulários */
    .stTextInput input, .stNumberInput input {
        background-color: #FFFFFF !important;
        color: #9D201C !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        border: 1px solid #CBD5E1 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] * {
        color: #0D253A !important;
        font-weight: 700 !important;
    }

    /* Botões */
    .btn-red button {
        background-color: #D01B13 !important;
        color: #FFFFFF !important;
        border-radius: 25px !important;
        font-weight: 800 !important;
        padding: 12px 28px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(208,27,19,0.3) !important;
        width: 100% !important;
    }
    .btn-pdf button {
        background-color: #2D3748 !important;
        color: #FFFFFF !important;
        border-radius: 25px !important;
        font-weight: 800 !important;
        padding: 12px 28px !important;
        border: none !important;
        width: 100% !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# COMPONENTE VISUAL BLINDADO (CABEÇALHO COM ESQUADRIAS + TÍTULO VERMELHO + ABAS PÍLULA)
# ==============================================================================
# Cores exatas das abas baseadas na ativação
c_proj = "#9D201C" if aba_atual == "projetos" else "#D01B13"
c_temp = "#9D201C" if aba_atual == "tempera" else "#D01B13"
c_fin = "#9D201C" if aba_atual == "financeiro" else "#D01B13"
c_abnt = "#9D201C" if aba_atual == "abnt" else "#D01B13"

sh_proj = (
    "box-shadow: 0 4px 12px rgba(157, 32, 28, 0.5);"
    if aba_atual == "projetos"
    else "box-shadow: 0 3px 6px rgba(208, 27, 19, 0.25);"
)
sh_temp = (
    "box-shadow: 0 4px 12px rgba(157, 32, 28, 0.5);"
    if aba_atual == "tempera"
    else "box-shadow: 0 3px 6px rgba(208, 27, 19, 0.25);"
)
sh_fin = (
    "box-shadow: 0 4px 12px rgba(157, 32, 28, 0.5);"
    if aba_atual == "financeiro"
    else "box-shadow: 0 3px 6px rgba(208, 27, 19, 0.25);"
)
sh_abnt = (
    "box-shadow: 0 4px 12px rgba(157, 32, 28, 0.5);"
    if aba_atual == "abnt"
    else "box-shadow: 0 3px 6px rgba(208, 27, 19, 0.25);"
)

html_cabecalho_e_abas = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: transparent; }}
    
    /* FAIXA BRANCA DO CABEÇALHO COM DESENHO ARQUITETÔNICO DE ESQUADRIAS */
    .header-box {{
        position: relative;
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-left: 8px solid #D01B13;
        border-radius: 12px;
        padding: 14px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(208, 27, 19, 0.08);
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-height: 98px;
    }}

    /* SVG DAS ESQUADRIAS EM PERSPECTIVA REAL */
    .esquadrias-svg {{
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        opacity: 0.38;
    }}

    .header-content {{
        position: relative;
        z-index: 3;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }}

    /* TÍTULO EM VERMELHO ESCURO PURO */
    .header-title {{
        color: #9D201C !important;
        font-size: 2.35rem;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-align: center;
    }}

    .header-author {{
        color: #5A5A5A;
        font-size: 0.95rem;
        font-weight: 600;
        font-style: italic;
        text-align: right;
    }}

    /* CONTAINER DAS 4 ABAS PÍLULA */
    .tabs-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 8px;
    }}

    /* ESTILO DAS PÍLULAS VERMELHAS COM TEXTO 100% BRANCO */
    .tab-pill {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 11px 16px;
        border-radius: 25px;
        color: #FFFFFF !important;
        text-decoration: none;
        font-weight: 800;
        font-size: 0.92rem;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        border: none;
        text-align: center;
    }}
    .tab-pill:hover {{
        background-color: #B50915 !important;
    }}
</style>
</head>
<body>
    <!-- CABEÇALHO -->
    <div class="header-box">
        <svg class="esquadrias-svg" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" viewBox="0 0 1200 120">
            <!-- Travessas Horizontais -->
            <line x1="0" y1="20" x2="1200" y2="20" stroke="#64748B" stroke-width="2"/>
            <line x1="0" y1="60" x2="1200" y2="60" stroke="#64748B" stroke-width="2.5"/>
            <line x1="0" y1="100" x2="1200" y2="100" stroke="#64748B" stroke-width="2"/>
            
            <!-- Montantes de Esquadrias em Perspectiva (Esquerda) -->
            <line x1="80" y1="0" x2="220" y2="120" stroke="#64748B" stroke-width="2.2"/>
            <line x1="160" y1="0" x2="270" y2="120" stroke="#94A3B8" stroke-width="1.8"/>
            <line x1="240" y1="0" x2="320" y2="120" stroke="#94A3B8" stroke-width="1.8"/>
            <line x1="320" y1="0" x2="370" y2="120" stroke="#CBD5E1" stroke-width="1.5"/>

            <!-- Montantes de Esquadrias em Perspectiva (Direita) -->
            <line x1="1120" y1="0" x2="980" y2="120" stroke="#64748B" stroke-width="2.2"/>
            <line x1="1040" y1="0" x2="930" y2="120" stroke="#94A3B8" stroke-width="1.8"/>
            <line x1="960" y1="0" x2="880" y2="120" stroke="#94A3B8" stroke-width="1.8"/>
            <line x1="880" y1="0" x2="830" y2="120" stroke="#CBD5E1" stroke-width="1.5"/>
            
            <!-- Reflexos no Vidro -->
            <line x1="140" y1="100" x2="220" y2="20" stroke="#E2E8F0" stroke-width="1.5" stroke-dasharray="10,6"/>
            <line x1="980" y1="100" x2="1060" y2="20" stroke="#E2E8F0" stroke-width="1.5" stroke-dasharray="10,6"/>
        </svg>

        <div class="header-content">
            <div style="flex-shrink: 0;">
                {logo_render_html}
            </div>
            <div style="text-align: center; flex-grow: 1;">
                <div class="header-title">HOPINESS PROJECT</div>
            </div>
            <div style="flex-shrink: 0;">
                <div class="header-author">by Felipe Correa</div>
            </div>
        </div>
    </div>

    <!-- 4 ABAS PÍLULAS VERMELHAS COM TEXTO BRANCO -->
    <div class="tabs-grid">
        <a class="tab-pill" style="background-color: {c_proj}; {sh_proj}" onclick="window.parent.postMessage({{type: 'streamlit:setQueryParams', queryParams: {{aba: 'projetos'}}}}, '*'); window.location.search='?aba=projetos';">
            📐 Projetos Padrão & Orçamento
        </a>
        <a class="tab-pill" style="background-color: {c_temp}; {sh_temp}" onclick="window.parent.postMessage({{type: 'streamlit:setQueryParams', queryParams: {{aba: 'tempera'}}}}, '*'); window.location.search='?aba=tempera';">
            🏭 Pedido de Têmpera (Corte)
        </a>
        <a class="tab-pill" style="background-color: {c_fin}; {sh_fin}" onclick="window.parent.postMessage({{type: 'streamlit:setQueryParams', queryParams: {{aba: 'financeiro'}}}}, '*'); window.location.search='?aba=financeiro';">
            💵 Financeiro da Obra
        </a>
        <a class="tab-pill" style="background-color: {c_abnt}; {sh_abnt}" onclick="window.parent.postMessage({{type: 'streamlit:setQueryParams', queryParams: {{aba: 'abnt'}}}}, '*'); window.location.search='?aba=abnt';">
            📋 Catálogo Técnico ABNT
        </a>
    </div>
</body>
</html>
"""

# Renderiza o topo com altura exata e sem quebras de layout
components.html(html_cabecalho_e_abas, height=195)

# ==============================================================================
# REGRAS TÉCNICAS E MOTOR DE PROJETOS
# ==============================================================================
PROJETOS_PADRAO = {
    "guarda_corpo_torres": {
        "nome": "Guarda-Corpo / Sacada (NBR 14718)",
        "vidro_padrao": "Laminado 10mm (5+5) ou Laminado-Temperado",
        "kit_base": 450.0,
        "insumos_base": 120.0,
        "calc": lambda l, a: [{
            "peca": "Painéis de Guarda-Corpo",
            "largura": round((l / 3) - 0.02, 3),
            "altura": round(a, 3),
            "qtd": 3,
        }],
    },
    "box_padrao_2f": {
        "nome": "Box Frontal Padrão (1 Fixo + 1 Móvel)",
        "vidro_padrao": "Temperado 8mm Incolor",
        "kit_base": 180.0,
        "insumos_base": 45.0,
        "calc": lambda l, a: [
            {
                "peca": "Vidro Fixo",
                "largura": round((l / 2) + 0.02, 3),
                "altura": round(a - 0.05, 3),
                "qtd": 1,
            },
            {
                "peca": "Vidro Móvel (Porta)",
                "largura": round((l / 2) + 0.05, 3),
                "altura": round(a - 0.05, 3),
                "qtd": 1,
            },
        ],
    },
    "janela_4f": {
        "nome": "Janela 4 Folhas (2 Fixos + 2 Móveis)",
        "vidro_padrao": "Temperado 8mm Incolor",
        "kit_base": 280.0,
        "insumos_base": 60.0,
        "calc": lambda l, a: [
            {
                "peca": "Fixos Laterais",
                "largura": round((l / 4) + 0.02, 3),
                "altura": round(a - 0.04, 3),
                "qtd": 2,
            },
            {
                "peca": "Móveis Centrais",
                "largura": round((l / 4) + 0.05, 3),
                "altura": round(a - 0.04, 3),
                "qtd": 2,
            },
        ],
    },
    "porta_pivotante": {
        "nome": "Porta Pivotante de Abrir (1 Folha)",
        "vidro_padrao": "Temperado 10mm Incolor",
        "kit_base": 340.0,
        "insumos_base": 50.0,
        "calc": lambda l, a: [{
            "peca": "Folha Pivotante",
            "largura": round(l - 0.015, 3),
            "altura": round(a - 0.02, 3),
            "qtd": 1,
        }],
    },
}


def arredondar_m2(dim):
  return math.ceil(dim / 0.05) * 0.05


def processar_calculo(
    chave_proj, largura, altura, preco_m2, kit, insumos, mao_obra, margem
):
  p = PROJETOS_PADRAO[chave_proj]
  pecas = p["calc"](largura, altura)
  area_liq = 0.0
  area_fat = 0.0

  for item in pecas:
    w, h, q = item["largura"], item["altura"], item["qtd"]
    area_liq += (w * h) * q
    area_fat += (arredondar_m2(w) * arredondar_m2(h)) * q

  custo_v = area_fat * preco_m2
  custo_total = custo_v + kit + insumos + mao_obra
  fator = 1.0 - (margem / 100.0 if margem < 100 else 0.99)
  preco_venda = custo_total / fator
  lucro = preco_venda - custo_total

  return {
      "nome": p["nome"],
      "vidro": p["vidro_padrao"],
      "pecas": pecas,
      "area_liq": area_liq,
      "area_fat": area_fat,
      "custo_v": custo_v,
      "custo_total": custo_total,
      "preco_venda": preco_venda,
      "lucro": lucro,
      "margem": margem,
  }


def gerar_pdf(dados):
  buf = io.BytesIO()
  doc = SimpleDocTemplate(
      buf,
      pagesize=A4,
      leftMargin=1.5 * cm,
      rightMargin=1.5 * cm,
      topMargin=1.5 * cm,
      bottomMargin=1.5 * cm,
  )
  styles = getSampleStyleSheet()

  AZUL_ESCURO = colors.HexColor("#9D201C")
  VERM = colors.HexColor("#D01B13")
  CINZA = colors.HexColor("#5A5A5A")
  FUNDO = colors.HexColor("#F8FAFC")
  BORDA = colors.HexColor("#CBD5E1")
  BRANCO = colors.white

  st_t = ParagraphStyle(
      "T",
      fontName="Helvetica-Bold",
      fontSize=18,
      textColor=AZUL_ESCURO,
      alignment=1,
  )
  st_sub = ParagraphStyle(
      "Sub", fontName="Helvetica", fontSize=9, textColor=CINZA, alignment=1
  )
  st_c = ParagraphStyle(
      "C", fontName="Helvetica", fontSize=8.5, textColor=CINZA
  )
  st_th = ParagraphStyle(
      "TH", fontName="Helvetica-Bold", fontSize=8.5, textColor=BRANCO
  )
  st_td = ParagraphStyle(
      "TD", fontName="Helvetica", fontSize=8.5, textColor=CINZA
  )
  st_tdr = ParagraphStyle(
      "TDR",
      fontName="Helvetica-Bold",
      fontSize=8.5,
      textColor=AZUL_ESCURO,
      alignment=2,
  )

  elems = [
      Paragraph("<b>HOPINESS PROJECT</b>", st_t),
      Paragraph(
          "Vidraçaria Rio Branco | Soluções em Vidros e Esquadrias", st_sub
      ),
      Spacer(1, 0.2 * cm),
      Paragraph(
          "<b>PROPOSTA COMERCIAL & ORÇAMENTO</b>",
          ParagraphStyle(
              "P",
              fontName="Helvetica-Bold",
              fontSize=12,
              textColor=VERM,
              alignment=1,
          ),
      ),
      HRFlowable(
          width="100%", thickness=1.5, color=VERM, spaceBefore=4, spaceAfter=8
      ),
      Table(
          [[
              Paragraph(
                  f"<b>CLIENTE:</b> {dados['cli']}<br/><b>LOCAL:</b>"
                  f" {dados['loc']}",
                  st_c,
              ),
              Paragraph(
                  f"<b>PROJETO:</b> {dados['proj']}<br/><b>VÃO:</b>"
                  f" {dados['l']:.2f}m x {dados['a']:.2f}m",
                  st_c,
              ),
          ]],
          colWidths=[9 * cm, 9 * cm],
          style=[
              ("BACKGROUND", (0, 0), (-1, -1), FUNDO),
              ("BOX", (0, 0), (-1, -1), 0.8, BORDA),
              ("TOPPADDING", (0, 0), (-1, -1), 6),
              ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
          ],
      ),
      Spacer(1, 0.4 * cm),
      Table(
          [
              [
                  Paragraph(
                      "Discriminação dos Serviços / Materiais", st_th
                  ),
                  Paragraph(
                      "Subtotal", ParagraphStyle("R", parent=st_th, alignment=2)
                  ),
              ],
              [
                  Paragraph(
                      f"Vidros Lapidados ({dados['vidro']}) - Área:"
                      f" {dados['fat']:.2f} m²",
                      st_td,
                  ),
                  Paragraph(f"R$ {dados['cv']:.2f}", st_tdr),
              ],
              [
                  Paragraph(
                      "Kits de Instalação e Ferragens Estruturais", st_td
                  ),
                  Paragraph(f"R$ {dados['ck']:.2f}", st_tdr),
              ],
              [
                  Paragraph(
                      "Insumos de Vedação e Fixadores Químicos", st_td
                  ),
                  Paragraph(f"R$ {dados['ci']:.2f}", st_tdr),
              ],
              [
                  Paragraph(
                      "Mão de Obra Especializada e Logística", st_td
                  ),
                  Paragraph(f"R$ {dados['cmo']:.2f}", st_tdr),
              ],
          ],
          colWidths=[13.5 * cm, 4.5 * cm],
          style=[
              ("BACKGROUND", (0, 0), (-1, 0), AZUL_ESCURO),
              ("GRID", (0, 0), (-1, -1), 0.5, BORDA),
              ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BRANCO, FUNDO]),
              ("TOPPADDING", (0, 0), (-1, -1), 5),
              ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
          ],
      ),
      Spacer(1, 0.4 * cm),
      Table(
          [[
              Paragraph(
                  "<b>Condições:</b> 50% de sinal e saldo na"
                  " conclusão.<br/>Desconto de 5% no Pix.<br/>Garantia: 1 ano"
                  " para instalação.",
                  st_c,
              ),
              Paragraph(
                  "<font size='8' color='#5A5A5A'>VALOR TOTAL</font><br/><font"
                  f" size='16' color='#9D201C'><b>R$ {dados['total']:.2f}</b></font>",
                  st_tdr,
              ),
          ]],
          colWidths=[11.5 * cm, 6.5 * cm],
          style=[
              ("BACKGROUND", (0, 0), (-1, -1), FUNDO),
              ("BOX", (0, 0), (-1, -1), 1, VERM),
              ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
              ("TOPPADDING", (0, 0), (-1, -1), 6),
              ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
          ],
      ),
  ]
  doc.build(elems)
  val = buf.getvalue()
  buf.close()
  return val


# ==============================================================================
# CONTEÚDO DA TELA ATIVA
# ==============================================================================
if aba_atual == "projetos":
  col_esq, col_dir = st.columns([1.1, 1.0], gap="large")

  with col_esq:
    st.markdown(
        "<div style='background:#FFFFFF; border:1px solid #CBD5E1;"
        " border-radius:12px; padding:22px; box-shadow:0 3px 10px"
        " rgba(0,0,0,0.04); margin-bottom:20px;'><h4 style='color:#9D201C;"
        " margin-top:0; font-size:1.3rem; font-weight:800;'>Configurações do"
        " Vão</h4>",
        unsafe_allow_html=True,
    )

    sel_proj = st.selectbox(
        "Selecione o Projeto Padrão da Obra",
        options=list(PROJETOS_PADRAO.keys()),
        format_func=lambda x: PROJETOS_PADRAO[x]["nome"],
    )

    c_cli, c_zap, c_loc = st.columns(3)
    nome_c = c_cli.text_input("Nome do Cliente", "Mariana Albuquerque")
    zap_c = c_zap.text_input("WhatsApp", "81991234567")
    loc_c = c_loc.text_input("Local da Instalação", "Boa Viagem - Recife/PE")

    c_l, c_a = st.columns(2)
    larg_v = c_l.number_input(
        "Largura do Vão (m)",
        min_value=0.2,
        max_value=12.0,
        value=3.40,
        step=0.05,
    )
    alt_v = c_a.number_input(
        "Altura do Vão (m)", min_value=0.2, max_value=6.0, value=1.10, step=0.05
    )

    c_pm2, c_k, c_ins = st.columns(3)
    pm2 = c_pm2.number_input("Vidro R$/m²", value=380.0, step=10.0)
    kit_v = c_k.number_input(
        "Kit/Ferragens (R$)",
        value=PROJETOS_PADRAO[sel_proj]["kit_base"],
        step=10.0,
    )
    ins_v = c_ins.number_input(
        "Insumos (R$)",
        value=PROJETOS_PADRAO[sel_proj]["insumos_base"],
        step=5.0,
    )

    c_mo, c_mg = st.columns(2)
    mo_v = c_mo.number_input("Mão de Obra (R$)", value=450.0, step=10.0)
    mg_v = c_mg.slider(
        "Margem de Lucro (%)", min_value=10.0, max_value=70.0, value=35.0
    )

    st.markdown("</div>", unsafe_allow_html=True)

  res = processar_calculo(
      sel_proj, larg_v, alt_v, pm2, kit_v, ins_v, mo_v, mg_v
  )

  with col_dir:
    m_c1, m_c2 = st.columns(2)
    with m_c1:
      st.markdown(
          f"""
            <div class="metric-box">
                <div class="metric-label">Área Real (Líquida):</div>
                <div class="metric-val">{res['area_liq']:.2f} m²</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Custo Direto Total:</div>
                <div class="metric-val">R$ {res['custo_total']:.2f}</div>
            </div>
        """,
          unsafe_allow_html=True,
      )
    with m_c2:
      st.markdown(
          f"""
            <div class="metric-box">
                <div class="metric-label">Área Faturada (+Folga):</div>
                <div class="metric-val">{res['area_fat']:.2f} m²</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Preço de Venda Sugerido:</div>
                <div class="metric-val">R$ {res['preco_venda']:.2f}</div>
            </div>
        """,
          unsafe_allow_html=True,
      )

    st.success(
        f" Lucro Bruto Estimado: **R$ {res['lucro']:.2f}** (Margem:"
        f" {res['margem']}%)"
    )

  # BOTÕES INFERIORES REDONDOS
  st.markdown("<br/>", unsafe_allow_html=True)
  b_esp1, b_c1, b_c2, b_esp2 = st.columns([1, 1.3, 1.3, 1])

  dados_proposta = {
      "cli": nome_c,
      "loc": loc_c,
      "proj": res["nome"],
      "vidro": res["vidro"],
      "l": larg_v,
      "a": alt_v,
      "fat": res["area_fat"],
      "cv": res["custo_v"],
      "ck": kit_v,
      "ci": ins_v,
      "cmo": mo_v,
      "total": res["preco_venda"],
  }

  with b_c1:
    st.markdown('<div class="btn-red">', unsafe_allow_html=True)
    if st.button("📄 Gerar Orçamento", use_container_width=True):
      st.toast("Orçamento recalculado com sucesso!")
    st.markdown("</div>", unsafe_allow_html=True)

  with b_c2:
    st.markdown('<div class="btn-pdf">', unsafe_allow_html=True)
    pdf_bytes = gerar_pdf(dados_proposta)
    st.download_button(
        "📥 Exportar PDF",
        data=pdf_bytes,
        file_name=f"Orcamento_{nome_c.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

elif aba_atual == "tempera":
  st.markdown(
      "<h3 style='color:#9D201C;'>Ordem de Corte para a Têmpera</h3>",
      unsafe_allow_html=True,
  )
  st.info("Medidas técnicas calculadas com descontos de folga e transpasse.")
  res_temp = processar_calculo(
      "guarda_corpo_torres", 3.40, 1.10, 380.0, 450.0, 120.0, 450.0, 35.0
  )
  tab_cortes = []
  for pc in res_temp["pecas"]:
    tab_cortes.append({
        "Peça / Posição": pc["peca"],
        "Largura de Corte (m)": f"{pc['largura']:.3f}",
        "Altura de Corte (m)": f"{pc['altura']:.3f}",
        "Quantidade": pc["qtd"],
        "Especificação": res_temp["vidro"],
    })
  st.table(tab_cortes)

elif aba_atual == "financeiro":
  st.markdown(
      "<h3 style='color:#9D201C;'>Gestão Financeira da Obra</h3>",
      unsafe_allow_html=True,
  )
  cf1, cf2, cf3 = st.columns(3)
  cf1.metric("Valor Total Previsto", "R$ 3.787,85")
  cf2.metric("Custo de Materiais e Instalação", "R$ 2.462,10")
  cf3.metric("Lucro Líquido Estimado", "R$ 1.325,75")

elif aba_atual == "abnt":
  st.markdown(
      "<h3 style='color:#9D201C;'>Normas Técnicas da Construção Civil</h3>",
      unsafe_allow_html=True,
  )
  st.markdown(
      """
    - **ABNT NBR 14207 (Boxes de Banheiro):** Exige vidro de segurança (temperado 8mm ou laminado).
    - **ABNT NBR 14718 (Guarda-Corpos e Sacadas):** Obrigatório vidro laminado ou laminado-temperado. Proibido vidro temperado comum sem laminação.
    - **ABNT NBR 7199 (Vidros na Construção Civil):** Vidros abaixo de 1,10m do piso acabado devem ser vidros de segurança.
    """
  )

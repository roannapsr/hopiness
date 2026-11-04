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

# ==============================================================================
# CONFIGURAÇÃO DE PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="HOPINESS PROJECT by Felipe Correa",
    page_icon="🪟",
    layout="wide",
)

# ==============================================================================
# LEITURA DA LOGO LOCAL (vdr.jpeg)
# ==============================================================================
logo_src = ""
for img_name in ["vdr.jpeg", "vdr.jpg", "logo.png", "logo.jpeg"]:
  if os.path.exists(img_name):
    with open(img_name, "rb") as f:
      b64 = base64.b64encode(f.read()).decode("utf-8")
    ext = "jpeg" if "jp" in img_name else "png"
    logo_src = f"data:image/{ext};base64,{b64}"
    break

# ==============================================================================
# CSS GLOBAL E CONTROLO DE CORES
# ==============================================================================
st.markdown(
    """
    <style>
        /* 1. FUNDO GERAL COM DEGRADÊ SUAVE */
        .stApp, [data-testid="stAppViewContainer"], section.main {
            background: linear-gradient(180deg, #FCE8E6 0%, #FFFFFF 30%, #F8F9FA 100%) !important;
            background-attachment: fixed !important;
        }

        /* 2. FORÇAR TODAS AS ABAS DO STREAMLIT A SEREM VERMELHAS COM TEXTO BRANCO */
        div[data-testid="stTabs"] [role="tablist"] {
            gap: 12px !important;
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            margin-bottom: 25px !important;
        }
        div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
            display: none !important;
        }
        div[data-testid="stTabs"] button[role="tab"] {
            background-color: #D01B13 !important;
            border-radius: 25px !important;
            border: none !important;
            padding: 10px 24px !important;
            box-shadow: 0 3px 6px rgba(208, 27, 19, 0.25) !important;
        }
        /* Força a cor branca em absolutamente todos os nós de texto das abas */
        div[data-testid="stTabs"] button[role="tab"] * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 0.95rem !important;
        }
        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            background-color: #9D201C !important;
            box-shadow: 0 4px 12px rgba(157, 32, 28, 0.45) !important;
        }

        /* 3. CARTÕES DE MÉTRICAS */
        .metric-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 20px 15px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.04);
            margin-bottom: 18px;
        }
        .metric-card-label {
            color: #5A5A5A;
            font-size: 0.95rem;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .metric-card-val {
            color: #9D201C;
            font-size: 1.85rem;
            font-weight: 900;
            margin: 0;
        }

        /* 4. CAMPOS DE ENTRADA */
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

        /* 5. BOTÕES */
        .stButton > button[kind="primary"] {
            background-color: #D01B13 !important;
            color: #FFFFFF !important;
            border-radius: 25px !important;
            font-weight: 800 !important;
            padding: 12px 28px !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(208,27,19,0.3) !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #B50915 !important;
        }
        .stDownloadButton > button {
            background-color: #5A5A5A !important;
            color: #FFFFFF !important;
            border-radius: 25px !important;
            font-weight: 700 !important;
            border: none !important;
            padding: 12px 24px !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# FAIXA DO CABEÇALHO (HTML/SVG INTEGRADO: ESQUADRIAS E TÍTULO VERMELHO GARANTIDOS)
# ==============================================================================
logo_tag = (
    f'<img src="{logo_src}" style="width: 65px; height: 65px; border-radius:'
    " 50%; object-fit: cover; display: block; mix-blend-mode: multiply;"
    ' border: none;">'
    if logo_src
    else """
    <div style="width: 60px; height: 60px; background-color: #5A5A5A; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #FFFFFF; font-size: 8px; font-weight: 900; text-align: center;">RIO<br/>BRANCO</div>
"""
)

st.markdown(
    f"""
    <div style="position: relative; background: #FFFFFF; border: 1px solid #CBD5E1; border-left: 8px solid #D01B13; border-radius: 12px; padding: 18px 25px; margin-top: -15px; margin-bottom: 22px; box-shadow: 0 4px 15px rgba(208, 27, 19, 0.08); overflow: hidden; min-height: 100px;">
        <!-- DESENHO REAL DAS ESQUADRIAS EM VETOR SVG -->
        <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; opacity: 0.65;" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <pattern id="esquadria_pat" width="120" height="100" patternUnits="userSpaceOnUse">
                    <!-- Perfis Principais de Alumínio -->
                    <rect x="0" y="0" width="120" height="100" fill="none" stroke="#94A3B8" stroke-width="2.5"/>
                    <line x1="60" y1="0" x2="60" y2="100" stroke="#94A3B8" stroke-width="2"/>
                    <line x1="0" y1="50" x2="120" y2="50" stroke="#94A3B8" stroke-width="2"/>
                    <!-- Linhas Diagonais Translúcidas de Reflexo de Vidro -->
                    <line x1="5" y1="95" x2="55" y2="5" stroke="#CBD5E1" stroke-width="1.2" stroke-dasharray="6,4"/>
                    <line x1="65" y1="95" x2="115" y2="5" stroke="#CBD5E1" stroke-width="1.2" stroke-dasharray="6,4"/>
                </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#esquadria_pat)"/>
        </svg>

        <!-- CONTEÚDO DO CABEÇALHO (LOGO, TÍTULO VERMELHO ESCURO E ASSINATURA) -->
        <div style="position: relative; z-index: 2; display: flex; align-items: center; justify-content: space-between; width: 100%;">
            <div style="flex-shrink: 0;">
                {logo_tag}
            </div>
            <div style="text-align: center; flex-grow: 1;">
                <div style="color: #9D201C !important; -webkit-text-fill-color: #9D201C !important; font-size: 2.35rem; font-weight: 900; letter-spacing: 2px; text-transform: uppercase; font-family: 'Segoe UI', sans-serif;">
                    HOPINESS PROJECT
                </div>
            </div>
            <div style="flex-shrink: 0;">
                <div style="color: #5A5A5A; font-size: 0.95rem; font-weight: 600; font-style: italic;">
                    by Felipe Correa
                </div>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# PROJETOS TÉCNICOS E CÁLCULO VIDREIRO
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


# ==============================================================================
# MOTOR DO PDF (REPORTLAB COM A PALETA DA VIDRAÇARIA RIO BRANCO)
# ==============================================================================
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
# NAVEGAÇÃO E ABAS (PÍLULAS VERMELHAS COM FONTE BRANCA)
# ==============================================================================
aba_proj, aba_temp, aba_fin, aba_abnt = st.tabs([
    "📐 Projetos Padrão & Orçamento",
    "🏭 Pedido de Têmpera (Corte)",
    "💵 Financeiro da Obra",
    "📋 Catálogo Técnico ABNT",
])

# ------------------------------------------------------------------------------
# ABA 1: PROJETOS E ORÇAMENTO
# ------------------------------------------------------------------------------
with aba_proj:
  col_esquerda, col_direita = st.columns([1.15, 1.0], gap="large")

  with col_esquerda:
    st.markdown(
        "<h4 style='color:#9D201C; margin-top:0;'>Configurações do Vão</h4>",
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

  res = processar_calculo(
      sel_proj, larg_v, alt_v, pm2, kit_v, ins_v, mo_v, mg_v
  )

  with col_direita:
    st.markdown(
        "<h4 style='color:#9D201C; margin-top:0;'>Resumo Comercial</h4>",
        unsafe_allow_html=True,
    )

    m_c1, m_c2 = st.columns(2)
    with m_c1:
      st.markdown(
          f"""
                <div class="metric-card">
                    <div class="metric-card-label">Área Real (Líquida):</div>
                    <div class="metric-card-val">{res['area_liq']:.2f} m²</div>
                </div>
                <div class="metric-card">
                    <div class="metric-card-label">Custo Direto Total:</div>
                    <div class="metric-card-val">R$ {res['custo_total']:.2f}</div>
                </div>
            """,
          unsafe_allow_html=True,
      )
    with m_c2:
      st.markdown(
          f"""
                <div class="metric-card">
                    <div class="metric-card-label">Área Faturada (+Folga):</div>
                    <div class="metric-card-val">{res['area_fat']:.2f} m²</div>
                </div>
                <div class="metric-card">
                    <div class="metric-card-label">Preço de Venda Sugerido:</div>
                    <div class="metric-card-val">R$ {res['preco_venda']:.2f}</div>
                </div>
            """,
          unsafe_allow_html=True,
      )

    st.success(
        f" Lucro Bruto Estimado: **R$ {res['lucro']:.2f}** (Margem:"
        f" {res['margem']}%)"
    )

  st.markdown("<br/>", unsafe_allow_html=True)
  b_col1, b_col2, b_col3 = st.columns([1, 1, 1])

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

  with b_col1:
    pdf_bytes = gerar_pdf(dados_proposta)
    st.download_button(
        " Exportar PDF Profissional",
        data=pdf_bytes,
        file_name=f"Orcamento_{nome_c.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

  with b_col2:
    msg_whats = (
        f"Olá, {nome_c}! Segue o orçamento da Vidraçaria Rio Branco para o seu"
        f" projeto de {res['nome']} ({larg_v:.2f}m x {alt_v:.2f}m) - Total: R$"
        f" {res['preco_venda']:.2f}."
    )
    url_zap = f"https://api.whatsapp.com/send?phone=55{zap_c.strip()}&text={urllib.parse.quote(msg_whats)}"
    st.link_button(" Enviar via WhatsApp", url_zap, use_container_width=True)

  with b_col3:
    st.button(" Atualizar Orçamento", type="primary", use_container_width=True)

# ------------------------------------------------------------------------------
# ABA 2: TÊMPERA
# ------------------------------------------------------------------------------
with aba_temp:
  st.markdown(
      "<h3 style='color:#9D201C;'>Ordem de Corte para a Têmpera</h3>",
      unsafe_allow_html=True,
  )
  tab_pecas = []
  for pc in res["pecas"]:
    tab_pecas.append({
        "Peça / Posição": pc["peca"],
        "Largura de Corte (m)": f"{pc['largura']:.3f}",
        "Altura de Corte (m)": f"{pc['altura']:.3f}",
        "Quantidade": pc["qtd"],
        "Especificação do Vidro": res["vidro"],
    })
  st.table(tab_pecas)

# ------------------------------------------------------------------------------
# ABA 3: FINANCEIRO
# ------------------------------------------------------------------------------
with aba_fin:
  st.markdown(
      "<h3 style='color:#9D201C;'>Gestão Financeira da Obra</h3>",
      unsafe_allow_html=True,
  )
  c_fin1, c_fin2, c_fin3 = st.columns(3)
  c_fin1.metric("Valor Total da Obra", f"R$ {res['preco_venda']:.2f}")
  c_fin2.metric("Custo Operacional Total", f"R$ {res['custo_total']:.2f}")
  c_fin3.metric("Lucro Líquido Previsto", f"R$ {res['lucro']:.2f}")

# ------------------------------------------------------------------------------
# ABA 4: ABNT
# ------------------------------------------------------------------------------
with aba_abnt:
  st.markdown(
      "<h3 style='color:#9D201C;'>Normas Técnicas da Construção Civil</h3>",
      unsafe_allow_html=True,
  )
  st.markdown(
      """
        - **ABNT NBR 14207 (Boxes de Banheiro):** Exige vidro de segurança (temperado 8mm ou laminado).
        - **ABNT NBR 14718 (Guarda-Corpos e Sacadas):** Obrigatório vidro laminado ou laminado-temperado. **Proibido vidro temperado comum sem laminação**.
        - **ABNT NBR 7199 (Vidros na Construção Civil):** Vidros abaixo de 1,10m do piso acabado devem ser vidros de segurança.
        """
  )

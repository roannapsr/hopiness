import io
import math
import urllib.parse
from datetime import datetime
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheetimport io
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
# CONFIGURAÇÃO DE TELA E ESTILO (Azul Marinho, Cinza e Branco)
# ==============================================================================
st.set_page_config(
    page_title="HOPINESS PROJECT by Felipe Correa",
    page_icon="🪟",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #ECEFF1;
        }
        p, span, label, .stMarkdown, .stCaption {
            color: #0D253A;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #0D253A !important;
            font-weight: 800 !important;
        }
        
        /* ABAS SEM BORDA RETANGULAR */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
            padding: 4px 0px;
            border: none !important;
            margin-bottom: 20px;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #0D253A !important;
            height: 3px !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #1E3A5F !important;
            background-color: transparent !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            padding: 8px 18px !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }
        .stTabs [aria-selected="true"] {
            color: #0D253A !important;
            background-color: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }

        /* SELECTBOX COM FONTE BRANCA NÍTIDA */
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
            color: #63B3ED !important;
        }

        /* INPUTS */
        .stTextInput input, .stNumberInput input {
            background-color: #FFFFFF !important;
            color: #0D253A !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            border: 1px solid #CBD5E1 !important;
        }

        /* CARDS */
        .custom-card {
            background-color: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 14px;
            box-shadow: 0 2px 4px rgba(13, 37, 58, 0.05);
        }
        .custom-card-title {
            color: #0D253A;
            font-size: 1.1rem;
            font-weight: 800;
            margin-bottom: 6px;
        }
        .custom-card-desc {
            color: #1E3A5F;
            font-size: 0.9rem;
            line-height: 1.45;
        }

        /* BOTÕES */
        .stButton > button[kind="primary"] {
            background-color: #0D253A !important;
            color: #FFFFFF !important;
            border-radius: 8px;
            font-weight: 700;
            padding: 10px 22px;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #1E3A5F !important;
        }
        .stDownloadButton > button {
            background-color: #1E3A5F !important;
            color: #FFFFFF !important;
            border-radius: 8px;
            font-weight: 700;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# CABEÇALHO DO PROJETO
# ==============================================================================
st.markdown(
    """
    <div style="margin-top: -20px; margin-bottom: 20px; border-bottom: 2px solid #CBD5E1; padding-bottom: 12px;">
        <h1 style="text-align: center; color: #0D253A; font-size: 2.2rem; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; text-transform: uppercase;">
            HOPINESS PROJECT
        </h1>
        <p style="text-align: right; color: #1E3A5F; font-size: 0.95rem; font-weight: 600; font-style: italic; margin-top: 2px; margin-bottom: 0px; padding-right: 10px;">
            by Felipe Correa
        </p>
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
            "largura_corte": round((l / 3) - 0.02, 3),
            "altura_corte": round(a, 3),
            "qtd": 3,
        }],
    },
    "porta_pivotante": {
        "nome": "Porta Pivotante de Abrir 1 Folha",
        "categoria": "Janelas & Portas",
        "vidro_padrao": "Temperado 10mm Incolor",
        "norma": "ABNT NBR 7199",
        "kit_padrao": (
            "Kit Ferragens Inox/Latão (Dobradiça Superior, Inferior, Fechadura"
            " e Puxador Tubo)"
        ),
        "custo_kit_base": 340.0,
        "custo_insumos_base": 50.0,
        "calcular_pecas": lambda l, a: [{
            "peca": "Folha Pivotante",
            "largura_corte": round(l - 0.015, 3),
            "altura_corte": round(a - 0.02, 3),
            "qtd": 1,
        }],
    },
    "espelho_bisotado": {
        "nome": "Espelho Prata Bisotado com Fixação Química",
        "categoria": "Espelhos & Decoração",
        "vidro_padrao": "Espelho Prata 4mm com Proteção Contra Oxidação",
        "norma": "ABNT NBR 15198",
        "kit_padrao": (
            "Silicone Neutro Fixa-Espelho + Fita Dupla Face Estrutural"
        ),
        "custo_kit_base": 65.0,
        "custo_insumos_base": 30.0,
        "calcular_pecas": lambda l, a: [{
            "peca": "Painel de Espelho Lapidado/Bisotado",
            "largura_corte": round(l, 3),
            "altura_corte": round(a, 3),
            "qtd": 1,
        }],
    },
}


# ==============================================================================
# FUNÇÕES DE CÁLCULO VIDREIRO
# ==============================================================================
def arredondar_m2_industrial(medida_m):
  """Arredondamento para múltiplos de 50mm (0.05m) para faturamento."""
  return math.ceil(medida_m / 0.05) * 0.05


def calcular_projeto_completo(
    projeto_key,
    largura_vao,
    altura_vao,
    preco_m2_vidro,
    custo_kit,
    custo_insumos,
    custo_mo,
    margem_lucro,
):
  proj = PROJETOS_PADRAO[projeto_key]
  pecas_corte = proj["calcular_pecas"](largura_vao, altura_vao)

  area_liquida_total = 0.0
  area_faturada_total = 0.0

  for p in pecas_corte:
    w = p["largura_corte"]
    h = p["altura_corte"]
    qtd = p["qtd"]
    area_liquida_total += (w * h) * qtd

    w_fat = arredondar_m2_industrial(w)
    h_fat = arredondar_m2_industrial(h)
    area_faturada_total += (w_fat * h_fat) * qtd

  custo_vidro = area_faturada_total * preco_m2_vidro
  custo_direto_total = custo_vidro + custo_kit + custo_insumos + custo_mo

  margem_decimal = (
      margem_lucro / 100.0 if margem_lucro < 100 else 0.99
  )  # Previne divisão por zero
  preco_venda_final = custo_direto_total / (1.0 - margem_decimal)
  lucro_bruto = preco_venda_final - custo_direto_total

  return {
      "projeto_nome": proj["nome"],
      "norma": proj["norma"],
      "vidro_padrao": proj["vidro_padrao"],
      "pecas_corte": pecas_corte,
      "area_liquida_total": area_liquida_total,
      "area_faturada_total": area_faturada_total,
      "custo_vidro": custo_vidro,
      "custo_kit": custo_kit,
      "custo_insumos": custo_insumos,
      "custo_mo": custo_mo,
      "custo_direto_total": custo_direto_total,
      "preco_venda_final": preco_venda_final,
      "lucro_bruto": lucro_bruto,
      "margem_lucro": margem_lucro,
  }


# ==============================================================================
# GERADOR DE PDF PROFISSIONAL COM SELEÇÃO DO TIPO DE DOCUMENTO
# ==============================================================================
def gerar_pdf_documento(tipo_doc, dados):
  buffer = io.BytesIO()
  doc = SimpleDocTemplate(
      buffer,
      pagesize=A4,
      leftMargin=1.5 * cm,
      rightMargin=1.5 * cm,
      topMargin=1.5 * cm,
      bottomMargin=1.5 * cm,
  )

  AZUL_NAVY = colors.HexColor("#0D253A")
  CINZA_FUNDO = colors.HexColor("#F8FAFC")
  CINZA_TEXTO = colors.HexColor("#0D253A")
  CINZA_BORDA = colors.HexColor("#CBD5E1")
  BRANCO = colors.white

  styles = getSampleStyleSheet()

  style_title = ParagraphStyle(
      "Title",
      parent=styles["Normal"],
      fontName="Helvetica-Bold",
      fontSize=18,
      leading=22,
      textColor=AZUL_NAVY,
      alignment=1,
  )
  style_sub = ParagraphStyle(
      "Sub",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=9,
      leading=12,
      textColor=colors.HexColor("#64748B"),
      alignment=1,
  )
  style_doc_type = ParagraphStyle(
      "DocType",
      parent=styles["Normal"],
      fontName="Helvetica-Bold",
      fontSize=12,
      leading=15,
      textColor=AZUL_NAVY,
      alignment=1,
  )
  style_card = ParagraphStyle(
      "Card",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=8.5,
      leading=12,
      textColor=CINZA_TEXTO,
  )
  style_th = ParagraphStyle(
      "TH",
      parent=styles["Normal"],
      fontName="Helvetica-Bold",
      fontSize=8.5,
      leading=11,
      textColor=BRANCO,
  )
  style_td = ParagraphStyle(
      "TD",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=8.5,
      leading=11,
      textColor=CINZA_TEXTO,
  )
  style_td_r = ParagraphStyle(
      "TDR", parent=style_td, alignment=2, fontName="Helvetica-Bold"
  )

  story = []
  story.append(Paragraph("<b>HOPINESS PROJECT</b>", style_title))
  story.append(
      Paragraph(
          "Vidraçaria e Engenharia de Vidros Planos | WhatsApp: (81) 98888-7777",
          style_sub,
      )
  )
  story.append(Spacer(1, 0.2 * cm))

  titulo_documento = (
      "PROPOSTA COMERCIAL E ORÇAMENTO"
      if tipo_doc == "orcamento"
      else (
          "PEDIDO DE CORTE PARA TÊMPERA / BENEFICIAMENTO"
          if tipo_doc == "tempera"
          else "RECIBO E TERMO DE GARANTIA DE SERVIÇO"
      )
  )
  story.append(Paragraph(f"<b>{titulo_documento}</b>", style_doc_type))
  story.append(
      HRFlowable(
          width="100%",
          thickness=1.5,
          color=AZUL_NAVY,
          spaceBefore=4,
          spaceAfter=8,
      )
  )

  # Dados do Cabeçalho
  info_data = [[
      Paragraph(
          f"<b>CLIENTE:</b> {dados['cliente']}<br/><b>CONTATO:</b>"
          f" {dados['telefone']}<br/><b>LOCAL:</b> {dados['local']}",
          style_card,
      ),
      Paragraph(
          f"<b>PROJETO:</b> {dados['projeto_nome']}<br/><b>VÃO REAL:</b>"
          f" {dados['largura_vao']:.2f}m (L) x {dados['altura_vao']:.2f}m"
          f" (A)<br/><b>DATA:</b> {datetime.now().strftime('%d/%m/%Y')}",
          style_card,
      ),
  ]]
  t_info = Table(info_data, colWidths=[9.0 * cm, 9.0 * cm])
  t_info.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, -1), CINZA_FUNDO),
          ("BOX", (0, 0), (-1, -1), 0.8, CINZA_BORDA),
          ("TOPPADDING", (0, 0), (-1, -1), 6),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
          ("LEFTPADDING", (0, 0), (-1, -1), 8),
          ("RIGHTPADDING", (0, 0), (-1, -1), 8),
      ])
  )
  story.append(t_info)
  story.append(Spacer(1, 0.35 * cm))

  # CONTEÚDO ESPECÍFICO DE CADA DOCUMENTO (IGUAL AO MEU VIDRACEIRO)
  if tipo_doc == "tempera":
    story.append(
        Paragraph("<b>MEDIDAS EXATAS DE CORTE DAS PEÇAS:</b>", style_card)
    )
    story.append(Spacer(1, 0.15 * cm))
    rows_tempera = [[
        Paragraph("Item / Peça", style_th),
        Paragraph("Largura (m)", style_th),
        Paragraph("Altura (m)", style_th),
        Paragraph("Qtd", style_th),
        Paragraph("Espessura / Tipo de Vidro", style_th),
    ]]
    for idx, pc in enumerate(dados["pecas_corte"], start=1):
      rows_tempera.append([
          Paragraph(f"{idx}. {pc['peca']}", style_td),
          Paragraph(f"{pc['largura_corte']:.3f} m", style_td),
          Paragraph(f"{pc['altura_corte']:.3f} m", style_td),
          Paragraph(str(pc["qtd"]), style_td),
          Paragraph(dados["vidro_padrao"], style_td),
      ])
    t_temp = Table(
        rows_tempera, colWidths=[5.5 * cm, 2.5 * cm, 2.5 * cm, 1.5 * cm, 6.0 * cm]
    )
    t_temp.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), AZUL_NAVY),
            ("GRID", (0, 0), (-1, -1), 0.5, CINZA_BORDA),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BRANCO, CINZA_FUNDO]),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ])
    )
    story.append(t_temp)
    story.append(Spacer(1, 0.4 * cm))
    story.append(
        Paragraph(
            "<i>* Observação para a fábrica: Peças com lapidação com cantos e"
            " furações padrão conforme catálogo.</i>",
            style_sub,
        )
    )

  elif tipo_doc == "orcamento":
    rows_orc = [
        [
            Paragraph("Item / Discriminação do Serviço", style_th),
            Paragraph("Subtotal", ParagraphStyle("THR", parent=style_th, alignment=2)),
        ],
        [
            Paragraph(
                f"Vidros Lapidados ({dados['vidro_padrao']}) - Área Fat:"
                f" {dados['area_faturada_total']:.2f} m²",
                style_td,
            ),
            Paragraph(f"R$ {dados['custo_vidro']:.2f}", style_td_r),
        ],
        [
            Paragraph(
                "Kits de Alumínio, Perfis Estruturais e Ferragens", style_td
            ),
            Paragraph(f"R$ {dados['custo_kit']:.2f}", style_td_r),
        ],
        [
            Paragraph(
                "Insumos de Vedação (Silicones e Fixadores Industriais)",
                style_td,
            ),
            Paragraph(f"R$ {dados['custo_insumos']:.2f}", style_td_r),
        ],
        [
            Paragraph(
                "Mão de Obra de Instalação, Nivelamento e Transporte", style_td
            ),
            Paragraph(f"R$ {dados['custo_mo']:.2f}", style_td_r),
        ],
    ]
    t_orc = Table(rows_orc, colWidths=[13.5 * cm, 4.5 * cm])
    t_orc.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), AZUL_NAVY),
            ("GRID", (0, 0), (-1, -1), 0.5, CINZA_BORDA),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BRANCO, CINZA_FUNDO]),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ])
    )
    story.append(t_orc)
    story.append(Spacer(1, 0.4 * cm))

    fechamento_data = [[
        Paragraph(
            "<b>Condições de Pagamento:</b> 50% no sinal e saldo na conclusão.<br/>Desconto de 5% no Pix.<br/>Garantia: 1 ano contra defeitos de instalação.",
            style_card,
        ),
        Paragraph(
            "<font size='8' color='#64748B'>VALOR TOTAL DA"
            " PROPOSTA</font><br/><font size='15'"
            f" color='#0D253A'><b>R$ {dados['preco_venda_final']:.2f}</b></font>",
            style_td_r,
        ),
    ]]
    t_fech = Table(fechamento_data, colWidths=[11.5 * cm, 6.5 * cm])
    t_fech.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CINZA_FUNDO),
            ("BOX", (0, 0), (-1, -1), 1.0, AZUL_NAVY),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    story.append(t_fech)

  elif tipo_doc == "recibo":
    recibo_data = [
        [
            Paragraph(
                f"Declaramos que recebemos de <b>{dados['cliente']}</b> o valor"
                " referente aos serviços contratados abaixo especificados, com"
                " quitação das obrigações nos termos acordados.",
                style_card,
            )
        ],
        [
            Paragraph(
                f"<b>Valor Quitado:</b> R$ {dados['preco_venda_final']:.2f} |"
                f" <b>Obra:</b> {dados['local']}",
                style_card,
            )
        ],
    ]
    t_rec = Table(recibo_data, colWidths=[18.0 * cm])
    t_rec.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CINZA_FUNDO),
            ("BOX", (0, 0), (-1, -1), 0.8, AZUL_NAVY),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ])
    )
    story.append(t_rec)
    story.append(Spacer(1, 0.6 * cm))

    # Assinatura
    rodape_data = [[
        Paragraph(
            "____________________________________________________<br/><b>Hopeness"
            " Vidraçaria</b>",
            ParagraphStyle("A1", alignment=1),
        ),
        Paragraph(
            "____________________________________________________<br/><b>Assinatura"
            " do Cliente</b>",
            ParagraphStyle("A2", alignment=1),
        ),
    ]]
    t_rod = Table(rodape_data, colWidths=[9.0 * cm, 9.0 * cm])
    story.append(KeepTogether(t_rod))

  doc.build(story)
  pdf_bytes = buffer.getvalue()
  buffer.close()
  return pdf_bytes


# ==============================================================================
# INTERFACE PRINCIPAL MULTI-MÓDULO
# ==============================================================================
aba_projetos, aba_tempera, aba_financeiro, aba_abnt = st.tabs([
    "📐 Projetos Padrão & Orçamento",
    "🏭 Pedido de Têmpera (Corte)",
    "💵 Financeiro da Obra",
    "📋 Catálogo Técnico ABNT",
])

# ------------------------------------------------------------------------------
# ABA 1: PROJETOS PADRÃO & ORÇAMENTO RÁPIDO
# ------------------------------------------------------------------------------
with aba_projetos:
  st.markdown(
      "<h3 style='color:#0D253A;'>Selecione o Projeto Padrão da Obra</h3>",
      unsafe_allow_html=True,
  )

  col_proj1, col_proj2 = st.columns([2, 1])
  with col_proj1:
    escolha_projeto = st.selectbox(
        "Tipo de Obra / Tipologia:",
        options=list(PROJETOS_PADRAO.keys()),
        format_func=lambda x: (
            f"{PROJETOS_PADRAO[x]['categoria']} — {PROJETOS_PADRAO[x]['nome']}"
        ),
    )
  with col_proj2:
    st.info(
        f"**Norma:** {PROJETOS_PADRAO[escolha_projeto]['norma']}\n\n**Vidro"
        f" Recomendado:** {PROJETOS_PADRAO[escolha_projeto]['vidro_padrao']}"
    )

  st.markdown("---")
  st.markdown(
      "<h4 style='color:#0D253A;'>1. Dados do Cliente e Medidas do Vão</h4>",
      unsafe_allow_html=True,
  )

  c_cli1, c_cli2, c_cli3 = st.columns(3)
  cli_nome = c_cli1.text_input("Nome do Cliente", "Mariana Albuquerque")
  cli_whats = c_cli2.text_input("WhatsApp (com DDD)", "81991234567")
  cli_local = c_cli3.text_input("Endereço / Local", "Boa Viagem - Recife/PE")

  c_m1, c_m2, c_m3 = st.columns(3)
  largura_input = c_m1.number_input(
      "Largura do Vão (m)", min_value=0.20, max_value=12.0, value=2.00, step=0.05
  )
  altura_input = c_m2.number_input(
      "Altura do Vão (m)", min_value=0.20, max_value=6.0, value=2.10, step=0.05
  )
  preco_m2_input = c_m3.number_input(
      "Custo m² do Vidro (R$)", min_value=10.0, value=190.0, step=10.0
  )

  st.markdown(
      "<h4 style='color:#0D253A;'>2. Custos Operacionais e Margem de"
      " Lucro</h4>",
      unsafe_allow_html=True,
  )
  c_c1, c_c2, c_c3, c_c4 = st.columns(4)
  custo_kit_input = c_c1.number_input(
      "Kits / Perfis Alumínio (R$)",
      value=PROJETOS_PADRAO[escolha_projeto]["custo_kit_base"],
      step=10.0,
  )
  custo_insumos_input = c_c2.number_input(
      "Insumos / Fixadores (R$)",
      value=PROJETOS_PADRAO[escolha_projeto]["custo_insumos_base"],
      step=5.0,
  )
  custo_mo_input = c_c3.number_input(
      "Mão de Obra e Instalação (R$)", value=250.0, step=10.0
  )
  margem_input = c_c4.slider(
      "Margem de Lucro Desejada (%)",
      min_value=10.0,
      max_value=70.0,
      value=35.0,
  )

  calc = calcular_projeto_completo(
      escolha_projeto,
      largura_input,
      altura_input,
      preco_m2_vidro=preco_m2_input,
      custo_kit=custo_kit_input,
      custo_insumos=custo_insumos_input,
      custo_mo=custo_mo_input,
      margem_lucro=margem_input,
  )

  st.markdown("---")
  st.markdown(
      "<h4 style='color:#0D253A;'>Resultado Comercial</h4>",
      unsafe_allow_html=True,
  )

  res1, res2, res3, res4 = st.columns(4)
  res1.metric("Área Real (Líquida)", f"{calc['area_liquida_total']:.2f} m²")
  res2.metric("Área Faturada (c/ Folgas)", f"{calc['area_faturada_total']:.2f} m²")
  res3.metric("Custo Direto Total", f"R$ {calc['custo_direto_total']:.2f}")
  res4.metric("Preço de Venda Sugerido", f"R$ {calc['preco_venda_final']:.2f}")

  st.success(
      f"**Lucro Bruto Estimado:** R$ {calc['lucro_bruto']:.2f} (Margem:"
      f" {calc['margem_lucro']}%)"
  )

  # Dados estruturados para gerar os documentos
  dados_doc = {
      "cliente": cli_nome,
      "telefone": cli_whats,
      "local": cli_local,
      "projeto_nome": calc["projeto_nome"],
      "largura_vao": largura_input,
      "altura_vao": altura_input,
      "vidro_padrao": calc["vidro_padrao"],
      "pecas_corte": calc["pecas_corte"],
      "area_faturada_total": calc["area_faturada_total"],
      "custo_vidro": calc["custo_vidro"],
      "custo_kit": calc["custo_kit"],
      "custo_insumos": calc["custo_insumos"],
      "custo_mo": calc["custo_mo"],
      "preco_venda_final": calc["preco_venda_final"],
  }

  btn_col1, btn_col2, btn_col3 = st.columns(3)

  with btn_col1:
    pdf_orc = gerar_pdf_documento("orcamento", dados_doc)
    st.download_button(
        "📄 Baixar Orçamento em PDF",
        data=pdf_orc,
        file_name=f"Orcamento_{cli_nome.replace(' ', '_')}.pdf",
        mime="application/pdf",
    )

  with btn_col2:
    pdf_rec = gerar_pdf_documento("recibo", dados_doc)
    st.download_button(
        "🧾 Baixar Recibo / Garantia",
        data=pdf_rec,
        file_name=f"Recibo_{cli_nome.replace(' ', '_')}.pdf",
        mime="application/pdf",
    )

  with btn_col3:
    msg = (
        f"Olá, {cli_nome}! Segue o orçamento para o seu projeto de"
        f" {calc['projeto_nome']}:\n\n📐 Vão: {largura_input:.2f}m x"
        f" {altura_input:.2f}m\n💎 Vidro: {calc['vidro_padrao']}\n💰 Valor"
        f" Total: R$ {calc['preco_venda_final']:.2f} (em até 3x sem juros ou"
        " 5% no Pix)\n\nFico no aguardo para agendarmos a medição fina!"
    )
    url_zap = f"https://api.whatsapp.com/send?phone=55{cli_whats.strip()}&text={urllib.parse.quote(msg)}"
    st.link_button("📲 Enviar via WhatsApp", url_zap)

# ------------------------------------------------------------------------------
# ABA 2: PEDIDO DE TÊMPERA (PLANO DE CORTE COM FOLGAS)
# ------------------------------------------------------------------------------
with aba_tempera:
  st.markdown(
      "<h3 style='color:#0D253A;'>Pedido Técnico para a Têmpera /"
      " Fornecedor</h3>",
      unsafe_allow_html=True,
  )
  st.write(
      "As folgas e descontos técnicos já foram aplicados automaticamente nas"
      " peças abaixo:"
  )

  tabela_cortes = []
  for p in calc["pecas_corte"]:
    tabela_cortes.append({
        "Peça / Componente": p["peca"],
        "Largura de Corte (m)": f"{p['largura_corte']:.3f}",
        "Altura de Corte (m)": f"{p['altura_corte']:.3f}",
        "Quantidade": p["qtd"],
        "Especificação": calc["vidro_padrao"],
    })
  st.table(tabela_cortes)

  pdf_temp = gerar_pdf_documento("tempera", dados_doc)
  st.download_button(
      "🏭 Baixar Pedido de Têmpera em PDF (Ordem de Corte)",
      data=pdf_temp,
      file_name=f"Pedido_Tempera_{cli_nome.replace(' ', '_')}.pdf",
      mime="application/pdf",
  )

# ------------------------------------------------------------------------------
# ABA 3: FINANCEIRO DA OBRA
# ------------------------------------------------------------------------------
with aba_financeiro:
  st.markdown(
      "<h3 style='color:#0D253A;'>Controle Financeiro da Obra</h3>",
      unsafe_allow_html=True,
  )

  f_col1, f_col2 = st.columns(2)
  with f_col1:
    sinal_pago = st.number_input(
        "Sinal Recebido (R$)",
        min_value=0.0,
        value=round(calc["preco_venda_final"] * 0.5, 2),
        step=50.0,
    )
  with f_col2:
    saldo_restante = calc["preco_venda_final"] - sinal_pago
    st.metric("Saldo Restante a Receber", f"R$ {saldo_restante:.2f}")

  st.markdown("#### Balanço Previsto:")
  b1, b2, b3 = st.columns(3)
  b1.metric("Valor Total Cobrado", f"R$ {calc['preco_venda_final']:.2f}")
  b2.metric("Custo Total de Materiais/MO", f"R$ {calc['custo_direto_total']:.2f}")
  b3.metric("Lucro Líquido Esperado", f"R$ {calc['lucro_bruto']:.2f}")

# ------------------------------------------------------------------------------
# ABA 4: CONSULTORIA ABNT
# ------------------------------------------------------------------------------
with aba_abnt:
  st.markdown(
      "<h3 style='color:#0D253A;'>Normas Técnicas Oficiais da Construção"
      " Civil</h3>",
      unsafe_allow_html=True,
  )
  st.markdown(
      """
    - **ABNT NBR 14207 (Box de Banheiro):** Exige vidro de segurança (temperado 8mm ou laminado). Recomenda película protetora[cite: 1].
    - **ABNT NBR 14718 (Guarda-Corpos):** Obrigatório vidro laminado ou laminado-temperado. **Proibido vidro temperado comum sem laminação**[cite: 1].
    - **ABNT NBR 7199 (Vidros em Geral):** Estabelece que vidros abaixo de 1,10m do piso, coberturas e claraboias devem ser vidros de segurança contra impactos e quedas[cite: 1].
    - **ABNT NBR 15198 (Espelhos):** Diretrizes para assentamento químico com fita estrutural e adesivo neutro para proteger a prata da oxidação[cite: 1].
    """
  )
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
# CONFIGURAÇÃO GERAL E CSS REFINADO
# ==============================================================================
st.set_page_config(
    page_title="HOPINESS PROJECT by Felipe Correa",
    page_icon="🪟",
    layout="wide",
)

st.markdown(
    """
    <style>
        /* 1. Fundo geral da aplicação */
        .stApp {
            background-color: #ECEFF1;
        }

        /* 2. Textos padrão da aplicação */
        p, span, label, .stMarkdown, .stCaption {
            color: #0D253A;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #0D253A !important;
            font-weight: 800 !important;
        }
        
        /* 3. CORREÇÃO DAS ABAS (FOTO 2: SEM NENHUMA BORDA RETANGULAR) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
            padding: 4px 0px;
            border: none !important;
            margin-bottom: 22px;
        }
        
        /* Barra de destaque inferior padrão do Streamlit removida */
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #0D253A !important;
            height: 3px !important;
            border-radius: 2px !important;
        }
        
        /* Guias Inativas: Sem borda, cor sutil e legível */
        .stTabs [data-baseweb="tab"] {
            color: #1E3A5F !important;
            background-color: transparent !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            padding: 10px 18px !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            transition: all 0.2s ease-in-out;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: #0D253A !important;
            background-color: rgba(13, 37, 58, 0.05) !important;
            border-radius: 6px !important;
        }
        
        /* Guia Ativa: Texto forte em Azul Marinho, 100% SEM BORDA */
        .stTabs [aria-selected="true"] {
            color: #0D253A !important;
            background-color: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }
        
        /* 4. CORREÇÃO DO SELECTBOX / DROPDOWN (FOTO 1: FONTE BRANCA E NÍTIDA) */
        div[data-baseweb="select"] > div {
            background-color: #1A202C !important;
            border: 1px solid #4A5568 !important;
            border-radius: 8px !important;
            color: #FFFFFF !important;
        }
        
        /* Texto selecionado dentro da caixa */
        div[data-baseweb="select"] * {
            color: #FFFFFF !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
        }
        
        /* Menu que abre (lista suspensa de opções) */
        ul[data-baseweb="menu"] {
            background-color: #1A202C !important;
            border: 1px solid #4A5568 !important;
            border-radius: 8px !important;
            padding: 6px !important;
        }
        
        /* Cada item da lista */
        ul[data-baseweb="menu"] li {
            color: #FFFFFF !important;
            background-color: transparent !important;
            font-weight: 500 !important;
            border-radius: 6px !important;
            padding: 10px 14px !important;
        }
        
        /* Item com mouse em cima ou selecionado na lista */
        ul[data-baseweb="menu"] li:hover,
        ul[data-baseweb="menu"] li[aria-selected="true"] {
            background-color: #2D3748 !important;
            color: #63B3ED !important;
        }

        /* 5. Inputs de texto e números */
        .stTextInput input, .stNumberInput input {
            background-color: #FFFFFF !important;
            color: #0D253A !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            border: 1px solid #CBD5E1 !important;
        }
        
        /* Cards Informativos */
        .custom-card {
            background-color: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 16px;
            box-shadow: 0 2px 5px rgba(13, 37, 58, 0.05);
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
        
        /* Botões */
        .stButton > button[kind="primary"] {
            background-color: #0D253A !important;
            color: #FFFFFF !important;
            border-radius: 8px;
            border: none;
            font-weight: 700;
            padding: 10px 24px;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #1E3A5F !important;
        }
        .stDownloadButton > button {
            background-color: #1E3A5F !important;
            color: #FFFFFF !important;
            border-radius: 8px;
            font-weight: 700;
            border: none;
        }

        /* Métricas */
        div[data-testid="stMetricValue"] {
            color: #0D253A !important;
            font-weight: 800 !important;
        }
        div[data-testid="stMetricLabel"] {
            color: #1E3A5F !important;
            font-weight: 700 !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# CABEÇALHO DO PROJETO
# ==============================================================================
st.markdown(
    """
    <div style="margin-top: -20px; margin-bottom: 22px; border-bottom: 2px solid #CBD5E1; padding-bottom: 12px;">
        <h1 style="text-align: center; color: #0D253A; font-size: 2.3rem; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; text-transform: uppercase;">
            HOPINESS PROJECT
        </h1>
        <p style="text-align: right; color: #1E3A5F; font-size: 0.95rem; font-weight: 600; font-style: italic; margin-top: 2px; margin-bottom: 0px; padding-right: 10px;">
            by Felipe Correa
        </p>
    </div>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# MOTOR TÉCNICO ABNT
# ==============================================================================
class RecomendadorTecnico:
  APLICACOES = {
      "1": "Box de Banheiro",
      "2": "Guarda-Corpo / Sacada",
      "3": "Cobertura / Clarabóia",
      "4": "Porta / Janela (Abaixo de 1,10m)",
      "5": "Divisória de Ambiente / Fechamento de Vão",
      "6": "Espelho Decorativo",
      "7": "Prateleira / Tampo de Mesa",
  }

  @staticmethod
  def recomendar(opcao_aplicacao: str) -> dict:
    recomendacoes = {
        "1": {
            "aplicacao": "Box de Banheiro",
            "vidros_permitidos": ["Temperado 8mm", "Laminado 8mm"],
            "norma_tecnica": "ABNT NBR 14207",
            "explicacao": (
                "Exige-se vidro de segurança[cite: 1]. O vidro temperado de 8mm oferece"
                " resistência mecânica e térmica adequada para área molhada."
            ),
        },
        "2": {
            "aplicacao": "Guarda-Corpo / Sacada",
            "vidros_permitidos": ["Laminado 10mm+", "Laminado-Temperado"],
            "norma_tecnica": "ABNT NBR 14718 / NBR 7199",
            "explicacao": (
                "Proibido vidro temperado monolítico[cite: 1]. Exige-se laminação com"
                " película de PVB para garantir retenção e impedir queda em"
                " altura[cite: 1]."
            ),
        },
        "3": {
            "aplicacao": "Cobertura / Clarabóia",
            "vidros_permitidos": [
                "Laminado",
                "Insulado (com lâmina inferior laminada)",
            ],
            "norma_tecnica": "ABNT NBR 7199",
            "explicacao": (
                "Obrigatório vidro laminado na face inferior para retenção de"
                " estilhaços suspensos em caso de quebra[cite: 1]."
            ),
        },
        "4": {
            "aplicacao": "Porta / Janela (Abaixo de 1,10m)",
            "vidros_permitidos": ["Temperado 8mm/10mm", "Laminado 8mm"],
            "norma_tecnica": "ABNT NBR 7199",
            "explicacao": (
                "Zona de impacto humano acidental[cite: 1]. Exige vidro de segurança"
                " conforme a cota de piso acabado[cite: 1]."
            ),
        },
        "5": {
            "aplicacao": "Divisória de Ambiente / Fechamento de Vão",
            "vidros_permitidos": ["Temperado 8mm/10mm", "Laminado"],
            "norma_tecnica": "ABNT NBR 7199",
            "explicacao": (
                "Vidro temperado confere alta rigidez estrutural para vãos"
                " amplos[cite: 1]."
            ),
        },
        "6": {
            "aplicacao": "Espelho Decorativo",
            "vidros_permitidos": ["Espelho Prata (com proteção química)"],
            "norma_tecnica": "ABNT NBR 15198",
            "explicacao": (
                "Fixação com adesivo neutro/silicone próprio para preservar a"
                " película de prata[cite: 1]."
            ),
        },
        "7": {
            "aplicacao": "Prateleira / Tampo de Mesa",
            "vidros_permitidos": ["Temperado", "Monolítico Lapidado"],
            "norma_tecnica": "Boas Práticas da Indústria",
            "explicacao": (
                "Dimensionamento proporcional aos apoios e carga de uso[cite: 1]."
            ),
        },
    }
    return recomendacoes.get(opcao_aplicacao, None)


# ==============================================================================
# CALCULADORA COMERCIAL (FOLGA DE 50MM)
# ==============================================================================
class CalculadoraOrcamento:
  STEP_COMERCIAL_M = 0.05

  @classmethod
  def arredondar_comercial(cls, medida_m: float) -> float:
    return math.ceil(medida_m / cls.STEP_COMERCIAL_M) * cls.STEP_COMERCIAL_M

  @classmethod
  def calcular_orcamento(
      cls,
      largura_m: float,
      altura_m: float,
      quantidade_folhas: int,
      preco_m2_vidro: float,
      custo_kits_ferragens: float,
      custo_insumos: float,
      custo_mao_de_obra: float,
      margem_lucro_pct: float,
  ) -> dict:
    largura_faturada = cls.arredondar_comercial(largura_m)
    altura_faturada = cls.arredondar_comercial(altura_m)

    area_liquida_total = (largura_m * altura_m) * quantidade_folhas
    area_faturada_total = (
        largura_faturada * altura_faturada
    ) * quantidade_folhas

    custo_vidro_total = area_faturada_total * preco_m2_vidro
    custo_direto_total = (
        custo_vidro_total
        + custo_kits_ferragens
        + custo_insumos
        + custo_mao_de_obra
    )

    if margem_lucro_pct >= 100:
      margem_lucro_pct = 99.0

    fator_margem = 1.0 - (margem_lucro_pct / 100.0)
    preco_venda_final = custo_direto_total / fator_margem
    lucro_bruto = preco_venda_final - custo_direto_total

    return {
        "dimensoes_reais": f"{largura_m:.2f}m x {altura_m:.2f}m",
        "dimensoes_faturadas": (
            f"{largura_faturada:.2f}m x {altura_faturada:.2f}m"
        ),
        "area_liquida_total": area_liquida_total,
        "area_faturada_total": area_faturada_total,
        "custo_vidro": custo_vidro_total,
        "custo_ferragens": custo_kits_ferragens,
        "custo_insumos": custo_insumos,
        "custo_mao_de_obra": custo_mao_de_obra,
        "custo_direto_total": custo_direto_total,
        "margem_aplicada_pct": margem_lucro_pct,
        "preco_venda_final": preco_venda_final,
        "lucro_bruto": lucro_bruto,
    }


# ==============================================================================
# GERADOR DE PDF PROFISSIONAL (REPORTLAB)
# ==============================================================================
def gerar_pdf_bytes(dados: dict) -> bytes:
  buffer = io.BytesIO()
  doc = SimpleDocTemplate(
      buffer,
      pagesize=A4,
      leftMargin=1.5 * cm,
      rightMargin=1.5 * cm,
      topMargin=1.5 * cm,
      bottomMargin=1.5 * cm,
  )

  AZUL_NAVY = colors.HexColor("#0D253A")
  CINZA_FUNDO = colors.HexColor("#F8FAFC")
  CINZA_TEXTO = colors.HexColor("#0D253A")
  CINZA_SUAVE = colors.HexColor("#1E3A5F")
  CINZA_BORDA = colors.HexColor("#CBD5E1")
  BRANCO = colors.white

  styles = getSampleStyleSheet()

  style_title = ParagraphStyle(
      "Title",
      parent=styles["Normal"],
      fontName="Helvetica-Bold",
      fontSize=18,
      leading=22,
      textColor=AZUL_NAVY,
      alignment=1,
  )
  style_sub_author = ParagraphStyle(
      "SubAuthor",
      parent=styles["Normal"],
      fontName="Helvetica-Oblique",
      fontSize=9.5,
      leading=13,
      textColor=CINZA_SUAVE,
      alignment=2,
  )
  style_meta = ParagraphStyle(
      "Meta",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=8.5,
      leading=12,
      alignment=2,
      textColor=CINZA_TEXTO,
  )
  style_card = ParagraphStyle(
      "Card",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=8.5,
      leading=12,
      textColor=CINZA_TEXTO,
  )
  style_th = ParagraphStyle(
      "TH",
      parent=styles["Normal"],
      fontName="Helvetica-Bold",
      fontSize=8.5,
      leading=11,
      textColor=BRANCO,
  )
  style_td = ParagraphStyle(
      "TD",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=8.5,
      leading=11,
      textColor=CINZA_TEXTO,
  )
  style_td_r = ParagraphStyle(
      "TDR",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=8.5,
      leading=11,
      alignment=2,
      textColor=CINZA_TEXTO,
  )

  story = []
  story.append(Paragraph("<b>HOPINESS PROJECT</b>", style_title))
  story.append(Spacer(1, 0.1 * cm))
  story.append(Paragraph("<i>by Felipe Correa</i>", style_sub_author))
  story.append(
      HRFlowable(
          width="100%",
          thickness=1.5,
          color=AZUL_NAVY,
          spaceBefore=4,
          spaceAfter=8,
      )
  )

  info_data = [[
      Paragraph(
          f"<b>CLIENTE:</b> {dados['cliente']}<br/><b>LOCAL:</b>"
          f" {dados['local']}",
          style_card,
      ),
      Paragraph(
          f"<b>AMBIENTE:</b> {dados['ambiente']}<br/><b>DIMENSÕES:</b>"
          f" {dados['dimensoes']} ({dados['folhas']} folha(s))<br/><b>ÁREA"
          f" FATURADA:</b> {dados['area_faturada']:.2f} m²",
          style_card,
      ),
  ]]
  t_info = Table(info_data, colWidths=[9.0 * cm, 9.0 * cm])
  t_info.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, -1), CINZA_FUNDO),
          ("BOX", (0, 0), (-1, -1), 0.8, CINZA_BORDA),
          ("TOPPADDING", (0, 0), (-1, -1), 6),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
          ("LEFTPADDING", (0, 0), (-1, -1), 8),
          ("RIGHTPADDING", (0, 0), (-1, -1), 8),
      ])
  )
  story.append(t_info)
  story.append(Spacer(1, 0.35 * cm))

  table_rows = [
      [
          Paragraph("Item / Discriminação do Serviço", style_th),
          Paragraph("Subtotal", ParagraphStyle("THR", parent=style_th, alignment=2)),
      ],
      [
          Paragraph("Vidros Planos Lapidados (com folga industrial)", style_td),
          Paragraph(f"R$ {dados['custo_vidro']:.2f}", style_td_r),
      ],
      [
          Paragraph("Kits de Instalação, Perfis e Ferragens", style_td),
          Paragraph(f"R$ {dados['custo_ferragens']:.2f}", style_td_r),
      ],
      [
          Paragraph("Insumos de Vedação e Fixadores Químicos", style_td),
          Paragraph(f"R$ {dados['custo_insumos']:.2f}", style_td_r),
      ],
      [
          Paragraph(
              "Mão de Obra Técnica Especializada e Nivelamento", style_td
          ),
          Paragraph(f"R$ {dados['custo_mo']:.2f}", style_td_r),
      ],
  ]
  t_itens = Table(table_rows, colWidths=[13.5 * cm, 4.5 * cm])
  t_itens.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, 0), AZUL_NAVY),
          ("GRID", (0, 0), (-1, -1), 0.5, CINZA_BORDA),
          ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BRANCO, CINZA_FUNDO]),
          ("TOPPADDING", (0, 0), (-1, -1), 5),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
          ("LEFTPADDING", (0, 0), (-1, -1), 8),
          ("RIGHTPADDING", (0, 0), (-1, -1), 8),
      ])
  )
  story.append(t_itens)
  story.append(Spacer(1, 0.4 * cm))

  fechamento_data = [[
      Paragraph(
          "<b>CONDIÇÕES COMERCIAIS:</b><br/>• 50% entrada + saldo em até 3x no"
          " cartão.<br/>• Desconto de 5% para pagamento via Pix.<br/>• Prazo:"
          " 10 a 15 dias úteis após medição fina.",
          style_card,
      ),
      Paragraph(
          "<font size='8' color='#1E3A5F'>VALOR TOTAL DA PROPOSTA</font><br/>"
          f"<font size='15' color='#0D253A'><b>R$"
          f" {dados['preco_final']:.2f}</b></font><br/>"
          "<font size='8' color='#1E3A5F'><b>Instalação inclusa</b></font>",
          style_meta,
      ),
  ]]
  t_fech = Table(fechamento_data, colWidths=[11.5 * cm, 6.5 * cm])
  t_fech.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, -1), CINZA_FUNDO),
          ("BOX", (0, 0), (-1, -1), 1.0, AZUL_NAVY),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 6),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
          ("LEFTPADDING", (0, 0), (-1, -1), 10),
          ("RIGHTPADDING", (0, 0), (-1, -1), 10),
      ])
  )
  story.append(t_fech)

  doc.build(story)
  pdf_bytes = buffer.getvalue()
  buffer.close()
  return pdf_bytes


# ==============================================================================
# INTERFACE PRINCIPAL
# ==============================================================================
aba_catalogo, aba_abnt, aba_orcamento, aba_os = st.tabs([
    "🪟 Catálogo & Guia Visual",
    "📋 Consultoria ABNT",
    "💰 Calculadora & WhatsApp",
    "📦 Gestão de Pedidos (OS)",
])

# ------------------------------------------------------------------------------
# ABA 1: CATÁLOGO E GUIA VISUAL DE VIDROS
# ------------------------------------------------------------------------------
with aba_catalogo:
  st.markdown(
      "<h3 style='color:#0D253A;'>Guia Visual: Tipos de Vidros e Suas"
      " Aplicações</h3>",
      unsafe_allow_html=True,
  )
  st.write(
      "Apresente aos clientes as características de cada composição para apoiar"
      " a decisão de compra."
  )

  col1, col2 = st.columns(2)

  with col1:
    st.markdown(
        """
        <div class="custom-card">
            <div class="custom-card-title">🔹 Vidro Temperado</div>
            <div class="custom-card-desc">
                <b>Resistência:</b> 5x mais resistente que o vidro comum.<br/>
                <b>Padrão de Quebra:</b> Fragmenta-se em pequenos pedaços pouco cortantes.<br/>
                <b>Aplicações Principais:</b> Box de banheiro, portas, divisórias e tampos.
            </div>
        </div>
        <div class="custom-card">
            <div class="custom-card-title">🔹 Vidro Laminado (Segurança Máxima)</div>
            <div class="custom-card-desc">
                <b>Composição:</b> Duas ou mais lâminas unidas por película de PVB.<br/>
                <b>Padrão de Quebra:</b> Os fragmentos ficam retidos na película sem abrir o vão.<br/>
                <b>Aplicações Principais:</b> Guarda-corpos, sacadas, coberturas e claraboias.
            </div>
        </div>
        <div class="custom-card">
            <div class="custom-card-title">🔹 Vidro Insulado / Duplo</div>
            <div class="custom-card-desc">
                <b>Estrutura:</b> Dupla lâmina com câmara de ar ou gás desidratado.<br/>
                <b>Destaque:</b> Máximo isolamento acústico contra ruídos e controle térmico.<br/>
                <b>Aplicações Principais:</b> Fachadas, estúdios e residências em avenidas movimentadas.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col2:
    st.markdown(
        """
        <div class="custom-card">
            <div class="custom-card-title">🔹 Vidros de Controle Solar (Reflecta / Low-E)</div>
            <div class="custom-card-desc">
                <b>Benefício:</b> Bloqueia até 70% da entrada de calor e 99% dos raios UV.<br/>
                <b>Destaque:</b> Mantém o ambiente fresco e protege pisos de madeira e móveis.<br/>
                <b>Aplicações Principais:</b> Sacadas poentes, coberturas e fachadas ensolaradas.
            </div>
        </div>
        <div class="custom-card">
            <div class="custom-card-title">🔹 Vidros Acidados & Serigrafados</div>
            <div class="custom-card-desc">
                <b>Acabamento:</b> Translúcido e fosco toque de seda.<br/>
                <b>Destaque:</b> Não engordura com facilidade e garante privacidade com luz natural.<br/>
                <b>Aplicações Principais:</b> Portas de armário, divisórias de escritório e lavabos.
            </div>
        </div>
        <div class="custom-card">
            <div class="custom-card-title">🔹 Espelhos com Camada Protetora</div>
            <div class="custom-card-desc">
                <b>Composição:</b> Base de prata pura com película ecológica protetora.<br/>
                <b>Destaque:</b> Alta durabilidade contra oxidação e manchas pretas nas bordas.<br/>
                <b>Aplicações Principais:</b> Banheiros, painéis de sala, academias e closets.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------------------
# ABA 2: CONSULTORIA ABNT
# ------------------------------------------------------------------------------
with aba_abnt:
  st.markdown(
      "<h3 style='color:#0D253A;'>Diagnóstico de Conformidade Normativa"
      " (ABNT)</h3>",
      unsafe_allow_html=True,
  )
  opcao = st.selectbox(
      "Selecione o local onde o vidro será instalado:",
      options=list(RecomendadorTecnico.APLICACOES.keys()),
      format_func=lambda x: RecomendadorTecnico.APLICACOES[x],
  )
  rec = RecomendadorTecnico.recomendar(opcao)
  if rec:
    c1, c2 = st.columns(2)
    c1.metric("Norma Regulamentadora", rec["norma_tecnica"])
    c2.metric("Vidro Obrigatório / Indicado", ", ".join(rec["vidros_permitidos"]))
    st.info(f"🛡️ **Diretriz Técnica de Segurança:** {rec['explicacao']}")

# ------------------------------------------------------------------------------
# ABA 3: CALCULADORA & ORÇAMENTO & WHATSAPP
# ------------------------------------------------------------------------------
with aba_orcamento:
  st.markdown(
      "<h3 style='color:#0D253A;'>Gerador Comercial de Proposta e PDF</h3>",
      unsafe_allow_html=True,
  )

  col_cli1, col_cli2, col_cli3 = st.columns(3)
  cliente_nome = col_cli1.text_input("Nome do Cliente", "Mariana Albuquerque")
  cliente_whats = col_cli2.text_input(
      "WhatsApp (com DDD)", "81991234567", help="Apenas números com DDD"
  )
  cliente_local = col_cli3.text_input(
      "Local da Instalação", "Boa Viagem - Recife/PE"
  )

  c1, c2 = st.columns(2)
  with c1:
    st.markdown("##### 1. Medidas do Vão")
    largura = st.number_input(
        "Largura do vão (m)",
        min_value=0.1,
        max_value=10.0,
        value=3.40,
        step=0.05,
    )
    altura = st.number_input(
        "Altura do vão (m)",
        min_value=0.1,
        max_value=10.0,
        value=1.10,
        step=0.05,
    )
    folhas = st.number_input(
        "Quantidade de Folhas/Peças", min_value=1, max_value=20, value=3
    )
    preco_m2 = st.number_input(
        "Custo do Vidro/m² (R$)", min_value=0.0, value=380.0, step=10.0
    )

  with c2:
    st.markdown("##### 2. Ferragens, Instalação e Margem")
    custo_kits = st.number_input(
        "Kits / Ferragens (R$)", min_value=0.0, value=570.0, step=10.0
    )
    custo_insumos = st.number_input(
        "Insumos / Fixadores (R$)", min_value=0.0, value=120.0, step=5.0
    )
    custo_mo = st.number_input(
        "Mão de Obra e Instalação (R$)", min_value=0.0, value=450.0, step=10.0
    )
    margem = st.slider(
        "Margem de Lucro Desejada (%)",
        min_value=5.0,
        max_value=70.0,
        value=35.0,
    )

  if st.button("Calcular Orçamento Completo", type="primary"):
    res = CalculadoraOrcamento.calcular_orcamento(
        largura,
        altura,
        folhas,
        preco_m2,
        custo_kits,
        custo_insumos,
        custo_mo,
        margem,
    )

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Área Real", f"{res['area_liquida_total']:.2f} m²")
    m2.metric("Área Faturada (+Folga)", f"{res['area_faturada_total']:.2f} m²")
    m3.metric("Custo Direto", f"R$ {res['custo_direto_total']:.2f}")
    m4.metric("Preço Sugerido", f"R$ {res['preco_venda_final']:.2f}")

    st.success(
        f"**Lucro Bruto Estimado:** R$ {res['lucro_bruto']:.2f} (Margem:"
        f" {res['margem_aplicada_pct']}%)"
    )

    dados_pdf = {
        "cliente": cliente_nome,
        "local": cliente_local,
        "ambiente": RecomendadorTecnico.APLICACOES[opcao],
        "dimensoes": res["dimensoes_reais"],
        "folhas": folhas,
        "area_faturada": res["area_faturada_total"],
        "custo_vidro": res["custo_vidro"],
        "custo_ferragens": res["custo_ferragens"],
        "custo_insumos": res["custo_insumos"],
        "custo_mo": res["custo_mao_de_obra"],
        "preco_final": res["preco_venda_final"],
    }

    pdf_bytes = gerar_pdf_bytes(dados_pdf)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
      st.download_button(
          label="📥 Baixar Orçamento em PDF (Página Única)",
          data=pdf_bytes,
          file_name=f"Orcamento_Hopiness_{cliente_nome.replace(' ', '_')}.pdf",
          mime="application/pdf",
      )

    with col_btn2:
      msg_whats = (
          f"Olá, {cliente_nome}! Segue a proposta comercial preparada pela"
          f" Hopiness para o seu projeto de"
          f" {RecomendadorTecnico.APLICACOES[opcao]}.\n\n"
          f"📐 Dimensões: {res['dimensoes_reais']} ({folhas} folhas)\n"
          f"💰 Valor Total: R$ {res['preco_venda_final']:.2f} (com instalação"
          " inclusa)\n"
          "🛡️ Especificação 100% em conformidade com as normas ABNT[cite: 1].\n\n"
          "Estou anexando o PDF detalhado da proposta para sua aprovação!"
      )
      link_whats = f"https://api.whatsapp.com/send?phone=55{cliente_whats.strip()}&text={urllib.parse.quote(msg_whats)}"
      st.link_button("📲 Enviar Mensagem via WhatsApp", link_whats)

# ------------------------------------------------------------------------------
# ABA 4: PIPELINE KANBAN DE ORDENS DE SERVIÇO
# ------------------------------------------------------------------------------
with aba_os:
  st.markdown(
      "<h3 style='color:#0D253A;'>Acompanhamento de Ordens de Serviço (OS)</h3>",
      unsafe_allow_html=True,
  )
  st.write(
      "Fluxo operacional desde a aprovação até a conclusão da instalação na"
      " obra."
  )

  c_k1, c_k2, c_k3, c_k4 = st.columns(4)

  with c_k1:
    st.markdown(
        """
        <div style="background-color:#E2E8F0; padding:10px; border-radius:8px; text-align:center; font-weight:800; color:#0D253A; margin-bottom:10px;">
            🟡 Orçamento Aberto (2)
        </div>
        <div class="custom-card">
            <b style="color:#0D253A;">#1024 - Carlos Silva</b><br/>
            Box Elegance Incolor 8mm<br/>
            <small style="color:#1E3A5F;">Aguardando retorno do cliente</small>
        </div>
        <div class="custom-card">
            <b style="color:#0D253A;">#1025 - Ed. Costa Dourada</b><br/>
            Espelho Prata Bisotado 4mm<br/>
            <small style="color:#1E3A5F;">Enviado via WhatsApp hoje</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with c_k2:
    st.markdown(
        """
        <div style="background-color:#FED7AA; padding:10px; border-radius:8px; text-align:center; font-weight:800; color:#9A3412; margin-bottom:10px;">
            🟠 Pedido na Têmpera (1)
        </div>
        <div class="custom-card">
            <b style="color:#0D253A;">#1022 - Roberta Maia</b><br/>
            Vidro Laminado 10mm (Guarda-Corpo)<br/>
            <small style="color:#1E3A5F;">Previsão de entrega: 2 dias</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with c_k3:
    st.markdown(
        """
        <div style="background-color:#BAE6FD; padding:10px; border-radius:8px; text-align:center; font-weight:800; color:#0369A1; margin-bottom:10px;">
            🔵 Rota de Instalação (1)
        </div>
        <div class="custom-card">
            <b style="color:#0D253A;">#1020 - Mariana Albuquerque</b><br/>
            Sacada Completa c/ Torres Inox<br/>
            <small style="color:#1E3A5F;">Equipe em deslocamento</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with c_k4:
    st.markdown(
        """
        <div style="background-color:#BBF7D0; padding:10px; border-radius:8px; text-align:center; font-weight:800; color:#166534; margin-bottom:10px;">
            🟢 Concluído & Faturado (4)
        </div>
        <div class="custom-card">
            <b style="color:#0D253A;">#1018 - Escritório Pina</b><br/>
            Divisória Acústica 10mm<br/>
            <small style="color:#166534;"><b>Saldo 100% quitado</b></small>
        </div>
        """,
        unsafe_allow_html=True,
    )

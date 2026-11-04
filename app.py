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

st.set_page_config(
    page_title="HOPINESS PROJECT by Felipe Correa",
    page_icon="🪟",
    layout="wide",
)

# 1. Carregamento da Logo (vdr.jpeg)
logo_b64 = ""
for arq in ["vdr.jpeg", "vdr.jpg", "logo.png", "logo.jpeg"]:
    if os.path.exists(arq):
        with open(arq, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        break

if logo_b64:
    logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}" style="width:68px;height:68px;border-radius:50%;object-fit:cover;display:block;border:none;outline:none;mix-blend-mode:multiply;">'
else:
    logo_html = '<div style="width:64px;height:64px;background-color:#5A5A5A;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#FFFFFF;font-size:8.5px;font-weight:900;text-align:center;">RIO<br/>BRANCO</div>'

# 2. CSS Global com degradê e estilização dos módulos
css_rules = [
    "<style>",
    "/* DEGRADÊ NA PÁGINA INTEIRA */",
    "html, body, [data-testid='stAppViewContainer'], .stApp, section.main {",
    "background: linear-gradient(160deg, #FADBD8 0%, #FFFFFF 35%, #FDE8E7 70%, #FFFFFF 100%) !important;",
    "background-attachment: fixed !important;",
    "}",
    "p, span, label, .stMarkdown {",
    "color: #5A5A5A !important;",
    "font-weight: 600;",
    "}",
    "/* CARDS DO MENU PRINCIPAL */",
    ".menu-card-container {",
    "background-color: #FFFFFF;",
    "border-radius: 12px;",
    "border: 1px solid #CBD5E1;",
    "box-shadow: 0 4px 15px rgba(0,0,0,0.06);",
    "margin-bottom: 20px;",
    "overflow: visible;",
    "position: relative;",
    "margin-top: 25px;",
    "}",
    ".menu-card-header {",
    "background-color: #D01B13;",
    "color: #FFFFFF !important;",
    "padding: 16px 20px;",
    "border-top-left-radius: 11px;",
    "border-top-right-radius: 11px;",
    "display: flex;",
    "align-items: center;",
    "justify-content: center;",
    "position: relative;",
    "min-height: 54px;",
    "}",
    ".menu-card-icon-badge {",
    "position: absolute;",
    "top: -24px;",
    "left: 20px;",
    "width: 48px;",
    "height: 48px;",
    "border-radius: 50%;",
    "background-color: #9D201C;",
    "color: #FFFFFF;",
    "display: flex;",
    "align-items: center;",
    "justify-content: center;",
    "font-size: 1.3rem;",
    "box-shadow: 0 4px 8px rgba(0,0,0,0.18);",
    "border: 3px solid #FFFFFF;",
    "}",
    ".menu-card-title {",
    "color: #FFFFFF !important;",
    "font-size: 1.25rem;",
    "font-weight: 800;",
    "margin: 0;",
    "text-align: center;",
    "letter-spacing: 0.5px;",
    "}",
    ".card-action-btn button {",
    "border-radius: 20px !important;",
    "padding: 6px 14px !important;",
    "font-weight: 800 !important;",
    "border: 2px solid #D01B13 !important;",
    "background-color: #FFFFFF !important;",
    "color: #D01B13 !important;",
    "box-shadow: 0 2px 5px rgba(208, 27, 19, 0.1) !important;",
    "width: 100% !important;",
    "}",
    ".card-action-btn button * {",
    "color: #D01B13 !important;",
    "font-weight: 800 !important;",
    "font-size: 0.9rem !important;",
    "}",
    ".card-action-btn button:hover {",
    "background-color: #D01B13 !important;",
    "color: #FFFFFF !important;",
    "}",
    ".card-action-btn button:hover * {",
    "color: #FFFFFF !important;",
    "}",
    "/* CARDS DA LISTA DE ORÇAMENTOS (ESTILO DO ANEXO) */",
    ".orc-card {",
    "background-color: #FFFFFF;",
    "border-radius: 10px;",
    "border: 1px solid #E2E8F0;",
    "box-shadow: 0 3px 12px rgba(0,0,0,0.05);",
    "padding: 16px 16px 12px 16px;",
    "margin-bottom: 20px;",
    "position: relative;",
    "}",
    ".status-badge {",
    "display: inline-flex;",
    "align-items: center;",
    "gap: 5px;",
    "padding: 4px 10px;",
    "border-radius: 14px;",
    "font-size: 0.78rem;",
    "font-weight: 700;",
    "}",
    ".status-badge-analise { background-color: #FEF3C7; color: #B45309; }",
    ".status-badge-aprovado { background-color: #D1FAE5; color: #047857; }",
    ".status-badge-reprovado { background-color: #FEE2E2; color: #B91C1C; }",
    ".status-badge-concluido { background-color: #E0E7FF; color: #3730A3; }",
    ".orc-card-title {",
    "color: #1E293B !important;",
    "font-size: 1.05rem;",
    "font-weight: 800;",
    "margin-top: 10px;",
    "margin-bottom: 3px;",
    "}",
    ".orc-card-sub {",
    "color: #64748B;",
    "font-size: 0.78rem;",
    "font-weight: 600;",
    "margin-bottom: 12px;",
    "}",
    "/* BOTÃO VOLTAR */",
    ".btn-voltar button {",
    "background-color: #5A5A5A !important;",
    "color: #FFFFFF !important;",
    "border-radius: 20px !important;",
    "font-weight: 800 !important;",
    "border: none !important;",
    "padding: 8px 22px !important;",
    "margin-bottom: 15px !important;",
    "}",
    ".btn-voltar button * {",
    "color: #FFFFFF !important;",
    "font-weight: 800 !important;",
    "}",
    "/* CARDS DE MÉTRICAS */",
    ".metric-card {",
    "background-color: #FFFFFF;",
    "border: 1px solid #E2E8F0;",
    "border-radius: 12px;",
    "padding: 18px 15px;",
    "text-align: center;",
    "box-shadow: 0 3px 10px rgba(0,0,0,0.04);",
    "margin-bottom: 15px;",
    "}",
    ".metric-card-label {",
    "color: #5A5A5A;",
    "font-size: 0.92rem;",
    "font-weight: 700;",
    "margin-bottom: 6px;",
    "}",
    ".metric-card-val {",
    "color: #9D201C;",
    "font-size: 1.85rem;",
    "font-weight: 900;",
    "margin: 0;",
    "}",
    "/* INPUTS */",
    ".stTextInput input, .stNumberInput input {",
    "background-color: #FFFFFF !important;",
    "color: #9D201C !important;",
    "font-weight: 800 !important;",
    "border-radius: 8px !important;",
    "border: 1px solid #CBD5E1 !important;",
    "}",
    "div[data-baseweb='select'] > div {",
    "background-color: #FFFFFF !important;",
    "border: 1px solid #CBD5E1 !important;",
    "border-radius: 8px !important;",
    "}",
    "div[data-baseweb='select'] * {",
    "color: #0D253A !important;",
    "font-weight: 700 !important;",
    "}",
    "/* BOTÕES DE AÇÃO INFERIORES */",
    ".btn-gerar button {",
    "background-color: #D01B13 !important;",
    "color: #FFFFFF !important;",
    "border-radius: 25px !important;",
    "font-weight: 800 !important;",
    "padding: 12px 28px !important;",
    "border: none !important;",
    "box-shadow: 0 4px 10px rgba(208,27,19,0.3) !important;",
    "width: 100% !important;",
    "}",
    ".btn-gerar button * {",
    "color: #FFFFFF !important;",
    "font-weight: 800 !important;",
    "}",
    ".btn-pdf button {",
    "background-color: #2D3748 !important;",
    "color: #FFFFFF !important;",
    "border-radius: 25px !important;",
    "font-weight: 800 !important;",
    "padding: 12px 28px !important;",
    "border: none !important;",
    "width: 100% !important;",
    "}",
    ".btn-pdf button * {",
    "color: #FFFFFF !important;",
    "font-weight: 800 !important;",
    "}",
    "</style>",
]

st.markdown("\n".join(css_rules), unsafe_allow_html=True)

# 3. Cabeçalho IDÊNTICO ao seu código (com título #9D201C vermelho escuro)
cabecalho_raw = f"""<div style="position:relative;background:rgba(255,255,255,0.45);backdrop-filter:blur(6px);border:1px solid rgba(226,232,240,0.9);border-left:8px solid #D01B13;border-radius:12px;padding:14px 24px;margin-top:-15px;margin-bottom:22px;box-shadow:0 4px 15px rgba(208,27,19,0.08);overflow:hidden;min-height:98px;">
<div style="position:relative;z-index:2;display:flex;align-items:center;justify-content:space-between;width:100%;">
<div style="flex-shrink:0;">{logo_html}</div>
<div style="text-align:center;flex-grow:1;">
<span style="color:#9D201C !important;-webkit-text-fill-color:#9D201C !important;font-size:2.35rem;font-weight:900;letter-spacing:2.5px;text-transform:uppercase;font-family:'Segoe UI',sans-serif;display:inline-block;">HOPINESS PROJECT</span>
</div>
<div style="flex-shrink:0;">
<span style="color:#5A5A5A;font-size:0.95rem;font-weight:600;font-style:italic;">by Felipe Correa</span>
</div>
</div>
</div>"""

clean_cabecalho = "\n".join([l.strip() for l in cabecalho_raw.splitlines() if l.strip()])
if hasattr(st, "html"):
    st.html(clean_cabecalho)
else:
    st.markdown(clean_cabecalho, unsafe_allow_html=True)

# 4. Controle de Telas e Base de Dados
if "tela_ativa" not in st.session_state:
    st.session_state["tela_ativa"] = "inicio"

if "orcamento_selecionado" not in st.session_state:
    st.session_state["orcamento_selecionado"] = None

if "historico_orcamentos" not in st.session_state:
    st.session_state["historico_orcamentos"] = [
        {"id": "2608251804903", "cliente": "Hemosan Mt", "data": "25/08/2026", "autor": "Eu", "status": "Em Analise", "projeto": "Guarda-Corpo / Sacada (NBR 14718)", "largura": 3.40, "altura": 1.10, "valor": 3787.85, "local": "Boa Viagem - Recife/PE", "whatsapp": "81991234567"},
        {"id": "2608241802746", "cliente": "Ivone", "data": "24/08/2026", "autor": "Eu", "status": "Em Analise", "projeto": "Box Frontal Padrão (1 Fixo + 1 Móvel)", "largura": 1.20, "altura": 1.90, "valor": 1250.00, "local": "Janga - Paulista/PE", "whatsapp": "81988776655"},
        {"id": "26081417888936", "cliente": "Marcos Emanuel Junior De Almeida", "data": "14/08/2026", "autor": "Eu", "status": "Aprovado", "projeto": "Janela 4 Folhas (2 Fixos + 2 Móveis)", "largura": 2.00, "altura": 1.20, "valor": 2180.00, "local": "Casa Forte - Recife/PE", "whatsapp": "81977665544"},
        {"id": "2608141788888", "cliente": "POSTURE SAUDE E CIENCIA", "data": "14/08/2026", "autor": "Eu", "status": "Em Analise", "projeto": "Porta Pivotante de Abrir (1 Folha)", "largura": 1.00, "altura": 2.10, "valor": 1940.00, "local": "Ilha do Leite - Recife/PE", "whatsapp": "81999881122"},
        {"id": "2608051771714", "cliente": "Clínica Práxis", "data": "05/08/2026", "autor": "Eu", "status": "Em Analise", "projeto": "Guarda-Corpo / Sacada (NBR 14718)", "largura": 4.10, "altura": 1.10, "valor": 4520.00, "local": "Espinheiro - Recife/PE", "whatsapp": "81998877665"},
        {"id": "2605151644433", "cliente": "CONDOMINIO EDIFICIO PORTAL DO BOSQUE", "data": "15/05/2026", "autor": "Eu", "status": "Em Analise", "projeto": "Guarda-Corpo / Sacada (NBR 14718)", "largura": 6.80, "altura": 1.10, "valor": 7890.00, "local": "Pina - Recife/PE", "whatsapp": "81987654321"},
    ]

if "clientes_cadastrados" not in st.session_state:
    st.session_state["clientes_cadastrados"] = [
        {"Nome": "Mariana Albuquerque", "WhatsApp": "(81) 99123-4567", "Local": "Boa Viagem - Recife/PE"},
        {"Nome": "Carlos Eduardo Silva", "WhatsApp": "(81) 98877-6655", "Local": "Janga - Paulista/PE"},
        {"Nome": "Juliana Tavares", "WhatsApp": "(81) 97766-5544", "Local": "Casa Forte - Recife/PE"},
    ]

# 5. Banco de dados técnico e cálculos (Mantidos 100% originais)
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
            {"peca": "Vidro Fixo", "largura": round((l / 2) + 0.02, 3), "altura": round(a - 0.05, 3), "qtd": 1},
            {"peca": "Vidro Móvel (Porta)", "largura": round((l / 2) + 0.05, 3), "altura": round(a - 0.05, 3), "qtd": 1},
        ],
    },
    "janela_4f": {
        "nome": "Janela 4 Folhas (2 Fixos + 2 Móveis)",
        "vidro_padrao": "Temperado 8mm Incolor",
        "kit_base": 280.0,
        "insumos_base": 60.0,
        "calc": lambda l, a: [
            {"peca": "Fixos Laterais", "largura": round((l / 4) + 0.02, 3), "altura": round(a - 0.04, 3), "qtd": 2},
            {"peca": "Móveis Centrais", "largura": round((l / 4) + 0.05, 3), "altura": round(a - 0.04, 3), "qtd": 2},
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

def processar_calculo(chave_proj, largura, altura, preco_m2, kit, insumos, mao_obra, margem):
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
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=1.5*cm, rightMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()
    
    AZUL_ESCURO = colors.HexColor("#9D201C")
    VERM = colors.HexColor("#D01B13")
    CINZA = colors.HexColor("#5A5A5A")
    FUNDO = colors.HexColor("#F8FAFC")
    BORDA = colors.HexColor("#CBD5E1")
    BRANCO = colors.white

    st_t = ParagraphStyle("T", fontName="Helvetica-Bold", fontSize=18, textColor=AZUL_ESCURO, alignment=1)
    st_sub = ParagraphStyle("Sub", fontName="Helvetica", fontSize=9, textColor=CINZA, alignment=1)
    st_c = ParagraphStyle("C", fontName="Helvetica", fontSize=8.5, textColor=CINZA)
    st_th = ParagraphStyle("TH", fontName="Helvetica-Bold", fontSize=8.5, textColor=BRANCO)
    st_td = ParagraphStyle("TD", fontName="Helvetica", fontSize=8.5, textColor=CINZA)
    st_tdr = ParagraphStyle("TDR", fontName="Helvetica-Bold", fontSize=8.5, textColor=AZUL_ESCURO, alignment=2)

    elems = [
        Paragraph("<b>HOPINESS PROJECT</b>", st_t),
        Paragraph("Vidraçaria Rio Branco | Soluções em Vidros e Esquadrias", st_sub),
        Spacer(1, 0.2*cm),
        Paragraph("<b>PROPOSTA COMERCIAL & ORÇAMENTO</b>", ParagraphStyle("P", fontName="Helvetica-Bold", fontSize=12, textColor=VERM, alignment=1)),
        HRFlowable(width="100%", thickness=1.5, color=VERM, spaceBefore=4, spaceAfter=8),
        Table([[
            Paragraph(f"<b>CLIENTE:</b> {dados['cli']}<br/><b>LOCAL:</b> {dados['loc']}", st_c),
            Paragraph(f"<b>PROJETO:</b> {dados['proj']}<br/><b>VÃO:</b> {dados['l']:.2f}m x {dados['a']:.2f}m", st_c),
        ]], colWidths=[9*cm, 9*cm], style=[
            ("BACKGROUND", (0,0), (-1,-1), FUNDO),
            ("BOX", (0,0), (-1,-1), 0.8, BORDA),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]),
        Spacer(1, 0.4*cm),
        Table([
            [Paragraph("Discriminação dos Serviços / Materiais", st_th), Paragraph("Subtotal", ParagraphStyle("R", parent=st_th, alignment=2))],
            [Paragraph(f"Vidros Lapidados ({dados['vidro']}) - Área: {dados['fat']:.2f} m²", st_td), Paragraph(f"R$ {dados['cv']:.2f}", st_tdr)],
            [Paragraph("Kits de Instalação e Ferragens Estruturais", st_td), Paragraph(f"R$ {dados['ck']:.2f}", st_tdr)],
            [Paragraph("Insumos de Vedação e Fixadores Químicos", st_td), Paragraph(f"R$ {dados['ci']:.2f}", st_tdr)],
            [Paragraph("Mão de Obra Especializada e Logística", st_td), Paragraph(f"R$ {dados['cmo']:.2f}", st_tdr)],
        ], colWidths=[13.5*cm, 4.5*cm], style=[
            ("BACKGROUND", (0,0), (-1,0), AZUL_ESCURO),
            ("GRID", (0,0), (-1,-1), 0.5, BORDA),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [BRANCO, FUNDO]),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]),
        Spacer(1, 0.4*cm),
        Table([[
            Paragraph("<b>Condições:</b> 50% de sinal e saldo na conclusão.<br/>Desconto de 5% no Pix.<br/>Garantia: 1 ano para instalação.", st_c),
            Paragraph(f"<font size='8' color='#5A5A5A'>VALOR TOTAL</font><br/><font size='16' color='#9D201C'><b>R$ {dados['total']:.2f}</b></font>", st_tdr)
        ]], colWidths=[11.5*cm, 6.5*cm], style=[
            ("BACKGROUND", (0,0), (-1,-1), FUNDO),
            ("BOX", (0,0), (-1,-1), 1, VERM),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ])
    ]
    doc.build(elems)
    val = buf.getvalue()
    buf.close()
    return val

# ==============================================================================
# RENDERIZAÇÃO DAS TELAS
# ==============================================================================

# TELA 0: INÍCIO (CARDS EM ESTILO ERP VIDRAÇARIA)
if st.session_state["tela_ativa"] == "inicio":
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    c_m1, c_m2, c_m3 = st.columns(3, gap="large")

    # CARD 1: ORÇAMENTOS
    with c_m1:
        st.markdown(
            """
            <div class="menu-card-container">
                <div class="menu-card-header">
                    <div class="menu-card-icon-badge">💬$</div>
                    <div class="menu-card-title">ORÇAMENTOS</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("➕ ADICIONAR", key="card_btn_add_orc", use_container_width=True):
                st.session_state["tela_ativa"] = "gerenciar_orcamentos"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_c2:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("📋 LISTAR", key="card_btn_list_orc", use_container_width=True):
                st.session_state["tela_ativa"] = "gerenciar_orcamentos"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # CARD 2: CLIENTES
    with c_m2:
        st.markdown(
            """
            <div class="menu-card-container">
                <div class="menu-card-header" style="background-color: #9D201C;">
                    <div class="menu-card-icon-badge" style="background-color: #D01B13;">👤</div>
                    <div class="menu-card-title">CLIENTES</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        b_cl1, b_cl2 = st.columns(2)
        with b_cl1:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("➕ ADICIONAR", key="card_btn_add_cli", use_container_width=True):
                st.session_state["tela_ativa"] = "novo_cliente"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_cl2:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("📋 LISTAR", key="card_btn_list_cli", use_container_width=True):
                st.session_state["tela_ativa"] = "listar_clientes"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # CARD 3: FINANCEIRO
    with c_m3:
        st.markdown(
            """
            <div class="menu-card-container">
                <div class="menu-card-header">
                    <div class="menu-card-icon-badge">📑$</div>
                    <div class="menu-card-title">FINANCEIRO</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        b_f1, b_f2, b_f3 = st.columns(3)
        with b_f1:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("➕ CAIXA", key="card_btn_add_fin", use_container_width=True):
                st.session_state["tela_ativa"] = "financeiro"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_f2:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("🏭 CORTE", key="card_btn_temp", use_container_width=True):
                st.session_state["tela_ativa"] = "tempera"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_f3:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("📋 LISTA", key="card_btn_list_fin", use_container_width=True):
                st.session_state["tela_ativa"] = "financeiro"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# TELA 1: GERENCIAR ORÇAMENTOS (EXATAMENTE COMO NO SEU ANEXO)
elif st.session_state["tela_ativa"] == "gerenciar_orcamentos":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR AO INÍCIO", key="btn_voltar_orc_grid"):
        st.session_state["tela_ativa"] = "inicio"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # BARRA SUPERIOR DE BUSCA E AÇÃO (ANEXO)
    top_col1, top_col2, top_col3 = st.columns([1.3, 3.2, 1.2])
    with top_col1:
        st.markdown('<div class="btn-gerar" style="margin-top: 4px;">', unsafe_allow_html=True)
        if st.button("➕ Criar Orçamento", key="btn_criar_novo_orc", use_container_width=True):
            st.session_state["orcamento_selecionado"] = None
            st.session_state["tela_ativa"] = "novo_orcamento"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with top_col2:
        termo_busca = st.text_input("Buscar", placeholder="🔍 Pesquise por nome, ID, telefone, CPF...", label_visibility="collapsed")

    with top_col3:
        st.date_input("Período", datetime.now(), label_visibility="collapsed")

    # FILTROS E STATUS (ANEXO)
    sub_col1, sub_col2 = st.columns([2.5, 1.0])
    with sub_col1:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 15px; flex-wrap: wrap; margin-bottom: 20px; margin-top: 5px;">
                <span style="font-weight: 800; color: #5A5A5A; font-size: 0.9rem;">Orçamentos:</span>
                <span class="status-badge status-badge-aprovado">🟢 Aprovado</span>
                <span class="status-badge status-badge-analise">🟡 Em Análise</span>
                <span class="status-badge status-badge-reprovado">🔴 Reprovado</span>
                <span class="status-badge status-badge-concluido">🔵 Concluído</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with sub_col2:
        st.markdown(
            """
            <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 5px;">
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #5A5A5A;">🗂 Cards</span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #94A3B8;">📋 Lista</span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #94A3B8;">📊 Kanban</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # FILTRAGEM DA LISTA
    lista_exibir = st.session_state["historico_orcamentos"]
    if termo_busca:
        lista_exibir = [
            o for o in lista_exibir
            if termo_busca.lower() in o["cliente"].lower() or termo_busca in str(o["id"]) or termo_busca in o.get("whatsapp", "")
        ]

    # GRADE DE 3 COLUNAS DE CARDS (IGUAL AO ANEXO)
    num_cols = 3
    for i in range(0, len(lista_exibir), num_cols):
        cols = st.columns(num_cols, gap="medium")
        for j in range(num_cols):
            if i + j < len(lista_exibir):
                item = lista_exibir[i + j]
                with cols[j]:
                    cor_barra = "#F59E0B" if item["status"] == "Em Analise" else "#10B981"
                    badge_class = "status-badge-analise" if item["status"] == "Em Analise" else "status-badge-aprovado"
                    status_label = "Em Análise ▾" if item["status"] == "Em Analise" else "Aprovado ▾"

                    st.markdown(
                        f"""
                        <div class="orc-card" style="border-top: 4px solid {cor_barra};">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span class="status-badge {badge_class}">{status_label}</span>
                                <span style="color: #94A3B8; font-size: 1.1rem; cursor: pointer;">★</span>
                            </div>
                            <div class="orc-card-title">{item['cliente']}</div>
                            <div class="orc-card-sub">Orçamento {item['id']} · {item['data']} · {item['autor']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # BOTÃO DETALHES QUE ABRE O FORMULÁRIO TÉCNICO DESTE ORÇAMENTO
                    if st.button(f"👁 Detalhes", key=f"det_{item['id']}", use_container_width=True):
                        st.session_state["orcamento_selecionado"] = item
                        st.session_state["tela_ativa"] = "novo_orcamento"
                        st.rerun()

                    # LINKS INFORMATIVOS E AÇÕES DA BASE (ANEXO)
                    st.markdown(
                        """
                        <div style="display: flex; justify-content: space-around; margin-top: 6px; margin-bottom: 10px; font-size: 0.76rem; color: #64748B; font-weight: 700;">
                            <span>📄 Relatórios</span>
                            <span>📝 Contrato</span>
                            <span>💬 Mais</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # BOTÕES DE RODAPÉ DO CARD
                    b_zap, b_map, b_cot = st.columns(3)
                    with b_zap:
                        link_wpp = f"https://api.whatsapp.com/send?phone=55{item['whatsapp']}&text=Ola%20{urllib.parse.quote(item['cliente'])}"
                        st.link_button("🟢 WhatsApp", link_wpp, use_container_width=True)
                    with b_map:
                        link_mapa = f"https://www.google.com/maps/search/{urllib.parse.quote(item['local'])}"
                        st.link_button("📍 Mapa", link_mapa, use_container_width=True)
                    with b_cot:
                        if st.button("💲 Cotação", key=f"cot_{item['id']}", use_container_width=True):
                            st.toast(f"Valor Total: R$ {item['valor']:.2f}")

# TELA 2: FORMULÁRIO DE ORÇAMENTO / CÁLCULO DE VÃO (AO CLICAR EM DETALHES OU NOVO ORÇAMENTO)
elif st.session_state["tela_ativa"] == "novo_orcamento":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR PARA ORÇAMENTOS", key="btn_voltar_orc"):
        st.session_state["tela_ativa"] = "gerenciar_orcamentos"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Carrega dados se for visualização de orçamento existente
    sel_dados = st.session_state.get("orcamento_selecionado") or {}
    val_nome = sel_dados.get("cliente", "Mariana Albuquerque")
    val_zap = sel_dados.get("whatsapp", "81991234567")
    val_loc = sel_dados.get("local", "Boa Viagem - Recife/PE")
    val_larg = sel_dados.get("largura", 3.40)
    val_alt = sel_dados.get("altura", 1.10)

    col_esq, col_dir = st.columns([1.1, 1.0], gap="large")

    with col_esq:
        st.markdown('<h4 style="color:#9D201C; margin-top:0; font-size:1.3rem; font-weight:800;">Configurações do Vão</h4>', unsafe_allow_html=True)

        sel_proj = st.selectbox(
            "Selecione o Projeto Padrão da Obra",
            options=list(PROJETOS_PADRAO.keys()),
            format_func=lambda x: PROJETOS_PADRAO[x]["nome"],
        )

        c_cli, c_zap, c_loc = st.columns(3)
        nome_c = c_cli.text_input("Nome do Cliente", val_nome)
        zap_c = c_zap.text_input("WhatsApp", val_zap)
        loc_c = c_loc.text_input("Local da Instalação", val_loc)

        c_l, c_a = st.columns(2)
        larg_v = c_l.number_input("Largura do Vão (m)", min_value=0.2, max_value=12.0, value=float(val_larg), step=0.05)
        alt_v = c_a.number_input("Altura do Vão (m)", min_value=0.2, max_value=6.0, value=float(val_alt), step=0.05)

        c_pm2, c_k, c_ins = st.columns(3)
        pm2 = c_pm2.number_input("Vidro R$/m²", value=380.0, step=10.0)
        kit_v = c_k.number_input("Kit/Ferragens (R$)", value=PROJETOS_PADRAO[sel_proj]["kit_base"], step=10.0)
        ins_v = c_ins.number_input("Insumos (R$)", value=PROJETOS_PADRAO[sel_proj]["insumos_base"], step=5.0)

        c_mo, c_mg = st.columns(2)
        mo_v = c_mo.number_input("Mão de Obra (R$)", value=450.0, step=10.0)
        mg_v = c_mg.slider("Margem de Lucro (%)", min_value=10.0, max_value=70.0, value=35.0)

    res = processar_calculo(sel_proj, larg_v, alt_v, pm2, kit_v, ins_v, mo_v, mg_v)

    with col_dir:
        m_c1, m_c2 = st.columns(2)
        with m_c1:
            st.markdown(
                f"""<div class="metric-card">
<div class="metric-card-label">Área Real (Líquida):</div>
<div class="metric-card-val">{res['area_liq']:.2f} m²</div>
</div>
<div class="metric-card">
<div class="metric-card-label">Custo Direto Total:</div>
<div class="metric-card-val">R$ {res['custo_total']:.2f}</div>
</div>""",
                unsafe_allow_html=True,
            )
        with m_c2:
            st.markdown(
                f"""<div class="metric-card">
<div class="metric-card-label">Área Faturada (+Folga):</div>
<div class="metric-card-val">{res['area_fat']:.2f} m²</div>
</div>
<div class="metric-card">
<div class="metric-card-label">Preço de Venda Sugerido:</div>
<div class="metric-card-val">R$ {res['preco_venda']:.2f}</div>
</div>""",
                unsafe_allow_html=True,
            )

        st.success(f"Lucro Bruto Estimado: **R$ {res['lucro']:.2f}** (Margem: {res['margem']}%)")

    st.markdown('<br/>', unsafe_allow_html=True)
    b_esp1, b_c1, b_c2, b_esp2 = st.columns([1, 1.3, 1.3, 1])

    dados_proposta = {
        "cli": nome_c, "loc": loc_c, "proj": res["nome"],
        "vidro": res["vidro"], "l": larg_v, "a": alt_v,
        "fat": res["area_fat"], "cv": res["custo_v"],
        "ck": kit_v, "ci": ins_v, "cmo": mo_v, "total": res["preco_venda"]
    }

    with b_c1:
        st.markdown('<div class="btn-gerar">', unsafe_allow_html=True)
        if st.button("💾 Salvar Orçamento", use_container_width=True):
            novo_id = f"26{datetime.now().strftime('%m%d%H%M%S')}"
            st.session_state["historico_orcamentos"].insert(0, {
                "id": novo_id,
                "cliente": nome_c,
                "data": datetime.now().strftime("%d/%m/%Y"),
                "autor": "Eu",
                "status": "Em Analise",
                "projeto": res["nome"],
                "largura": larg_v,
                "altura": alt_v,
                "valor": res["preco_venda"],
                "local": loc_c,
                "whatsapp": zap_c,
            })
            st.toast("Orçamento registrado com sucesso!")
            st.session_state["tela_ativa"] = "gerenciar_orcamentos"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

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
        st.markdown('</div>', unsafe_allow_html=True)

# TELA 3: CLIENTES (CADASTRO E LISTA)
elif st.session_state["tela_ativa"] == "novo_cliente":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR AO INÍCIO", key="btn_voltar_new_cli"):
        st.session_state["tela_ativa"] = "inicio"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h3 style='color:#9D201C;'>➕ Cadastro de Cliente</h3>", unsafe_allow_html=True)
    with st.form("cad_cliente_form"):
        nc = st.text_input("Nome do Cliente")
        tc = st.text_input("Telefone / WhatsApp")
        lc = st.text_input("Endereço / Bairro")
        if st.form_submit_button("Salvar Cadastro", type="primary"):
            if nc:
                st.session_state["clientes_cadastrados"].append({
                    "Nome": nc, "WhatsApp": tc, "Local": lc
                })
                st.success(f"Cliente {nc} cadastrado com sucesso!")
            else:
                st.warning("Preencha o nome do cliente.")

elif st.session_state["tela_ativa"] == "listar_clientes":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR AO INÍCIO", key="btn_voltar_lista_cli"):
        st.session_state["tela_ativa"] = "inicio"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h3 style='color:#9D201C;'>👥 Clientes Cadastrados</h3>", unsafe_allow_html=True)
    st.table(st.session_state["clientes_cadastrados"])

# TELA 4: FINANCEIRO
elif st.session_state["tela_ativa"] == "financeiro":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR AO INÍCIO", key="btn_voltar_fin_tela"):
        st.session_state["tela_ativa"] = "inicio"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h3 style='color:#9D201C;'>Gestão Financeira da Obra</h3>", unsafe_allow_html=True)
    cf1, cf2, cf3 = st.columns(3)
    cf1.metric("Valor Total Previsto", "R$ 3.787,85")
    cf2.metric("Custo de Materiais e Instalação", "R$ 2.462,10")
    cf3.metric("Lucro Líquido Estimado", "R$ 1.325,75")

# TELA 5: TÊMPERA
elif st.session_state["tela_ativa"] == "tempera":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR AO INÍCIO", key="btn_voltar_temp_tela"):
        st.session_state["tela_ativa"] = "inicio"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h3 style='color:#9D201C;'>Ordem de Corte para a Têmpera</h3>", unsafe_allow_html=True)
    st.info("Medidas técnicas calculadas com descontos de folga e transpasse.")
    res_temp = processar_calculo("guarda_corpo_torres", 3.40, 1.10, 380.0, 450.0, 120.0, 450.0, 35.0)
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

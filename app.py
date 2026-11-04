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

# 1. Carregamento da Logomarca (vdr.jpeg)
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

# 2. Definição de CSS Seguro sem Quebras de String
css_rules = [
    "<style>",
    "html, body, [data-testid='stAppViewContainer'], .stApp, section.main {",
    "background: linear-gradient(160deg, #FADBD8 0%, #FFFFFF 35%, #FDE8E7 70%, #FFFFFF 100%) !important;",
    "background-attachment: fixed !important;",
    "}",
    "p, span, label, .stMarkdown {",
    "color: #5A5A5A !important;",
    "font-weight: 600;",
    "}",
    "div[data-testid='stHorizontalBlock'] .tab-nav-btn button {",
    "background-color: #D01B13 !important;",
    "border-radius: 25px !important;",
    "padding: 10px 14px !important;",
    "border: none !important;",
    "width: 100% !important;",
    "box-shadow: 0 3px 6px rgba(208, 27, 19, 0.25) !important;",
    "}",
    "div[data-testid='stHorizontalBlock'] .tab-nav-btn button[kind='primary'] {",
    "background-color: #9D201C !important;",
    "box-shadow: 0 4px 12px rgba(157, 32, 28, 0.5) !important;",
    "}",
    "div[data-testid='stHorizontalBlock'] .tab-nav-btn button *,",
    "div[data-testid='stHorizontalBlock'] .tab-nav-btn button p,",
    "div[data-testid='stHorizontalBlock'] .tab-nav-btn button span {",
    "color: #FFFFFF !important;",
    "fill: #FFFFFF !important;",
    "-webkit-text-fill-color: #FFFFFF !important;",
    "font-weight: 800 !important;",
    "font-size: 0.93rem !important;",
    "}",
    "div[data-testid='stHorizontalBlock'] .tab-nav-btn button:hover {",
    "background-color: #B50915 !important;",
    "}",
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

# 3. Cabeçalho Estruturado com Esquadrias em Perspetiva e Título em Vermelho
cabecalho_lines = [
    '<div style="position:relative;background:rgba(255,255,255,0.45);backdrop-filter:blur(6px);border:1px solid rgba(226,232,240,0.9);border-left:8px solid #D01B13;border-radius:12px;padding:14px 24px;margin-top:-15px;margin-bottom:22px;box-shadow:0 4px 15px rgba(208,27,19,0.08);overflow:hidden;min-height:98px;">',
    '<svg style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" viewBox="0 0 1000 100">',
    '<defs>',
    '<radialGradient id="blurGlow" cx="50%" cy="50%" r="40%">',
    '<stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>',
    '<stop offset="60%" stop-color="#FDE8E7" stop-opacity="0.8"/>',
    '<stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>',
    '</radialGradient>',
    '</defs>',
    '<ellipse cx="500" cy="50" rx="280" ry="48" fill="url(#blurGlow)"/>',
    '<g stroke="#64748B" stroke-width="1.3" opacity="0.75">',
    '<line x1="0" y1="10" x2="360" y2="40"/>',
    '<line x1="0" y1="30" x2="360" y2="46"/>',
    '<line x1="0" y1="50" x2="360" y2="50"/>',
    '<line x1="0" y1="70" x2="360" y2="54"/>',
    '<line x1="0" y1="90" x2="360" y2="60"/>',
    '<line x1="30" y1="0" x2="30" y2="100" stroke-width="2.2" stroke="#475569"/>',
    '<line x1="85" y1="0" x2="85" y2="100" stroke-width="1.8"/>',
    '<line x1="145" y1="0" x2="145" y2="100" stroke-width="1.5"/>',
    '<line x1="210" y1="0" x2="210" y2="100" stroke-width="1.3"/>',
    '<line x1="280" y1="0" x2="280" y2="100" stroke-width="1.1"/>',
    '<line x1="350" y1="0" x2="350" y2="100" stroke-width="0.9"/>',
    '<line x1="1000" y1="10" x2="640" y2="40"/>',
    '<line x1="1000" y1="30" x2="640" y2="46"/>',
    '<line x1="1000" y1="50" x2="640" y2="50"/>',
    '<line x1="1000" y1="70" x2="640" y2="54"/>',
    '<line x1="1000" y1="90" x2="640" y2="60"/>',
    '<line x1="970" y1="0" x2="970" y2="100" stroke-width="2.2" stroke="#475569"/>',
    '<line x1="915" y1="0" x2="915" y2="100" stroke-width="1.8"/>',
    '<line x1="855" y1="0" x2="855" y2="100" stroke-width="1.5"/>',
    '<line x1="790" y1="0" x2="790" y2="100" stroke-width="1.3"/>',
    '<line x1="720" y1="0" x2="720" y2="100" stroke-width="1.1"/>',
    '<line x1="650" y1="0" x2="650" y2="100" stroke-width="0.9"/>',
    '</g>',
    '</svg>',
    '<div style="position:relative;z-index:2;display:flex;align-items:center;justify-content:space-between;width:100%;">',
    f'<div style="flex-shrink:0;">{logo_html}</div>',
    '<div style="text-align:center;flex-grow:1;">',
    '<span style="color:#9D201C !important;-webkit-text-fill-color:#9D201C !important;font-size:2.35rem;font-weight:900;letter-spacing:2.5px;text-transform:uppercase;font-family:\'Segoe UI\',sans-serif;display:inline-block;">HOPINESS PROJECT</span>',
    '</div>',
    '<div style="flex-shrink:0;">',
    '<span style="color:#5A5A5A;font-size:0.95rem;font-weight:600;font-style:italic;">by Felipe Correa</span>',
    '</div>',
    '</div>',
    '</div>',
]

st.markdown("\n".join(cabecalho_lines), unsafe_allow_html=True)

# 4. Navegação entre Abas
if "aba_ativa" not in st.session_state:
    st.session_state["aba_ativa"] = "projetos"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="tab-nav-btn">', unsafe_allow_html=True)
    if st.button("📐 Projetos Padrão & Orçamento", type="primary" if st.session_state["aba_ativa"] == "projetos" else "secondary", use_container_width=True):
        st.session_state["aba_ativa"] = "projetos"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="tab-nav-btn">', unsafe_allow_html=True)
    if st.button("🏭 Pedido de Têmpera (Corte)", type="primary" if st.session_state["aba_ativa"] == "tempera" else "secondary", use_container_width=True):
        st.session_state["aba_ativa"] = "tempera"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="tab-nav-btn">', unsafe_allow_html=True)
    if st.button("💵 Financeiro da Obra", type="primary" if st.session_state["aba_ativa"] == "financeiro" else "secondary", use_container_width=True):
        st.session_state["aba_ativa"] = "financeiro"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="tab-nav-btn">', unsafe_allow_html=True)
    if st.button("📋 Catálogo Técnico ABNT", type="primary" if st.session_state["aba_ativa"] == "abnt" else "secondary", use_container_width=True):
        st.session_state["aba_ativa"] = "abnt"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# 5. Banco de Dados Técnico
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

# 6. Conteúdo da Aba Ativa
if st.session_state["aba_ativa"] == "projetos":
    col_esq, col_dir = st.columns([1.1, 1.0], gap="large")

    with col_esq:
        st.markdown('<h4 style="color:#9D201C; margin-top:0; font-size:1.3rem; font-weight:800;">Configurações do Vão</h4>', unsafe_allow_html=True)

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
        larg_v = c_l.number_input("Largura do Vão (m)", min_value=0.2, max_value=12.0, value=3.40, step=0.05)
        alt_v = c_a.number_input("Altura do Vão (m)", min_value=0.2, max_value=6.0, value=1.10, step=0.05)

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
                f'''<div class="metric-card">
<div class="metric-card-label">Área Real (Líquida):</div>
<div class="metric-card-val">{res['area_liq']:.2f} m²</div>
</div>
<div class="metric-card">
<div class="metric-card-label">Custo Direto Total:</div>
<div class="metric-card-val">R$ {res['custo_total']:.2f}</div>
</div>''',
                unsafe_allow_html=True,
            )
        with m_c2:
            st.markdown(
                f'''<div class="metric-card">
<div class="metric-card-label">Área Faturada (+Folga):</div>
<div class="metric-card-val">{res['area_fat']:.2f} m²</div>
</div>
<div class="metric-card">
<div class="metric-card-label">Preço de Venda Sugerido:</div>
<div class="metric-card-val">R$ {res['preco_venda']:.2f}</div>
</div>''',
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
        if st.button("📄 Gerar Orçamento", use_container_width=True):
            st.toast("Orçamento recalculado com sucesso!")
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

elif st.session_state["aba_ativa"] == "tempera":
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

elif st.session_state["aba_ativa"] == "financeiro":
    st.markdown("<h3 style='color:#9D201C;'>Gestão Financeira da Obra</h3>", unsafe_allow_html=True)
    cf1, cf2, cf3 = st.columns(3)
    cf1.metric("Valor Total Previsto", "R$ 3.787,85")
    cf2.metric("Custo de Materiais e Instalação", "R$ 2.462,10")
    cf3.metric("Lucro Líquido Estimado", "R$ 1.325,75")

elif st.session_state["aba_ativa"] == "abnt":
    st.markdown("<h3 style='color:#9D201C;'>Normas Técnicas da Construção Civil</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        - **ABNT NBR 14207 (Boxes de Banheiro):** Exige vidro de segurança (temperado 8mm ou laminado).
        - **ABNT NBR 14718 (Guarda-Corpos e Sacadas):** Obrigatório vidro laminado ou laminado-temperado. Proibido vidro temperado comum sem laminação.
        - **ABNT NBR 7199 (Vidros na Construção Civil):** Vidros abaixo de 1,10m do piso acabado devem ser vidros de segurança.
        """
    )

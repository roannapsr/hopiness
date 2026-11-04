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

# 2. CSS Global
css_code = """<style>
html, body, [data-testid="stAppViewContainer"], .stApp, section.main {
background: linear-gradient(160deg, #FADBD8 0%, #FFFFFF 35%, #FDE8E7 70%, #FFFFFF 100%) !important;
background-attachment: fixed !important;
}

p, span, label, .stMarkdown {
color: #5A5A5A !important;
font-weight: 600;
}

.menu-card-container {
background-color: #FFFFFF;
border-radius: 12px;
border: 1px solid #CBD5E1;
box-shadow: 0 4px 15px rgba(0,0,0,0.06);
margin-bottom: 20px;
overflow: visible;
position: relative;
margin-top: 25px;
}
.menu-card-header {
background-color: #D01B13;
color: #FFFFFF !important;
padding: 16px 20px;
border-top-left-radius: 11px;
border-top-right-radius: 11px;
display: flex;
align-items: center;
justify-content: center;
position: relative;
min-height: 54px;
}
.menu-card-icon-badge {
position: absolute;
top: -24px;
left: 20px;
width: 48px;
height: 48px;
border-radius: 50%;
background-color: #9D201C;
color: #FFFFFF;
display: flex;
align-items: center;
justify-content: center;
font-size: 1.3rem;
box-shadow: 0 4px 8px rgba(0,0,0,0.18);
border: 3px solid #FFFFFF;
}
.menu-card-title {
color: #FFFFFF !important;
font-size: 1.05rem;
font-weight: 800;
margin: 0;
text-align: center;
letter-spacing: 0.3px;
}
.card-action-btn button {
border-radius: 20px !important;
padding: 6px 14px !important;
font-weight: 800 !important;
border: 2px solid #D01B13 !important;
background-color: #FFFFFF !important;
color: #D01B13 !important;
box-shadow: 0 2px 5px rgba(208, 27, 19, 0.1) !important;
width: 100% !important;
}
.card-action-btn button * {
color: #D01B13 !important;
font-weight: 800 !important;
font-size: 0.9rem !important;
}
.card-action-btn button:hover {
background-color: #D01B13 !important;
color: #FFFFFF !important;
}
.card-action-btn button:hover * {
color: #FFFFFF !important;
}
.btn-voltar button {
background-color: #5A5A5A !important;
color: #FFFFFF !important;
border-radius: 20px !important;
font-weight: 800 !important;
border: none !important;
padding: 8px 22px !important;
margin-bottom: 15px !important;
}
.btn-voltar button * {
color: #FFFFFF !important;
font-weight: 800 !important;
}

.metric-card {
background-color: #FFFFFF;
border: 1px solid #E2E8F0;
border-radius: 12px;
padding: 18px 15px;
text-align: center;
box-shadow: 0 3px 10px rgba(0,0,0,0.04);
margin-bottom: 15px;
}
.metric-card-label {
color: #5A5A5A;
font-size: 0.92rem;
font-weight: 700;
margin-bottom: 6px;
}
.metric-card-val {
color: #9D201C;
font-size: 1.85rem;
font-weight: 900;
margin: 0;
}

.orc-card {
background-color: #FFFFFF;
border-radius: 10px;
border: 1px solid #E2E8F0;
box-shadow: 0 3px 12px rgba(0,0,0,0.05);
padding: 16px 16px 12px 16px;
margin-bottom: 20px;
position: relative;
}
.status-badge {
display: inline-flex;
align-items: center;
gap: 5px;
padding: 4px 10px;
border-radius: 14px;
font-size: 0.78rem;
font-weight: 700;
}
.status-badge-analise { background-color: #FEF3C7; color: #B45309; }
.status-badge-aprovado { background-color: #D1FAE5; color: #047857; }
.status-badge-reprovado { background-color: #FEE2E2; color: #B91C1C; }
.status-badge-concluido { background-color: #E0E7FF; color: #3730A3; }
.orc-card-title {
color: #1E293B !important;
font-size: 1.05rem;
font-weight: 800;
margin-top: 10px;
margin-bottom: 3px;
}
.orc-card-sub {
color: #64748B;
font-size: 0.78rem;
font-weight: 600;
margin-bottom: 12px;
}

.cli-card {
background-color: #FFFFFF;
border-radius: 10px;
border: 1px solid #E2E8F0;
border-top: 4px solid #D01B13;
box-shadow: 0 3px 12px rgba(0,0,0,0.05);
padding: 16px;
margin-bottom: 20px;
position: relative;
min-height: 190px;
display: flex;
flex-direction: column;
justify-content: space-between;
}
.cli-avatar {
width: 38px;
height: 38px;
border-radius: 50%;
background-color: #9D201C;
color: #FFFFFF;
display: flex;
align-items: center;
justify-content: center;
font-weight: 800;
font-size: 1.1rem;
flex-shrink: 0;
}
.cli-nome {
color: #1E293B !important;
font-size: 0.98rem;
font-weight: 800;
text-transform: uppercase;
line-height: 1.2;
}
.cli-resp {
color: #64748B;
font-size: 0.78rem;
font-weight: 600;
margin-top: 2px;
}
.cli-info-line {
display: flex;
align-items: center;
gap: 7px;
color: #475569;
font-size: 0.82rem;
font-weight: 600;
margin-top: 4px;
}

.fin-top-card {
background-color: #FFFFFF;
border: 1px solid #E2E8F0;
border-radius: 10px;
padding: 14px 18px;
box-shadow: 0 2px 8px rgba(0,0,0,0.03);
margin-bottom: 15px;
}
.fin-top-title {
color: #64748B;
font-size: 0.82rem;
font-weight: 700;
margin-bottom: 4px;
}
.fin-top-val {
color: #1E293B;
font-size: 1.25rem;
font-weight: 800;
margin-bottom: 8px;
}
.fin-tag-realizado {
background-color: #E0E7FF;
color: #3730A3;
padding: 2px 8px;
border-radius: 10px;
font-size: 0.72rem;
font-weight: 700;
display: inline-block;
}

/* CARD CLIENTES DO DIA */
.dia-card {
background-color: #FFFFFF;
border-left: 5px solid #D01B13;
border-radius: 8px;
padding: 12px 16px;
box-shadow: 0 2px 6px rgba(0,0,0,0.04);
margin-bottom: 10px;
display: flex;
justify-content: space-between;
align-items: center;
}

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

.btn-gerar button {
background-color: #D01B13 !important;
color: #FFFFFF !important;
border-radius: 25px !important;
font-weight: 800 !important;
padding: 12px 28px !important;
border: none !important;
box-shadow: 0 4px 10px rgba(208,27,19,0.3) !important;
width: 100% !important;
}
.btn-gerar button * {
color: #FFFFFF !important;
font-weight: 800 !important;
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
.btn-pdf button * {
color: #FFFFFF !important;
font-weight: 800 !important;
}
</style>"""

clean_css = "\n".join([l.strip() for l in css_code.splitlines() if l.strip()])
if hasattr(st, "html"):
    st.html(clean_css)
else:
    st.markdown(clean_css, unsafe_allow_html=True)

# 3. Cabeçalho com título em vermelho escuro #9D201C
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

# 4. Controle de Telas e Memória (com Agenda e Clientes do Dia)
if "tela_ativa" not in st.session_state:
    st.session_state["tela_ativa"] = "inicio"

if "orcamento_selecionado" not in st.session_state:
    st.session_state["orcamento_selecionado"] = None

if "historico_orcamentos" not in st.session_state:
    st.session_state["historico_orcamentos"] = [
        {"id": "2608251804903", "cliente": "HEMOSAN MT", "data": "25/08/2026", "autor": "Eu", "status": "Em Analise", "projeto": "Guarda-Corpo / Sacada (NBR 14718)", "largura": 3.40, "altura": 1.10, "valor": 3787.85, "local": "Boa Viagem - Recife/PE", "whatsapp": "81991234567"},
        {"id": "2608241802746", "cliente": "IVONE", "data": "24/08/2026", "autor": "Eu", "status": "Em Analise", "projeto": "Box Frontal Padrão (1 Fixo + 1 Móvel)", "largura": 1.20, "altura": 1.90, "valor": 1250.00, "local": "Janga - Paulista/PE", "whatsapp": "81988776655"},
        {"id": "26081417888936", "cliente": "MARCOS EMANUEL JUNIOR DE ALMEIDA NUNES LEITE", "data": "14/08/2026", "autor": "Eu", "status": "Aprovado", "projeto": "Janela 4 Folhas (2 Fixos + 2 Móveis)", "largura": 2.00, "altura": 1.20, "valor": 2180.00, "local": "Casa Forte - Recife/PE", "whatsapp": "81977665544"},
    ]

if "clientes_cadastrados" not in st.session_state:
    st.session_state["clientes_cadastrados"] = [
        {"nome": "MARIANA ALBUQUERQUE", "responsavel": "Eu", "telefone": "81991234567", "email": "mariana@email.com", "cadastro": "03/11/2026", "local": "Boa Viagem - Recife/PE"},
        {"nome": "HEMOSAN MT", "responsavel": "Eu", "telefone": "", "email": "", "cadastro": "25/08/2026", "local": "Boa Viagem - Recife/PE"},
        {"nome": "IVONE", "responsavel": "Eu", "telefone": "", "email": "", "cadastro": "24/08/2026", "local": "Janga - Paulista/PE"},
        {"nome": "MARCOS EMANUEL JUNIOR DE ALMEIDA NUNES LEITE", "responsavel": "Eu", "telefone": "", "email": "", "cadastro": "14/08/2026", "local": "Recife/PE"},
    ]

if "agenda_compromissos" not in st.session_state:
    st.session_state["agenda_compromissos"] = [
        {"cliente": "MARIANA ALBUQUERQUE", "horario": "09:00", "servico": "Instalação de Guarda-Corpo", "data": datetime.now().strftime("%d/%m/%Y")},
        {"cliente": "IVONE", "horario": "14:30", "servico": "Medição de Box Frontal", "data": datetime.now().strftime("%d/%m/%Y")},
        {"cliente": "HEMOSAN MT", "horario": "16:00", "servico": "Orçamento Técnico", "data": datetime.now().strftime("%d/%m/%Y")},
    ]

# Sincronização automática
nomes_cad = {str(c.get("nome", "")).upper() for c in st.session_state["clientes_cadastrados"]}
for orc in st.session_state["historico_orcamentos"]:
    nm = str(orc.get("cliente", "")).strip().upper()
    if nm and nm not in nomes_cad:
        st.session_state["clientes_cadastrados"].append({
            "nome": nm,
            "responsavel": orc.get("autor", "Eu"),
            "telefone": orc.get("whatsapp", ""),
            "email": "",
            "cadastro": orc.get("data", datetime.now().strftime("%d/%m/%Y")),
            "local": orc.get("local", "Recife/PE")
        })
        nomes_cad.add(nm)

# 5. Banco de dados técnico e cálculos
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
# RENDERIZAÇÃO DAS TELAS (4 CARDS NA PÁGINA INICIAL + CLIENTES DO DIA)
# ==============================================================================

if st.session_state["tela_ativa"] == "inicio":
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    c_m1, c_m2, c_m3, c_m4 = st.columns(4, gap="medium")

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
            if st.button("➕", key="btn_add_orc_mini", use_container_width=True):
                st.session_state["tela_ativa"] = "gerenciar_orcamentos"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_c2:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("📋", key="btn_list_orc_mini", use_container_width=True):
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
            if st.button("➕", key="btn_add_cli_mini", use_container_width=True):
                st.session_state["tela_ativa"] = "gerenciar_clientes"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_cl2:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("📋", key="btn_list_cli_mini", use_container_width=True):
                st.session_state["tela_ativa"] = "gerenciar_clientes"
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
            if st.button("💲", key="btn_fin_mini", use_container_width=True):
                st.session_state["tela_ativa"] = "financeiro"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_f2:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("🏭", key="btn_temp_mini", use_container_width=True):
                st.session_state["tela_ativa"] = "tempera"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_f3:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("📊", key="btn_fin_list_mini", use_container_width=True):
                st.session_state["tela_ativa"] = "financeiro"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # CARD 4: AGENDA
    with c_m4:
        st.markdown(
            """
            <div class="menu-card-container">
                <div class="menu-card-header" style="background-color: #9D201C;">
                    <div class="menu-card-icon-badge" style="background-color: #D01B13;">📅</div>
                    <div class="menu-card-title">AGENDA</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        b_ag1, b_ag2 = st.columns(2)
        with b_ag1:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("➕", key="btn_add_agenda_mini", use_container_width=True):
                st.session_state["tela_ativa"] = "agenda"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_ag2:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("📅", key="btn_ver_agenda_mini", use_container_width=True):
                st.session_state["tela_ativa"] = "agenda"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # SEÇÃO: CLIENTES DO DIA NA PÁGINA INICIAL
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#9D201C; font-weight:800; margin-bottom: 15px;'>📌 CLIENTES DO DIA (Agendamentos)</h4>", unsafe_allow_html=True)

    compromissos_hoje = [c for c in st.session_state["agenda_compromissos"] if c.get("data") == datetime.now().strftime("%d/%m/%Y")]
    if not compromissos_hoje:
        compromissos_hoje = st.session_state["agenda_compromissos"] # exibe todos se for demonstração

    for comp in compromissos_hoje:
        st.markdown(
            f"""
            <div class="dia-card">
                <div>
                    <span style="font-weight: 800; color: #1E293B; font-size: 1rem; text-transform: uppercase;">{comp.get('cliente')}</span>
                    <div style="color: #64748B; font-size: 0.82rem; font-weight: 600; margin-top: 2px;">Serviço: {comp.get('servico')}</div>
                </div>
                <div style="background: #FEE2E2; color: #9D201C; padding: 6px 14px; border-radius: 20px; font-weight: 800; font-size: 0.88rem;">
                    ⏰ {comp.get('horario')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# TELA DE AGENDA (CALENDÁRIO COMPLETO CONFORME ANEXO)
elif st.session_state["tela_ativa"] == "agenda":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR AO INÍCIO", key="btn_voltar_agenda"):
        st.session_state["tela_ativa"] = "inicio"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # BARRA SUPERIOR DA AGENDA (EXATAMENTE COMO NO ANEXO)
    ag_top1, ag_top2, ag_top3 = st.columns([1.5, 3.0, 2.0])
    with ag_top1:
        st.markdown('<div class="btn-gerar" style="margin-top: 4px;">', unsafe_allow_html=True)
        if st.button("➕ Novo Agendamento", key="btn_novo_agendamento", use_container_width=True):
            st.session_state["modal_novo_agendamento"] = True
        st.markdown('</div>', unsafe_allow_html=True)

    with ag_top2:
        st.markdown(
            """
            <div style="display: flex; gap: 8px; align-items: center; margin-top: 6px;">
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #5A5A5A;">Hoje</span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #5A5A5A;">7 dias</span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #5A5A5A;">15 dias</span>
                <span style="background: #D01B13; color: #FFFFFF; padding: 4px 12px; border-radius: 6px; font-size: 0.82rem; font-weight: 700;">Novembro de 2026 ▾</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with ag_top3:
        st.markdown(
            """
            <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 6px;">
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #94A3B8;">Status: Todos ▾</span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #94A3B8;">Prioridade: Todas ▾</span>
                <span style="background: #D01B13; color: #FFFFFF; padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 700;">Calendário</span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #5A5A5A;">Lista</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    # CADASTRO RÁPIDO DE NOVO AGENDAMENTO
    if st.session_state.get("modal_novo_agendamento", False):
        with st.form("form_novo_agendamento"):
            st.markdown("<h4 style='color:#9D201C;'>Novo Agendamento na Agenda</h4>", unsafe_allow_html=True)
            cli_agenda = st.selectbox("Cliente", options=[c["nome"] for c in st.session_state["clientes_cadastrados"]])
            hora_agenda = st.text_input("Horário (Ex: 10:30)", "10:30")
            serv_agenda = st.text_input("Serviço / Obra", "Instalação de Box")
            data_agenda = st.text_input("Data (DD/MM/AAAA)", datetime.now().strftime("%d/%m/%Y"))
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                if st.form_submit_button("Salvar Agendamento", type="primary"):
                    st.session_state["agenda_compromissos"].append({
                        "cliente": cli_agenda,
                        "horario": hora_agenda,
                        "servico": serv_agenda,
                        "data": data_agenda
                    })
                    st.success("Agendamento salvo com sucesso!")
                    st.session_state["modal_novo_agendamento"] = False
                    st.rerun()
            with col_s2:
                if st.form_submit_button("Cancelar"):
                    st.session_state["modal_novo_agendamento"] = False
                    st.rerun()

    # GRADE DO CALENDÁRIO MENSAL (EXATAMENTE COMO NO ANEXO)
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    cols_dias = st.columns(7)
    for idx, d_nome in enumerate(dias_semana):
        with cols_dias[idx]:
            st.markdown(f"<div style='text-align: center; font-weight: 800; color: #9D201C; padding: 8px; background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 6px; margin-bottom: 5px;'>{d_nome}</div>", unsafe_allow_html=True)

    matriz_dias = [
        [26, 27, 28, 29, 30, 31, 1],
        [2, 3, 4, 5, 6, 7, 8],
        [9, 10, 11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20, 21, 22],
        [23, 24, 25, 26, 27, 28, 29],
        [30, 1, 2, 3, 4, 5, 6]
    ]

    for semana in matriz_dias:
        cols_sem = st.columns(7)
        for idx, dia_num in enumerate(semana):
            with cols_sem[idx]:
                destaque_hoje = "background-color: #FEE2E2; border: 2px solid #D01B13;" if dia_num == 4 else "background-color: #FFFFFF;"
                
                conteudo_dia = f"<div style='font-weight: 800; font-size: 0.85rem; color: #1E293B;'>{dia_num}</div>"
                if dia_num in [4, 24, 25]:
                    conteudo_dia += "<div style='background: #D01B13; color: #FFFFFF; font-size: 0.7rem; padding: 2px 4px; border-radius: 4px; margin-top: 4px; font-weight: 700;'>📌 Compromisso</div>"

                st.markdown(
                    f"""
                    <div style="{destaque_hoje} border: 1px solid #E2E8F0; border-radius: 6px; padding: 8px; min-height: 75px; margin-bottom: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
                        {conteudo_dia}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# TELA 1: GERENCIAR ORÇAMENTOS
elif st.session_state["tela_ativa"] == "gerenciar_orcamentos":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR AO INÍCIO", key="btn_voltar_orc_grid"):
        st.session_state["tela_ativa"] = "inicio"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    top_col1, top_col2, top_col3 = st.columns([1.3, 3.2, 1.2])
    with top_col1:
        st.markdown('<div class="btn-gerar" style="margin-top: 4px;">', unsafe_allow_html=True)
        if st.button("➕ Criar Orçamento", key="btn_criar_novo_orc", use_container_width=True):
            st.session_state["orcamento_selecionado"] = None
            st.session_state["tela_ativa"] = "novo_orcamento"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with top_col2:
        termo_busca = st.text_input("Buscar Orçamento", placeholder="🔍 Pesquise por nome, ID, telefone, CPF...", label_visibility="collapsed")

    with top_col3:
        st.date_input("Período Orçamento", datetime.now(), label_visibility="collapsed")

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

    lista_exibir = st.session_state["historico_orcamentos"]
    if termo_busca:
        lista_exibir = [
            o for o in lista_exibir
            if termo_busca.lower() in o.get("cliente", "").lower() or termo_busca in str(o.get("id", "")) or termo_busca in o.get("whatsapp", "")
        ]

    num_cols = 3
    for i in range(0, len(lista_exibir), num_cols):
        cols = st.columns(num_cols, gap="medium")
        for j in range(num_cols):
            if i + j < len(lista_exibir):
                item = lista_exibir[i + j]
                with cols[j]:
                    st_val = item.get("status", "Em Analise")
                    cor_barra = "#F59E0B" if st_val == "Em Analise" else "#10B981"
                    badge_class = "status-badge-analise" if st_val == "Em Analise" else "status-badge-aprovado"
                    status_label = "Em Análise ▾" if st_val == "Em Analise" else "Aprovado ▾"

                    st.markdown(
                        f"""
                        <div class="orc-card" style="border-top: 4px solid {cor_barra};">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span class="status-badge {badge_class}">{status_label}</span>
                                <span style="color: #94A3B8; font-size: 1.1rem; cursor: pointer;">★</span>
                            </div>
                            <div class="orc-card-title">{item.get('cliente', 'Cliente')}</div>
                            <div class="orc-card-sub">Orçamento {item.get('id', '---')} · {item.get('data', '')} · {item.get('autor', 'Eu')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if st.button(f"👁 Detalhes", key=f"det_{item.get('id', i+j)}", use_container_width=True):
                        st.session_state["orcamento_selecionado"] = item
                        st.session_state["tela_ativa"] = "novo_orcamento"
                        st.rerun()

                    b_zap, b_map, b_cot = st.columns(3)
                    with b_zap:
                        link_wpp = f"https://api.whatsapp.com/send?phone=55{item.get('whatsapp', '')}&text=Ola%20{urllib.parse.quote(item.get('cliente', ''))}"
                        st.link_button("🟢 WhatsApp", link_wpp, use_container_width=True)
                    with b_map:
                        link_mapa = f"https://www.google.com/maps/search/{urllib.parse.quote(item.get('local', 'Recife PE'))}"
                        st.link_button("📍 Mapa", link_mapa, use_container_width=True)
                    with b_cot:
                        if st.button("💲 Cotação", key=f"cot_{item.get('id', i+j)}", use_container_width=True):
                            val_c = item.get("valor", 0.0)
                            if isinstance(val_c, (int, float)):
                                st.toast(f"Valor Total: R$ {val_c:.2f}")
                            else:
                                st.toast(f"Valor: {val_c}")

# TELA 2: FORMULÁRIO DE ORÇAMENTO
elif st.session_state["tela_ativa"] == "novo_orcamento":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR PARA ORÇAMENTOS", key="btn_voltar_orc"):
        st.session_state["tela_ativa"] = "gerenciar_orcamentos"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

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
                "cliente": nome_c.upper(),
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

# TELA 3: GERENCIAR CLIENTES
elif st.session_state["tela_ativa"] == "gerenciar_clientes":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR AO INÍCIO", key="btn_voltar_cli_grid"):
        st.session_state["tela_ativa"] = "inicio"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    top_c1, top_c2, top_c3 = st.columns([1.5, 3.2, 1.2])
    with top_c1:
        st.markdown('<div class="btn-gerar" style="margin-top: 4px;">', unsafe_allow_html=True)
        if st.button("➕ Adicionar Cliente", key="btn_add_cliente_top", use_container_width=True):
            st.session_state["tela_ativa"] = "novo_cliente"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with top_c2:
        busca_cli = st.text_input("Buscar Cliente", placeholder="🔍 Pesquise por nome, telefone, CPF...", label_visibility="collapsed")

    with top_c3:
        st.selectbox("Filtro", ["Tudo", "Com Telefone", "Sem Telefone"], label_visibility="collapsed")

    total_clientes = len(st.session_state["clientes_cadastrados"])
    sub_c1, sub_c2 = st.columns([2.0, 1.0])
    with sub_c1:
        st.markdown(f"<span style='font-weight: 800; color: #475569; font-size: 0.95rem;'>Clientes: {total_clientes}</span>", unsafe_allow_html=True)
    with sub_c2:
        st.markdown(
            """
            <div style="display: flex; justify-content: flex-end; gap: 8px; margin-bottom: 15px;">
                <span style="font-size: 0.8rem; color: #64748B; font-weight: 700; align-self: center;">Exibir como:</span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #5A5A5A;">🗂 Cards</span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #94A3B8;">📋 Lista</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    clientes_filtrados = st.session_state["clientes_cadastrados"]
    if busca_cli:
        clientes_filtrados = [
            c for c in clientes_filtrados
            if busca_cli.lower() in c.get("nome", "").lower() or busca_cli in c.get("telefone", "")
        ]

    num_cols = 3
    for i in range(0, len(clientes_filtrados), num_cols):
        cols = st.columns(num_cols, gap="medium")
        for j in range(num_cols):
            if i + j < len(clientes_filtrados):
                c_item = clientes_filtrados[i + j]
                idx_real = st.session_state["clientes_cadastrados"].index(c_item) if c_item in st.session_state["clientes_cadastrados"] else i + j
                with cols[j]:
                    nome_str = c_item.get("nome", "Cliente")
                    inicial = nome_str[0].upper() if nome_str else "C"
                    tel_str = c_item.get("telefone") or "Não informado"
                    email_str = c_item.get("email") or "Não informado"
                    cad_str = c_item.get("cadastro") or "25/08/2026"
                    resp_str = c_item.get("responsavel") or "Eu"

                    st.markdown(
                        f"""
                        <div class="cli-card">
                            <div>
                                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                    <div style="display: flex; gap: 12px; align-items: center;">
                                        <div class="cli-avatar">{inicial}</div>
                                        <div>
                                            <div class="cli-nome">{nome_str}</div>
                                            <div class="cli-resp">👤 {resp_str}</div>
                                        </div>
                                    </div>
                                </div>
                                <div style="margin-top: 14px;">
                                    <div class="cli-info-line"><span>📞</span> <span>{tel_str}</span></div>
                                    <div class="cli-info-line"><span>✉</span> <span>{email_str}</span></div>
                                    <div class="cli-info-line"><span>📅</span> <span>Cadastro {cad_str}</span></div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    b_det, b_ed = st.columns(2)
                    with b_det:
                        if st.button("👁 Detalhes", key=f"det_cli_{idx_real}", use_container_width=True):
                            st.session_state["cliente_selecionado_idx"] = idx_real
                            st.session_state["tela_ativa"] = "detalhes_cliente"
                            st.rerun()
                    with b_ed:
                        if st.button("✏️ Editar", key=f"edit_cli_{idx_real}", use_container_width=True):
                            st.session_state["cliente_selecionado_idx"] = idx_real
                            st.session_state["tela_ativa"] = "editar_cliente"
                            st.rerun()

                    b_exc, b_orc_cli = st.columns(2)
                    with b_exc:
                        if st.button("🗑 Excluir", key=f"exc_cli_{idx_real}", use_container_width=True):
                            st.session_state["clientes_cadastrados"].pop(idx_real)
                            st.toast(f"Cliente {nome_str} removido!")
                            st.rerun()
                    with b_orc_cli:
                        if st.button("➕ Orçamento", key=f"add_orc_cli_{idx_real}", use_container_width=True):
                            st.session_state["orcamento_selecionado"] = {
                                "cliente": nome_str,
                                "whatsapp": c_item.get("telefone", ""),
                                "local": c_item.get("local", "Recife/PE"),
                                "largura": 3.40,
                                "altura": 1.10
                            }
                            st.session_state["tela_ativa"] = "novo_orcamento"
                            st.rerun()

# TELA 3.1: DETALHES DO CLIENTE
elif st.session_state["tela_ativa"] == "detalhes_cliente":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR PARA CLIENTES", key="btn_voltar_det_cli"):
        st.session_state["tela_ativa"] = "gerenciar_clientes"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    c_idx = st.session_state.get("cliente_selecionado_idx", 0)
    if c_idx < len(st.session_state["clientes_cadastrados"]):
        c_det = st.session_state["clientes_cadastrados"][c_idx]
        st.markdown(f"<h3 style='color:#9D201C;'>👁 Ficha do Cliente: {c_det.get('nome')}</h3>", unsafe_allow_html=True)
        
        st.markdown(
            f"""
            <div style="background: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #CBD5E1; box-shadow: 0 3px 10px rgba(0,0,0,0.04);">
                <p><b>👤 Nome / Empresa:</b> {c_det.get('nome')}</p>
                <p><b>📞 Telefone / WhatsApp:</b> {c_det.get('telefone') or 'Não informado'}</p>
                <p><b>✉ E-mail:</b> {c_det.get('email') or 'Não informado'}</p>
                <p><b>📍 Endereço / Local:</b> {c_det.get('local') or 'Não informado'}</p>
                <p><b>📅 Data de Cadastro:</b> {c_det.get('cadastro') or '25/08/2026'}</p>
                <p><b>👨‍💼 Responsável:</b> {c_det.get('responsavel', 'Eu')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("Cliente não encontrado.")

# TELA 3.2: EDITAR CLIENTE
elif st.session_state["tela_ativa"] == "editar_cliente":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR PARA CLIENTES", key="btn_voltar_edit_cli"):
        st.session_state["tela_ativa"] = "gerenciar_clientes"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    c_idx = st.session_state.get("cliente_selecionado_idx", 0)
    if c_idx < len(st.session_state["clientes_cadastrados"]):
        c_ed = st.session_state["clientes_cadastrados"][c_idx]
        st.markdown(f"<h3 style='color:#9D201C;'>✏️ Editar Cliente: {c_ed.get('nome')}</h3>", unsafe_allow_html=True)
        
        with st.form("form_editar_cliente_real"):
            ne = st.text_input("Nome do Cliente", value=c_ed.get("nome", ""))
            te = st.text_input("Telefone / WhatsApp", value=c_ed.get("telefone", ""))
            ee = st.text_input("E-mail", value=c_ed.get("email", ""))
            le = st.text_input("Endereço / Local", value=c_ed.get("local", ""))
            
            if st.form_submit_button("Salvar Alterações", type="primary"):
                if ne:
                    st.session_state["clientes_cadastrados"][c_idx] = {
                        "nome": ne.upper(),
                        "responsavel": c_ed.get("responsavel", "Eu"),
                        "telefone": te,
                        "email": ee,
                        "cadastro": c_ed.get("cadastro", datetime.now().strftime("%d/%m/%Y")),
                        "local": le
                    }
                    st.success("Dados atualizados com sucesso!")
                    st.session_state["tela_ativa"] = "gerenciar_clientes"
                    st.rerun()
                else:
                    st.warning("O nome não pode estar vazio.")

# TELA 3.3: CADASTRO DE NOVO CLIENTE
elif st.session_state["tela_ativa"] == "novo_cliente":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR PARA CLIENTES", key="btn_voltar_new_cli"):
        st.session_state["tela_ativa"] = "gerenciar_clientes"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h3 style='color:#9D201C;'>➕ Cadastrar Novo Cliente</h3>", unsafe_allow_html=True)
    with st.form("cad_cliente_form"):
        nc = st.text_input("Nome do Cliente / Empresa")
        tc = st.text_input("Telefone / WhatsApp")
        ec = st.text_input("E-mail (opcional)")
        lc = st.text_input("Endereço / Local da Instalação")
        if st.form_submit_button("Salvar Cadastro", type="primary"):
            if nc:
                st.session_state["clientes_cadastrados"].insert(0, {
                    "nome": nc.upper(),
                    "responsavel": "Eu",
                    "telefone": tc,
                    "email": ec,
                    "cadastro": datetime.now().strftime("%d/%m/%Y"),
                    "local": lc or "Recife/PE"
                })
                st.success(f"Cliente {nc} cadastrado com sucesso!")
                st.session_state["tela_ativa"] = "gerenciar_clientes"
                st.rerun()
            else:
                st.warning("Preencha o nome do cliente.")

# TELA 4: CONTROLE FINANCEIRO
elif st.session_state["tela_ativa"] == "financeiro":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR AO INÍCIO", key="btn_voltar_fin_tela"):
        st.session_state["tela_ativa"] = "inicio"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    fin_b1, fin_b2, fin_b3, fin_b4, fin_b5 = st.columns([1.5, 1.5, 3.0, 1.2, 1.2])
    with fin_b1:
        st.markdown('<div class="btn-gerar" style="margin-top: 4px;">', unsafe_allow_html=True)
        if st.button("➕ Nova Receita", key="btn_nova_receita", use_container_width=True):
            st.toast("Módulo de Nova Receita acionado.")
        st.markdown('</div>', unsafe_allow_html=True)
    with fin_b2:
        st.markdown('<div class="btn-gerar" style="margin-top: 4px; background-color: #9D201C !important;">', unsafe_allow_html=True)
        if st.button("➖ Nova Despesa", key="btn_nova_despesa", use_container_width=True):
            st.toast("Módulo de Nova Despesa acionado.")
        st.markdown('</div>', unsafe_allow_html=True)
    with fin_b4:
        st.markdown('<div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; padding: 8px; text-align: center; font-size: 0.82rem; font-weight: 700; color: #5A5A5A; margin-top: 4px; cursor: pointer;">🏷️ Categorias</div>', unsafe_allow_html=True)
    with fin_b5:
        st.markdown('<div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; padding: 8px; text-align: center; font-size: 0.82rem; font-weight: 700; color: #5A5A5A; margin-top: 4px; cursor: pointer;">👁️ Ocultar valores</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    sub_f1, sub_f2 = st.columns([2.0, 3.0])
    with sub_f1:
        st.markdown(
            """
            <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 15px;">
                <span style="background: #D01B13; color: #FFFFFF; padding: 4px 12px; border-radius: 6px; font-size: 0.82rem; font-weight: 700;">Visão Geral</span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 12px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #64748B;">Gráficos</span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 12px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #64748B;">Recebíveis</span>
                <span style="background: #FFFFFF; border: 1px solid #CBD5E1; padding: 4px 12px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; color: #64748B;">Contas a pagar</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    fc1, fc2, fc3, fc4 = st.columns(4, gap="medium")
    with fc1:
        st.markdown(
            """
            <div class="fin-top-card">
                <div class="fin-top-title">📥 Receitas recebidas</div>
                <div class="fin-top-val">R$ 3.787,85</div>
                <span class="fin-tag-realizado">Realizado</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with fc2:
        st.markdown(
            """
            <div class="fin-top-card">
                <div class="fin-top-title">📤 Despesas pagas</div>
                <div class="fin-top-val">R$ 2.462,10</div>
                <span class="fin-tag-realizado" style="background-color: #FEE2E2; color: #B91C1C;">Realizado</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with fc3:
        st.markdown(
            """
            <div class="fin-top-card">
                <div class="fin-top-title">💼 Resultado realizado</div>
                <div class="fin-top-val" style="color: #047857;">R$ 1.325,75</div>
                <span class="fin-tag-realizado" style="background-color: #D1FAE5; color: #047857;">Realizado</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with fc4:
        st.markdown(
            """
            <div class="fin-top-card">
                <div class="fin-top-title">🏢 Obras totais</div>
                <div class="fin-top-val">3</div>
                <span class="fin-tag-realizado">Realizado</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    inf_c1, inf_c2 = st.columns([1.3, 1.0], gap="large")
    with inf_c1:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <span style="font-weight: 800; color: #1E293B; font-size: 1rem;">📊 Resumo de obras</span>
                    <span style="background: #D01B13; color: #FFFFFF; padding: 4px 12px; border-radius: 16px; font-size: 0.78rem; font-weight: 700; cursor: pointer;">Ver todas as obras</span>
                </div>
                <div style="display: flex; justify-content: space-around; text-align: center; border-bottom: 1px solid #F1F5F9; padding-bottom: 12px; margin-bottom: 12px;">
                    <div>
                        <div style="font-size: 1.1rem; font-weight: 800; color: #1E293B;">3</div>
                        <div style="font-size: 0.75rem; color: #64748B; font-weight: 700;">Total de Obras</div>
                    </div>
                    <div>
                        <div style="font-size: 1.1rem; font-weight: 800; color: #047857;">1</div>
                        <div style="font-size: 0.75rem; color: #64748B; font-weight: 700;">Concluídas</div>
                    </div>
                    <div>
                        <div style="font-size: 1.1rem; font-weight: 800; color: #B45309;">2</div>
                        <div style="font-size: 0.75rem; color: #64748B; font-weight: 700;">Em Andamento</div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-around; text-align: center;">
                    <div>
                        <div style="font-size: 1.1rem; font-weight: 800; color: #9D201C;">R$ 2.459,28</div>
                        <div style="font-size: 0.75rem; color: #64748B; font-weight: 700;">Ticket médio por obra</div>
                    </div>
                    <div>
                        <div style="font-size: 1.1rem; font-weight: 800; color: #047857;">35.0%</div>
                        <div style="font-size: 0.75rem; color: #64748B; font-weight: 700;">Margem de resultado</div>
                    </div>
                    <div>
                        <div style="font-size: 1.1rem; font-weight: 800; color: #B91C1C;">0</div>
                        <div style="font-size: 0.75rem; color: #64748B; font-weight: 700;">Obras sem orçamento</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with inf_c2:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); min-height: 200px;">
                <div style="font-weight: 800; color: #1E293B; font-size: 1rem; margin-bottom: 15px;">📑 Transações Recentes</div>
                <div style="padding: 25px 0; text-align: center; color: #94A3B8; font-size: 0.85rem; font-weight: 600;">
                    Nenhuma transação neste período.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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

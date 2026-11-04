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

# 2. CSS Global com degradê real cobrindo toda a tela e abas 100% vermelhas
css_code = """<style>
/* DEGRADÊ VERMELHO + BRANCO NA PÁGINA INTEIRA */
html, body, [data-testid="stAppViewContainer"], .stApp, section.main {
background: linear-gradient(160deg, #FADBD8 0%, #FFFFFF 35%, #FDE8E7 70%, #FFFFFF 100%) !important;
background-attachment: fixed !important;
}

p, span, label, .stMarkdown {
color: #5A5A5A !important;
font-weight: 600;
}

/* CARDS DO MENU PRINCIPAL */
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
font-size: 1.25rem;
font-weight: 800;
margin: 0;
text-align: center;
letter-spacing: 0.5px;
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

/* CARDS DE MÉTRICAS */
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

/* CARDS DA LISTA DE ORÇAMENTOS */
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

/* CARDS DA LISTA DE CLIENTES */
.cli-card {
background-color: #FFFFFF;
border-radius: 10px;
border: 1px solid #E2E8F0;
border-top: 4px solid #D01B13;
box-shadow: 0 3px 12px rgba(0,0,0,0.05);
padding: 16px;
margin-bottom: 15px;
position: relative;
min-height: 180px;
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

/* INPUTS */
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

/* BOTÕES INFERIORES */
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

# 3. Cabeçalho IDÊNTICO ao seu código
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

# 4. Controle de Telas e Memória
if "tela_ativa" not in st.session_state:
    st.session_state["tela_ativa"] = "inicio"

if "orcamento_selecionado" not in st.session_state:
    st.session_state["orcamento_selecionado"] = None

if "historico_orcamentos" not in st.session_state:
    st.session_state["historico_orcamentos"] = [
        {"id": "2608251804903", "cliente": "HEMOSAN MT", "data": "25/08/2026", "autor": "Eu", "status": "Em Analise", "projeto": "Guarda-Corpo / Sacada (NBR 14718)", "largura": 3.40, "altura": 1.10, "valor": 3787.85, "local": "Boa Viagem - Recife/PE", "whatsapp": "81991234567"},
        {"id": "2608241802746", "cliente": "IVONE", "data": "24/08/2026", "autor": "Eu", "status": "Em Analise", "projeto": "Box Frontal Padrão (1 Fixo + 1 Móvel)", "largura": 1.20, "altura": 1.90, "valor": 1250.00, "local": "Janga - Paulista/PE", "whatsapp": "81988776655"},
        {"id": "26081417888936", "cliente": "MARCOS EMANUEL JUNIOR DE ALMEIDA NUNES LEITE", "data": "14/08/2026", "autor": "Eu", "status": "Aprovado", "projeto": "Janela 4 Folhas (2 Fixos + 2 Móveis)", "largura": 2.00, "altura": 1.20, "valor": 2180.00, "local": "Casa Forte - Recife/PE", "whatsapp": "81977665544"},
        {"id": "2608141788888", "cliente": "POSTURE SAUDE E CIENCIA", "data": "14/08/2026", "autor": "Eu", "status": "Em Analise", "projeto": "Porta Pivotante de Abrir (1 Folha)", "largura": 1.00, "altura": 2.10, "valor": 1940.00, "local": "Ilha do Leite - Recife/PE", "whatsapp": "81999881122"},
        {"id": "2608051771714", "cliente": "CLÍNICA PRÁXIS", "data": "05/08/2026", "autor": "Eu", "status": "Em Analise", "projeto": "Guarda-Corpo / Sacada (NBR 14718)", "largura": 4.10, "altura": 1.10, "valor": 4520.00, "local": "Espinheiro - Recife/PE", "whatsapp": "81998877665"},
        {"id": "2605151644433", "cliente": "CONDOMINIO EDIFICIO PORTAL DO BOSQUE", "data": "15/05/2026", "autor": "Eu", "status": "Em Analise", "projeto": "Guarda-Corpo / Sacada (NBR 14718)", "largura": 6.80, "altura": 1.10, "valor": 7890.00, "local": "Pina - Recife/PE", "whatsapp": "81987654321"},
    ]

if "clientes_cadastrados" not in st.session_state:
    st.session_state["clientes_cadastrados"] = [
        {"nome": "HEMOSAN MT", "responsavel": "Eu", "telefone": "81991234567", "email": "", "cadastro": "25/08/2026", "local": "Boa Viagem - Recife/PE"},
        {"nome": "IVONE", "responsavel": "Eu", "telefone": "81988776655", "email": "", "cadastro": "24/08/2026", "local": "Janga - Paulista/PE"},
        {"nome": "MARCOS EMANUEL JUNIOR DE ALMEIDA NUNES LEITE", "responsavel": "Eu", "telefone": "81977665544", "email": "", "cadastro": "14/08/2026", "local": "Recife/PE"},
        {"nome": "SABOR DA TERRA", "responsavel": "Eu", "telefone": "", "email": "", "cadastro": "11/05/2026", "local": "Paulista/PE"},
        {"nome": "MARCOS AURELIO NOGUEIRA", "responsavel": "Eu", "telefone": "", "email": "", "cadastro": "11/05/2026", "local": "Olinda/PE"},
        {"nome": "POSTURE SAUDE E CIENCIA", "responsavel": "Eu", "telefone": "81999881122", "email": "", "cadastro": "04/05/2026", "local": "Recife/PE"},
        {"nome": "FLAVIA CAMPANO", "responsavel": "Eu", "telefone": "", "email": "", "cadastro": "23/04/2026", "local": "Janga/PE"},
        {"nome": "EUNICE", "responsavel": "Eu", "telefone": "(65) 9 8448-7060", "email": "", "cadastro": "07/04/2026", "local": "Recife/PE"},
        {"nome": "COND CHAPADA CESARI", "responsavel": "Eu", "telefone": "(66) 9 9622-8589", "email": "", "cadastro": "07/04/2026", "local": "Paulista/PE"},
    ]

# SINCRONIZAÇÃO AUTOMÁTICA DE CLIENTES DOS ORÇAMENTOS (INCLUINDO MARIANA ETC)
nomes_existentes_cli = {c["nome"].upper() for c in st.session_state["clientes_cadastrados"]}
for orc in st.session_state["historico_orcamentos"]:
    c_nome = orc.get("cliente", "").strip().upper()
    if c_nome and c_nome not in nomes_existentes_cli:
        st.session_state["clientes_cadastrados"].append({
            "nome": c_nome,
            "responsavel": orc.get("autor", "Eu"),
            "telefone": orc.get("whatsapp", ""),
            "email": "",
            "cadastro": orc.get("data", datetime.now().strftime("%d/%m/%Y")),
            "local": orc.get("local", "Recife/PE")
        })
        nomes_existentes_cli.add(c_nome)

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
                st.session_state["tela_ativa"] = "novo_orcamento"
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
                st.session_state["tela_ativa"] = "gerenciar_clientes"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_cl2:
            st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
            if st.button("📋 LISTAR", key="card_btn_list_cli", use_container_width=True):
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

# TELA 2: FORMULÁRIO DE ORÇAMENTO / CÁLCULO DE VÃO
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

        st.success(f"Lucro Bruto Estimado: R$ {res['lucro']:.2f} ({res['margem']}%)")

        st.markdown("<h5 style='color:#9D201C; font-weight:800; margin-top:15px;'>Plano de Corte dos Vidros</h5>", unsafe_allow_html=True)
        st.dataframe(res["pecas"], use_container_width=True)

        dados_pdf = {
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
        
        pdf_bytes = gerar_pdf(dados_pdf)
        
        st.markdown('<div class="btn-pdf">', unsafe_allow_html=True)
        st.download_button(
            label="📄 BAIXAR ORÇAMENTO EM PDF",
            data=pdf_bytes,
            file_name=f"Orcamento_{nome_c.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

# TELA 3: GERENCIAR CLIENTES
elif st.session_state["tela_ativa"] == "gerenciar_clientes":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR AO INÍCIO", key="btn_voltar_cli"):
        st.session_state["tela_ativa"] = "inicio"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Gestão de Clientes")

    termo_cli = st.text_input("Buscar Cliente", placeholder="🔍 Pesquise por nome, local, telefone...", label_visibility="collapsed")

    lista_cli_exibir = st.session_state["clientes_cadastrados"]
    if termo_cli:
        lista_cli_exibir = [
            c for c in lista_cli_exibir
            if termo_cli.lower() in c.get("nome", "").lower() or termo_cli.lower() in c.get("local", "").lower() or termo_cli in c.get("telefone", "")
        ]

    if "cliente_em_edicao" not in st.session_state:
        st.session_state["cliente_em_edicao"] = None
    if "cliente_detalhes" not in st.session_state:
        st.session_state["cliente_detalhes"] = None

    # TELA DE EDIÇÃO DO CLIENTE
    if st.session_state["cliente_em_edicao"] is not None:
        idx = st.session_state["cliente_em_edicao"]
        cli = st.session_state["clientes_cadastrados"][idx]
        st.markdown(f"### Editando Cliente: {cli['nome']}")
        with st.form("form_edita_cliente"):
            novo_nome = st.text_input("Nome do Cliente", value=cli["nome"])
            novo_resp = st.text_input("Responsável", value=cli.get("responsavel", "Eu"))
            novo_tel = st.text_input("Telefone / WhatsApp", value=cli.get("telefone", ""))
            novo_email = st.text_input("E-mail", value=cli.get("email", ""))
            novo_loc = st.text_input("Local / Endereço", value=cli.get("local", ""))
            
            col_salvar, col_cancelar = st.columns(2)
            with col_salvar:
                if st.form_submit_button("💾 Salvar Alterações", use_container_width=True):
                    st.session_state["clientes_cadastrados"][idx] = {
                        "nome": novo_nome.upper(),
                        "responsavel": novo_resp,
                        "telefone": novo_tel,
                        "email": novo_email,
                        "cadastro": cli.get("cadastro", datetime.now().strftime("%d/%m/%Y")),
                        "local": novo_loc
                    }
                    st.session_state["cliente_em_edicao"] = None
                    st.success("Cliente atualizado com sucesso!")
                    st.rerun()
            with col_cancelar:
                if st.form_submit_button("❌ Cancelar", use_container_width=True):
                    st.session_state["cliente_em_edicao"] = None
                    st.rerun()
    else:
        # EXIBIÇÃO DOS CARDS DE CLIENTES
        num_cols = 3
        for i in range(0, len(lista_cli_exibir), num_cols):
            cols = st.columns(num_cols, gap="medium")
            for j in range(num_cols):
                if i + j < len(lista_cli_exibir):
                    cli = lista_cli_exibir[i + j]
                    orig_idx = st.session_state["clientes_cadastrados"].index(cli)
                    with cols[j]:
                        st.markdown(
                            f"""
                            <div class="cli-card">
                                <div>
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <div class="cli-avatar">{cli['nome'][:1]}</div>
                                        <span style="font-size:0.75rem; color:#64748B; font-weight:700;">Cad: {cli.get('cadastro', '')}</span>
                                    </div>
                                    <div class="cli-nome" style="margin-top: 8px;">{cli['nome']}</div>
                                    <div class="cli-resp">Resp: {cli.get('responsavel', 'Eu')}</div>
                                    <div class="cli-info-line">📍 {cli.get('local', 'Não informado')}</div>
                                    <div class="cli-info-line">📞 {cli.get('telefone', 'Não informado')}</div>
                                    {f"<div class='cli-info-line'>✉️ {cli.get('email')}</div>" if cli.get('email') else ""}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        b_det, b_edit = st.columns(2)
                        with b_det:
                            if st.button("👁 Detalhes", key=f"det_cli_{orig_idx}", use_container_width=True):
                                st.session_state["cliente_detalhes"] = cli['nome']
                                st.rerun()
                        with b_edit:
                            if st.button("✏️ Editar", key=f"edit_cli_{orig_idx}", use_container_width=True):
                                st.session_state["cliente_em_edicao"] = orig_idx
                                st.rerun()

        # MODAL / SEÇÃO DE DETALHES DO CLIENTE SELECIONADO
        if st.session_state["cliente_detalhes"]:
            cli_nome_det = st.session_state["cliente_detalhes"]
            st.markdown("---")
            st.markdown(f"### Detalhes e Orçamentos de: **{cli_nome_det}**")
            orcamentos_cliente = [o for o in st.session_state["historico_orcamentos"] if o.get("cliente", "").upper() == cli_nome_det.upper()]
            if orcamentos_cliente:
                for orc in orcamentos_cliente:
                    st.info(f"**Orçamento #{orc.get('id')}** — Projeto: {orc.get('projeto')} | Valor: R$ {orc.get('valor', 0):.2f} | Status: {orc.get('status')} | Data: {orc.get('data')}")
            else:
                st.warning("Nenhum orçamento vinculado a este cliente no momento.")
            
            if st.button("❌ Fechar Detalhes", key="fechar_det_cli"):
                st.session_state["cliente_detalhes"] = None
                st.rerun()

# TELAS SECUNDÁRIAS (FINANCEIRO E CORTE/TÊMPERA)
elif st.session_state["tela_ativa"] in ["financeiro", "tempera"]:
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅ VOLTAR AO INÍCIO", key="btn_voltar_outros"):
        st.session_state["tela_ativa"] = "inicio"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.info(f"Módulo **{st.session_state['tela_ativa'].upper()}** em desenvolvimento.")

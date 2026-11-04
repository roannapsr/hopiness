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
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO GERAL DA PÁGINA E CSS PERSONALIZADO
# ==============================================================================
st.set_page_config(
    page_title="HOPINESS PROJECT by Felipe Correa",
    page_icon="🪟",
    layout="wide",
)

st.markdown(
    """
    <style>
        /* Fundo limpo e tipografia */
        .stApp {
            background-color: #F8FAFC;
        }
        
        /* CORREÇÃO DAS ABAS (Fim do texto branco invisível) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: #E2E8F0;
            padding: 8px 10px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .stTabs [data-baseweb="tab"] {
            color: #475569 !important; /* Cinza escuro legível quando inativa */
            font-weight: 700 !important;
            font-size: 0.92rem !important;
            padding: 8px 18px !important;
            border-radius: 8px !important;
            background-color: transparent !important;
            border: none !important;
        }
        .stTabs [aria-selected="true"] {
            color: #0D253A !important; /* Azul marinho na aba ativa */
            background-color: #FFFFFF !important; /* Fundo branco destacado */
            box-shadow: 0 2px 6px rgba(0,0,0,0.08) !important;
        }
        
        /* Cards Informativos */
        .custom-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }
        .custom-card-title {
            color: #0D253A;
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 6px;
        }
        .custom-card-desc {
            color: #475569;
            font-size: 0.88rem;
            line-height: 1.4;
        }
        
        /* Botões Primários */
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
        
        /* Métricas */
        div[data-testid="stMetricValue"] {
            color: #0D253A !important;
            font-weight: 800 !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# CABEÇALHO PADRÃO
# ==============================================================================
st.markdown(
    """
    <div style="margin-top: -20px; margin-bottom: 20px; border-bottom: 2px solid #CBD5E1; padding-bottom: 12px;">
        <h1 style="text-align: center; color: #0D253A; font-size: 2.3rem; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; text-transform: uppercase;">
            HOPINESS PROJECT
        </h1>
        <p style="text-align: right; color: #64748B; font-size: 0.95rem; font-weight: 500; font-style: italic; margin-top: 2px; margin-bottom: 0px; padding-right: 10px;">
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
                "Exige-se vidro de segurança. O vidro temperado de 8mm oferece"
                " resistência térmica e mecânica ideal para área molhada."
            ),
        },
        "2": {
            "aplicacao": "Guarda-Corpo / Sacada",
            "vidros_permitidos": ["Laminado 10mm+", "Laminado-Temperado"],
            "norma_tecnica": "ABNT NBR 14718 / NBR 7199",
            "explicacao": (
                "Proibido vidro temperado monolítico. Exige-se laminação com"
                " PVB para garantir retenção mecânica e impedir queda em"
                " altura."
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
                " estilhaços suspensos em caso de quebra."
            ),
        },
        "4": {
            "aplicacao": "Porta / Janela (Abaixo de 1,10m)",
            "vidros_permitidos": ["Temperado 8mm/10mm", "Laminado 8mm"],
            "norma_tecnica": "ABNT NBR 7199",
            "explicacao": (
                "Zona de impacto humano acidental. Exige vidro de segurança"
                " conforme a cota de piso acabado."
            ),
        },
        "5": {
            "aplicacao": "Divisória de Ambiente / Fechamento de Vão",
            "vidros_permitidos": ["Temperado 8mm/10mm", "Laminado"],
            "norma_tecnica": "ABNT NBR 7199",
            "explicacao": (
                "Vidro temperado confere grande rigidez e segurança estrutural"
                " com ferragens de pressão."
            ),
        },
        "6": {
            "aplicacao": "Espelho Decorativo",
            "vidros_permitidos": ["Espelho Prata (com proteção química)"],
            "norma_tecnica": "ABNT NBR 15198",
            "explicacao": (
                "Fixação química obrigatória com silicone neutro específico"
                " para preservar a película espelhada de prata."
            ),
        },
        "7": {
            "aplicacao": "Prateleira / Tampo de Mesa",
            "vidros_permitidos": ["Temperado", "Monolítico Lapidado"],
            "norma_tecnica": "Boas Práticas da Indústria",
            "explicacao": (
                "Dimensionamento proporcional à carga e aos pontos de suporte"
                " mecânico."
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
  CINZA_TEXTO = colors.HexColor("#334155")
  CINZA_SUAVE = colors.HexColor("#64748B")
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
          "<font size='8' color='#64748B'>VALOR TOTAL DA PROPOSTA</font><br/>"
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
                <b>Resistência:</b> 5x mais resistente que o comum.<br/>
                <b>Quebra:</b> Fragmenta-se em pequenos pedaços pouco cortantes.<br/>
                <b>Ideal para:</b> Box de banheiro, portas, divisórias e tampos.
            </div>
        </div>
        <div class="custom-card">
            <div class="custom-card-title">🔹 Vidro Laminado (Segurança Máxima)</div>
            <div class="custom-card-desc">
                <b>Resistência:</b> Duas ou mais lâminas unidas por película de PVB.<br/>
                <b>Quebra:</b> Os fragmentos ficam retidos na película sem abrir vão.<br/>
                <b>Ideal para:</b> Guarda-corpos, sacadas, coberturas e claraboias.
            </div>
        </div>
        <div class="custom-card">
            <div class="custom-card-title">🔹 Vidro Insulado / Duplo</div>
            <div class="custom-card-desc">
                <b>Benefício:</b> Dupla lâmina com câmara de ar ou gás desidratado.<br/>
                <b>Destaque:</b> Máximo isolamento acústico e controle térmico.<br/>
                <b>Ideal para:</b> Fachadas, estúdios e residências em áreas barulhentas.
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
                <b>Benefício:</b> Bloqueia até 70% do calor e 99% dos raios UV.<br/>
                <b>Destaque:</b> Mantém o ambiente fresco e protege pisos/móveis.<br/>
                <b>Ideal para:</b> Sacadas poentes, coberturas e fachadas ensolaradas.
            </div>
        </div>
        <div class="custom-card">
            <div class="custom-card-title">🔹 Vidros Acidados & Serigrafados</div>
            <div class="custom-card-desc">
                <b>Benefício:</b> Acabamento translúcido e fosco toque de seda.<br/>
                <b>Destaque:</b> Não mancha com facilidade e garante privacidade.<br/>
                <b>Ideal para:</b> Portas de armário, divisórias de escritório e lavabos.
            </div>
        </div>
        <div class="custom-card">
            <div class="custom-card-title">🔹 Espelhos com Camada Protetora</div>
            <div class="custom-card-desc">
                <b>Benefício:</b> Base de prata pura com película ecológica.<br/>
                <b>Destaque:</b> Alta durabilidade contra oxidação e manchas pretas.<br/>
                <b>Ideal para:</b> Banheiros, painéis de sala, academias e closets.
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
          "🛡️ Especificação 100% em conformidade com as normas ABNT.\n\n"
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
        <div style="background-color:#E2E8F0; padding:10px; border-radius:8px; text-align:center; font-weight:700; color:#0D253A; margin-bottom:10px;">
            🟡 Orçamento Aberto (2)
        </div>
        <div class="custom-card">
            <b>#1024 - Carlos Silva</b><br/>
            Box Elegance Incolor 8mm<br/>
            <small style="color:#64748B;">Aguardando retorno do cliente</small>
        </div>
        <div class="custom-card">
            <b>#1025 - Ed. Costa Dourada</b><br/>
            Espelho Prata Bisotado 4mm<br/>
            <small style="color:#64748B;">Enviado via WhatsApp hoje</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with c_k2:
    st.markdown(
        """
        <div style="background-color:#FED7AA; padding:10px; border-radius:8px; text-align:center; font-weight:700; color:#9A3412; margin-bottom:10px;">
            🟠 Pedido na Têmpera (1)
        </div>
        <div class="custom-card">
            <b>#1022 - Roberta Maia</b><br/>
            Vidro Laminado 10mm (Guarda-Corpo)<br/>
            <small style="color:#64748B;">Previsão de entrega: 2 dias</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with c_k3:
    st.markdown(
        """
        <div style="background-color:#BAE6FD; padding:10px; border-radius:8px; text-align:center; font-weight:700; color:#0369A1; margin-bottom:10px;">
            🔵 Rota de Instalação (1)
        </div>
        <div class="custom-card">
            <b>#1020 - Mariana Albuquerque</b><br/>
            Sacada Completa c/ Torres Inox<br/>
            <small style="color:#64748B;">Equipe em deslocamento</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with c_k4:
    st.markdown(
        """
        <div style="background-color:#BBF7D0; padding:10px; border-radius:8px; text-align:center; font-weight:700; color:#166534; margin-bottom:10px;">
            🟢 Concluído & Faturado (4)
        </div>
        <div class="custom-card">
            <b>#1018 - Escritório Pina</b><br/>
            Divisória Acústica 10mm<br/>
            <small style="color:#166534;"><b>Saldo 100% quitado</b></small>
        </div>
        """,
        unsafe_allow_html=True,
    )

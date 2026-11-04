import io
import math
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
# CONFIGURAÇÃO DE TEMA E IDENTIDADE VISUAL
# ==============================================================================
# Paleta de Cores:
# Azul Marinho Principal: #0D253A
# Azul Marinho Médio: #1E3A5F
# Cinza Claro Fundo: #F8FAFC
# Cinza Borda / Detalhe: #E2E8F0
# Texto Neutro: #64748B
# Branco: #FFFFFF


# ==============================================================================
# 1. MOTOR DE RECOMENDAÇÃO TÉCNICA (ABNT NBR 7199 / 14207 / 14718)
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
                "Pela NBR 14207, exige-se vidro de segurança. O vidro temperado"
                " de 8mm é o padrão normativo de mercado."
            ),
        },
        "2": {
            "aplicacao": "Guarda-Corpo / Sacada",
            "vidros_permitidos": ["Laminado 10mm+", "Laminado-Temperado"],
            "norma_tecnica": "ABNT NBR 14718 / ABNT NBR 7199",
            "explicacao": (
                "É expressamente proibido o uso de vidro temperado monolítico."
                " Exige-se vidro laminado para reter fragmentos e impedir queda"
                " em altura."
            ),
        },
        "3": {
            "aplicacao": "Cobertura / Clarabóia",
            "vidros_permitidos": [
                "Laminado",
                "Insulado com lâmina inferior laminada",
            ],
            "norma_tecnica": "ABNT NBR 7199",
            "explicacao": (
                "Para evitar queda de estilhaços sobre pessoas em caso de"
                " quebra, a face inferior deve ser obrigatoriamente laminada."
            ),
        },
        "4": {
            "aplicacao": "Porta / Janela (Abaixo de 1,10m)",
            "vidros_permitidos": ["Temperado 8mm/10mm", "Laminado 8mm"],
            "norma_tecnica": "ABNT NBR 7199",
            "explicacao": (
                "Instalações abaixo de 1,10m em relação ao piso exigem vidro de"
                " segurança contra impactos acidentais."
            ),
        },
        "5": {
            "aplicacao": "Divisória de Ambiente / Fechamento de Vão",
            "vidros_permitidos": ["Temperado 8mm/10mm", "Laminado"],
            "norma_tecnica": "ABNT NBR 7199",
            "explicacao": (
                "Exige-se vidro de segurança com ancoragem adequada para grandes"
                " vãos estruturais."
            ),
        },
        "6": {
            "aplicacao": "Espelho Decorativo",
            "vidros_permitidos": ["Espelho Prata (com proteção química)"],
            "norma_tecnica": "ABNT NBR 15198",
            "explicacao": (
                "Fixação com adesivo neutro/silicone para espelhos para evitar a"
                " oxidação da prata."
            ),
        },
        "7": {
            "aplicacao": "Prateleira / Tampo de Mesa",
            "vidros_permitidos": ["Temperado", "Monolítico Lapidado"],
            "norma_tecnica": "Boas Práticas da Indústria",
            "explicacao": (
                "Dimensionamento proporcional aos pontos de apoio e à carga"
                " distribuída."
            ),
        },
    }
    return recomendacoes.get(opcao_aplicacao, None)


# ==============================================================================
# 2. CALCULADORA COMERCIAL (FOLGA DE 50MM E MARGEM)
# ==============================================================================
class CalculadoraOrcamento:
  STEP_COMERCIAL_M = 0.05  # Arredondamento comercial de 50mm

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
# 3. GERADOR DE PDF PROFISSIONAL COM NOVA PALETA
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
  AZUL_MEDIO = colors.HexColor("#1E3A5F")
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
      alignment=1,  # Centralizado
  )
  style_sub_author = ParagraphStyle(
      "SubAuthor",
      parent=styles["Normal"],
      fontName="Helvetica-Oblique",
      fontSize=9.5,
      leading=13,
      textColor=CINZA_SUAVE,
      alignment=2,  # Direcionado à direita
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

  # Topo do Documento: Título Centralizado + Autor à Direita
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

  # Dados do Cliente e Projeto
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

  # Tabela de Composição
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

  # Fechamento Financeiro
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
# 4. APLICAÇÃO WEB STREAMLIT
# ==============================================================================
def main():
  st.set_page_config(
      page_title="HOPINESS PROJECT by Felipe Correa",
      page_icon="🪟",
      layout="wide",
  )

  # Custom CSS para aplicar a paleta: Azul Marinho, Cinza Claro e Branco
  st.markdown(
      """
        <style>
            /* Cores de fundo e botões */
            .stApp {
                background-color: #FFFFFF;
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
            }
            .stTabs [data-baseweb="tab"] {
                color: #0D253A;
                font-weight: 600;
            }
            div[data-testid="stMetricValue"] {
                color: #0D253A;
                font-weight: 700;
            }
            /* Botões primários em Azul Marinho */
            .stButton > button[kind="primary"] {
                background-color: #0D253A !important;
                color: #FFFFFF !important;
                border-radius: 6px;
                border: none;
                font-weight: 600;
            }
            .stButton > button[kind="primary"]:hover {
                background-color: #1E3A5F !important;
            }
            /* Download button */
            .stDownloadButton > button {
                background-color: #1E3A5F !important;
                color: #FFFFFF !important;
                border-radius: 6px;
                font-weight: 600;
            }
        </style>
    """,
      unsafe_allow_html=True,
  )

  # Cabeçalho Principal: HOPINESS PROJECT centralizado em destaque + by Felipe Correa à direita
  st.markdown(
      """
        <div style="margin-top: -15px; margin-bottom: 25px; border-bottom: 2px solid #E2E8F0; padding-bottom: 12px;">
            <h1 style="text-align: center; color: #0D253A; font-size: 2.4rem; font-weight: 800; letter-spacing: 2px; margin-bottom: 0px; text-transform: uppercase;">
                HOPINESS PROJECT
            </h1>
            <p style="text-align: right; color: #64748B; font-size: 0.95rem; font-weight: 400; font-style: italic; margin-top: 2px; margin-bottom: 0px; padding-right: 10px;">
                by Felipe Correa
            </p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  aba1, aba2 = st.tabs(
      ["📋 Consultoria Técnica (ABNT)", "💰 Calculadora de Orçamentos"]
  )

  with aba1:
    st.markdown(
        "<h3 style='color:#0D253A;'>Especificações e Normas Técnicas</h3>",
        unsafe_allow_html=True,
    )
    opcao = st.selectbox(
        "Selecione o local de aplicação do vidro:",
        options=list(RecomendadorTecnico.APLICACOES.keys()),
        format_func=lambda x: RecomendadorTecnico.APLICACOES[x],
    )
    rec = RecomendadorTecnico.recomendar(opcao)
    if rec:
      c1, c2 = st.columns(2)
      c1.metric("Norma Regulamentadora", rec["norma_tecnica"])
      c2.metric("Vidros Indicados", ", ".join(rec["vidros_permitidos"]))
      st.info(f"🛡️ **Diretriz Técnica de Segurança:** {rec['explicacao']}")

  with aba2:
    st.markdown(
        "<h3 style='color:#0D253A;'>Composição Comercial da Proposta</h3>",
        unsafe_allow_html=True,
    )

    col_cli1, col_cli2 = st.columns(2)
    cliente_nome = col_cli1.text_input("Nome do Cliente", "Mariana Albuquerque")
    cliente_local = col_cli2.text_input(
        "Local da Instalação", "Boa Viagem - Recife/PE"
    )

    c1, c2 = st.columns(2)
    with c1:
      st.markdown("##### 1. Dimensões do Vão")
      largura = st.number_input(
          "Largura (m)",
          min_value=0.1,
          max_value=10.0,
          value=3.40,
          step=0.05,
      )
      altura = st.number_input(
          "Altura (m)",
          min_value=0.1,
          max_value=10.0,
          value=1.10,
          step=0.05,
      )
      folhas = st.number_input(
          "Quantidade de Peças/Folhas", min_value=1, max_value=20, value=3
      )
      preco_m2 = st.number_input(
          "Custo do Vidro/m² (R$)", min_value=0.0, value=380.0, step=10.0
      )

    with c2:
      st.markdown("##### 2. Ferragens, Insumos e Margem")
      custo_kits = st.number_input(
          "Kits / Ferragens (R$)", min_value=0.0, value=570.0, step=10.0
      )
      custo_insumos = st.number_input(
          "Insumos / Fixadores (R$)", min_value=0.0, value=120.0, step=5.0
      )
      custo_mo = st.number_input(
          "Mão de Obra e Instalação (R$)",
          min_value=0.0,
          value=450.0,
          step=10.0,
      )
      margem = st.slider(
          "Margem de Lucro Desejada (%)",
          min_value=5.0,
          max_value=70.0,
          value=35.0,
      )

    if st.button("Gerar Proposta Comercial", type="primary"):
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
      m2.metric(
          "Área Faturada (+Folga)", f"{res['area_faturada_total']:.2f} m²"
      )
      m3.metric("Custo Direto", f"R$ {res['custo_direto_total']:.2f}")
      m4.metric("Preço Sugerido", f"R$ {res['preco_venda_final']:.2f}")

      st.success(
          f"**Margem de Lucro Bruta:** R$ {res['lucro_bruto']:.2f} ("
          f"{res['margem_aplicada_pct']}%)"
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
      st.download_button(
          label="📥 Baixar Orçamento em PDF (Formato WhatsApp)",
          data=pdf_bytes,
          file_name=(
              f"Orcamento_Hopiness_{cliente_nome.replace(' ', '_')}.pdf"
          ),
          mime="application/pdf",
      )


if __name__ == "__main__":
  main()

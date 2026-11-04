import io
import math
import sys
from datetime import datetime
import streamlit as st
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
                " de 8mm é o padrão de mercado, podendo utilizar película de"
                " proteção ou vidro laminado."
            ),
        },
        "2": {
            "aplicacao": "Guarda-Corpo / Sacada",
            "vidros_permitidos": ["Laminado 10mm+", "Laminado-Temperado"],
            "norma_tecnica": "ABNT NBR 14718 / ABNT NBR 7199",
            "explicacao": (
                "É expressamente proibido o uso de vidro temperado monolítico."
                " Exige-se vidro laminado para garantir a retenção do usuário"
                " em caso de quebra."
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
                "Para evitar a queda de fragmentos em caso de quebra, a lâmina"
                " inferior deve ser obrigatoriamente laminada."
            ),
        },
        "4": {
            "aplicacao": "Porta / Janela (Abaixo de 1,10m)",
            "vidros_permitidos": ["Temperado 8mm/10mm", "Laminado 8mm"],
            "norma_tecnica": "ABNT NBR 7199",
            "explicacao": (
                "Vidros instalados abaixo de 1,10m do piso devem utilizar"
                " vidros de segurança contra impactos acidentais."
            ),
        },
        "5": {
            "aplicacao": "Divisória de Ambiente / Fechamento de Vão",
            "vidros_permitidos": ["Temperado 8mm/10mm", "Laminado"],
            "norma_tecnica": "ABNT NBR 7199",
            "explicacao": (
                "Exige-se vidro de segurança. Vidros temperados de 8mm ou 10mm"
                " estruturam grandes vãos com excelência mecânica."
            ),
        },
        "6": {
            "aplicacao": "Espelho Decorativo",
            "vidros_permitidos": ["Espelho Prata (Monolítico com proteção)"],
            "norma_tecnica": "ABNT NBR 15198",
            "explicacao": (
                "Espelhos devem ter proteção posterior contra oxidação e"
                " fixação com silicone neutro específico para espelho."
            ),
        },
        "7": {
            "aplicacao": "Prateleira / Tampo de Mesa",
            "vidros_permitidos": ["Temperado", "Monolítico Lapidado"],
            "norma_tecnica": "Boas Práticas da Indústria",
            "explicacao": (
                "A espessura deve ser dimensionada conforme os apoios e a carga"
                " distribuída prevista."
            ),
        },
    }
    return recomendacoes.get(opcao_aplicacao, None)


# ==============================================================================
# 2. CALCULADORA DE ORÇAMENTOS E PRECIFICAÇÃO
# ==============================================================================
class CalculadoraOrcamento:
  STEP_COMERCIAL_M = 0.05  # Passo de arredondamento de 50mm

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
# 3. GERADOR DE PDF PROFISSIONAL (REPORTLAB)
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

  AZUL_PRIMARIO = colors.HexColor("#0D3B66")
  AZUL_SECUNDARIO = colors.HexColor("#0077B6")
  CINZA_FUNDO = colors.HexColor("#F8F9FA")
  CINZA_TEXTO = colors.HexColor("#333333")
  CINZA_CLARO = colors.HexColor("#E5E9EC")
  BRANCO = colors.white

  styles = getSampleStyleSheet()

  style_title = ParagraphStyle(
      "Title",
      parent=styles["Normal"],
      fontName="Helvetica-Bold",
      fontSize=18,
      leading=22,
      textColor=AZUL_PRIMARIO,
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
  style_sub = ParagraphStyle(
      "Sub",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=8.5,
      leading=12,
      textColor=AZUL_SECUNDARIO,
  )
  style_card = ParagraphStyle(
      "Card",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=8,
      leading=11,
      textColor=CINZA_TEXTO,
  )
  style_th = ParagraphStyle(
      "TH",
      parent=styles["Normal"],
      fontName="Helvetica-Bold",
      fontSize=8,
      leading=10,
      textColor=BRANCO,
  )
  style_td = ParagraphStyle(
      "TD",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=8,
      leading=10,
      textColor=CINZA_TEXTO,
  )
  style_td_r = ParagraphStyle(
      "TDR",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=8,
      leading=10,
      alignment=2,
      textColor=CINZA_TEXTO,
  )

  story = []

  # Cabeçalho
  header_data = [
      [
          Paragraph("<b>Hopeness Vidros & Soluções</b>", style_title),
          Paragraph(
              f"<b>PROPOSTA COMERCIAL</b><br/><b>Data:</b>"
              f" {datetime.now().strftime('%d/%m/%Y')}<br/><b>Validade:</b> 10"
              " dias",
              style_meta,
          ),
      ],
      [
          Paragraph(
              "Vidraçaria e Engenharia de Vidros Planos | WhatsApp: (81)"
              " 98888-7777",
              style_sub,
          ),
          "",
      ],
  ]
  t_header = Table(header_data, colWidths=[11.0 * cm, 7.0 * cm])
  t_header.setStyle(
      TableStyle([
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("SPAN", (1, 0), (1, 1)),
      ])
  )
  story.append(t_header)
  story.append(Spacer(1, 0.2 * cm))
  story.append(
      HRFlowable(
          width="100%",
          thickness=1.5,
          color=AZUL_PRIMARIO,
          spaceBefore=1,
          spaceAfter=6,
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
          ("BOX", (0, 0), (-1, -1), 0.5, CINZA_CLARO),
          ("TOPPADDING", (0, 0), (-1, -1), 5),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
      ])
  )
  story.append(t_info)
  story.append(Spacer(1, 0.3 * cm))

  # Tabela de Valores
  table_rows = [
      [
          Paragraph("Item / Descrição", style_th),
          Paragraph("Total", ParagraphStyle("THR", parent=style_th, alignment=2)),
      ],
      [
          Paragraph("Vidros Especificados (c/ folgas de lapidação)", style_td),
          Paragraph(f"R$ {dados['custo_vidro']:.2f}", style_td_r),
      ],
      [
          Paragraph("Kits, Perfis e Ferragens de Fixação", style_td),
          Paragraph(f"R$ {dados['custo_ferragens']:.2f}", style_td_r),
      ],
      [
          Paragraph("Insumos Técnicos e Fixadores", style_td),
          Paragraph(f"R$ {dados['custo_insumos']:.2f}", style_td_r),
      ],
      [
          Paragraph("Mão de Obra de Instalação Especializada", style_td),
          Paragraph(f"R$ {dados['custo_mo']:.2f}", style_td_r),
      ],
  ]
  t_itens = Table(table_rows, colWidths=[13.5 * cm, 4.5 * cm])
  t_itens.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, 0), AZUL_PRIMARIO),
          ("GRID", (0, 0), (-1, -1), 0.5, CINZA_CLARO),
          ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BRANCO, CINZA_FUNDO]),
          ("TOPPADDING", (0, 0), (-1, -1), 4),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
      ])
  )
  story.append(t_itens)
  story.append(Spacer(1, 0.3 * cm))

  # Bloco Final de Preço
  fechamento_data = [[
      Paragraph(
          "<b>Condições:</b> 50% entrada + saldo em até 3x no cartão.<br/>À"
          " vista com 5% de desconto via Pix.<br/>Instalação em 10 a 15 dias"
          " úteis.",
          style_card,
      ),
      Paragraph(
          "<font size='8' color='#555555'>TOTAL DA PROPOSTA</font><br/><font"
          f" size='14' color='#0D3B66'><b>R$"
          f" {dados['preco_final']:.2f}</b></font>",
          style_meta,
      ),
  ]]
  t_fech = Table(fechamento_data, colWidths=[12.0 * cm, 6.0 * cm])
  t_fech.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, -1), CINZA_FUNDO),
          ("BOX", (0, 0), (-1, -1), 0.8, AZUL_PRIMARIO),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 6),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
      ])
  )
  story.append(t_fech)

  doc.build(story)
  pdf_value = buffer.getvalue()
  buffer.close()
  return pdf_value


# ==============================================================================
# 4. APLICAÇÃO PRINCIPAL STREAMLIT
# ==============================================================================
def main():
  st.set_page_config(
      page_title="Hopeness - Vidraçaria & Consultoria",
      page_icon="🪟",
      layout="wide",
  )
  st.title("🪟 Hopeness - Gestão & Consultoria de Vidros")
  st.caption("Plataforma de validação técnica ABNT e orçamentos comerciais")

  aba1, aba2 = st.tabs(
      ["📋 Consultoria Técnica (ABNT)", "💰 Calculadora & Orçamento"]
  )

  with aba1:
    st.header("Especificação Normativa (ABNT NBR 7199 / 14718 / 14207)")
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
      st.info(f"💡 **Diretriz de Segurança:** {rec['explicacao']}")

  with aba2:
    st.header("Gerador de Orçamento Comercial")
    col_cli1, col_cli2 = st.columns(2)
    cliente_nome = col_cli1.text_input("Nome do Cliente", "Mariana Albuquerque")
    cliente_local = col_cli2.text_input(
        "Local da Instalação", "Boa Viagem - Recife/PE"
    )

    c1, c2 = st.columns(2)
    with c1:
      st.subheader("1. Dimensões do Vão")
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
          "Custo do Vidro por m² (R$)", min_value=0.0, value=380.0, step=10.0
      )

    with c2:
      st.subheader("2. Ferragens, Insumos e Margem")
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
      m4.metric("Preço Final de Venda", f"R$ {res['preco_venda_final']:.2f}")

      st.success(
          f"**Lucro Bruto Estimado:** R$ {res['lucro_bruto']:.2f} (Margem:"
          f" {res['margem_aplicada_pct']}%)"
      )

      # Geração do PDF
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
          file_name=f"Orcamento_Hopeness_{cliente_nome.replace(' ', '_')}.pdf",
          mime="application/pdf",
      )


if __name__ == "__main__":
  main()

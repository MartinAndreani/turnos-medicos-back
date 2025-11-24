# app/reports/pacientes/utils/pdf_generator.py

from io import BytesIO
from typing import Optional

from fpdf import FPDF
import pandas as pd


class PDFGenerator:
    """
    Genera un PDF con los reportes de pacientes usando fpdf2.
    Recibe DataFrames y gráficos (BytesIO) y devuelve bytes del PDF.
    """

    def _add_title(self, pdf: FPDF, text: str):
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, text, ln=True, align="C")
        pdf.ln(5)

    def _add_subtitle(self, pdf: FPDF, text: str):
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, text, ln=True)
        pdf.ln(2)

    def _add_paragraph(self, pdf: FPDF, text: str):
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, text)
        pdf.ln(2)

    def _add_table_from_df(self, pdf: FPDF, df: pd.DataFrame, col_widths: Optional[list[float]] = None):
        if df.empty:
            pdf.set_font("Helvetica", "I", 10)
            pdf.cell(0, 6, "Sin datos para mostrar.", ln=True)
            pdf.ln(2)
            return

        pdf.set_font("Helvetica", "B", 9)

        columns = list(df.columns)
        n_cols = len(columns)

        if not col_widths:
            page_width = pdf.w - 2 * pdf.l_margin
            col_widths = [page_width / n_cols] * n_cols

        # Header
        for col, width in zip(columns, col_widths):
            pdf.cell(width, 6, str(col), border=1)
        pdf.ln()

        pdf.set_font("Helvetica", "", 9)
        # Rows
        for _, row in df.iterrows():
            for col, width in zip(columns, col_widths):
                value = str(row[col])
                pdf.cell(width, 6, value[:40], border=1)  # recorte simple
            pdf.ln()
        pdf.ln(3)

    def create_pacientes_report(
        self,
        df_nuevos: pd.DataFrame,
        df_ranking: pd.DataFrame,
        df_inactivos: pd.DataFrame,
        chart_nuevos,
        chart_ranking,
        chart_inactivos,
    ) -> bytes:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Portada / título principal
        self._add_title(pdf, "Reporte de Pacientes")

        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 6, "Resumen estadístico de pacientes del sistema de turnos médicos.", ln=True)
        pdf.ln(5)

        # =========================
        # Sección 1: Pacientes nuevos por mes
        # =========================
        self._add_subtitle(pdf, "1. Pacientes nuevos por mes")

        self._add_paragraph(
            pdf,
            "Este gráfico muestra la cantidad de pacientes nuevos registrados en el sistema "
            "agrupados por mes. Permite visualizar tendencias de crecimiento.",
        )

        if chart_nuevos:
            pdf.image(chart_nuevos, type="PNG", w=180)
            pdf.ln(5)

        self._add_table_from_df(pdf, df_nuevos)

        # =========================
        # Sección 2: Ranking de pacientes por consultas
        # =========================
        pdf.add_page()
        self._add_subtitle(pdf, "2. Ranking de pacientes con más consultas")

        self._add_paragraph(
            pdf,
            "Top de pacientes ordenados por la cantidad de turnos registrados en el sistema. "
            "Es útil para identificar pacientes crónicos o de alta recurrencia.",
        )

        if chart_ranking:
            pdf.image(chart_ranking, type="PNG", w=180)
            pdf.ln(5)

        self._add_table_from_df(pdf, df_ranking)

        # =========================
        # Sección 3: Pacientes inactivos
        # =========================
        pdf.add_page()
        self._add_subtitle(pdf, "3. Pacientes inactivos")

        self._add_paragraph(
            pdf,
            "Pacientes ordenados por la cantidad de días desde su última consulta. "
            "Puede ayudar a planificar campañas de recordatorio o seguimiento.",
        )

        if chart_inactivos:
            pdf.image(chart_inactivos, type="PNG", w=180)
            pdf.ln(5)

        self._add_table_from_df(pdf, df_inactivos)

        # Salida en bytes
        pdf_bytes = bytes(pdf.output(dest="S"))
        return pdf_bytes

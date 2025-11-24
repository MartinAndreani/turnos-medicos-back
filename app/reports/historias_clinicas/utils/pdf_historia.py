from fpdf import FPDF
import matplotlib.pyplot as plt
import io
import base64

class PDFHistoriaGenerator:

    @staticmethod
    def _imagen_a_bytes(fig):
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", dpi=150)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generar_pdf_diagnosticos(df):

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Reporte - Diagnósticos más frecuentes", ln=True)

        # gráfico
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(df["diagnostico"], df["cantidad"])
        ax.set_xlabel("Cantidad")
        ax.set_ylabel("Diagnóstico")
        ax.set_title("Top Diagnósticos")

        img_bytes = PDFHistoriaGenerator._imagen_a_bytes(fig)
        pdf.image(img_bytes, x=10, y=30, w=180)
        plt.close()

        pdf.ln(80)
        pdf.set_font("Arial", "", 12)

        for _, row in df.iterrows():
            pdf.cell(0, 8, f"{row['diagnostico']}: {row['cantidad']}", ln=True)

        return pdf.output(dest="S")

    @staticmethod
    def generar_pdf_tratamientos(df):

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Reporte - Tratamientos más frecuentes", ln=True)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(df["tratamiento"], df["cantidad"])
        ax.set_xlabel("Cantidad")
        ax.set_ylabel("Tratamiento")
        ax.set_title("Top Tratamientos")
        plt.xticks(rotation=45, ha="right")

        img_bytes = PDFHistoriaGenerator._imagen_a_bytes(fig)
        pdf.image(img_bytes, x=10, y=30, w=180)
        plt.close()

        pdf.ln(80)
        pdf.set_font("Arial", "", 12)

        for _, row in df.iterrows():
            pdf.cell(0, 8, f"{row['tratamiento']}: {row['cantidad']}", ln=True)

        return pdf.output(dest="S")
    

    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Reporte de Historia Clínica - Registros por Paciente", 0, 1, "C")
        self.ln(5)

    def generar_registros_por_paciente(self, registros):
        self.add_page()
        self.set_font("Arial", size=11)

        for r in registros:
            self.set_font("Arial", "B", 11)
            fecha = r.fecha_registro.strftime("%d/%m/%Y %H:%M")
            self.cell(0, 10, f"Registro — {fecha}", ln=1)

            self.set_font("Arial", size=10)
            self.multi_cell(0, 6, f"Médico: {r.medico.nombre}")
            self.multi_cell(0, 6, f"Diagnóstico: {r.diagnostico or '-'}")
            self.multi_cell(0, 6, f"Tratamiento: {r.tratamiento or '-'}")
            self.multi_cell(0, 6, f"Observaciones: {r.observaciones or '-'}")

            self.ln(4)
            self.cell(0, 0, "-" * 80, ln=1)
            self.ln(4)

        return self.output(dest="S").encode("latin1")

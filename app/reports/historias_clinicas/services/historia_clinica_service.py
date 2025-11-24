import pandas as pd
from app.reports.historias_clinicas.repositories.historia_clinica_repository import HistoriaClinicaReportsRepository
from app.reports.historias_clinicas.utils.pdf_historia import PDFHistoriaGenerator

class HistoriaClinicaReportsService:

    def __init__(self, db):
        self.repo = HistoriaClinicaReportsRepository(db)

    def generar_reporte_diagnosticos(self):
        data = self.repo.obtener_diagnosticos_frecuentes()

        df = pd.DataFrame(data, columns=["diagnostico", "cantidad"])

        pdf_bytes = PDFHistoriaGenerator.generar_pdf_diagnosticos(df)

        return pdf_bytes

    def generar_reporte_tratamientos(self):
        data = self.repo.obtener_tratamientos_frecuentes()

        df = pd.DataFrame(data, columns=["tratamiento", "cantidad"])

        pdf_bytes = PDFHistoriaGenerator.generar_pdf_tratamientos(df)

        return pdf_bytes
    

    def generar_reporte_registros_por_paciente(self, id_paciente: str):
        registros = self.repo.obtener_registros_por_paciente(id_paciente)
        pdf = PDFHistoriaGenerator()

        return pdf.generar_registros_por_paciente(registros)

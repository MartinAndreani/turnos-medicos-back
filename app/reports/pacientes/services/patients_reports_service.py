# app/reports/pacientes/services/patients_reports_service.py

from datetime import datetime
from sqlalchemy.orm import Session
import pandas as pd

from app.reports.pacientes.repositories.patients_reports_repository import (
    PatientsReportsRepository,
)
from app.reports.pacientes.utils.charts import ChartsGenerator
from app.reports.pacientes.utils.pdf_generator import PDFGenerator


class PatientsReportsService:
    """
    Orquesta:
    - Consulta de datos (repository)
    - Transformación a DataFrame
    - Generación de gráficos
    - Armado del PDF final
    """

    def __init__(
        self,
        repo: PatientsReportsRepository | None = None,
        charts: ChartsGenerator | None = None,
        pdf_generator: PDFGenerator | None = None,
    ):
        self.repo = repo or PatientsReportsRepository()
        self.charts = charts or ChartsGenerator()
        self.pdf = pdf_generator or PDFGenerator()

    # --------------------------
    #   Helpers internos
    # --------------------------
    def _build_df_nuevos_por_mes(self, db: Session) -> pd.DataFrame:
        rows = self.repo.pacientes_nuevos_por_mes(db)
        data = []
        for r in rows:
            # r.mes es un datetime truncado al primer día del mes
            mes_label = r.mes.strftime("%Y-%m") if isinstance(r.mes, datetime) else str(r.mes)
            data.append({"mes": mes_label, "cantidad": int(r.cantidad)})
        return pd.DataFrame(data, columns=["mes", "cantidad"])

    def _build_df_ranking(self, db: Session) -> pd.DataFrame:
        rows = self.repo.ranking_pacientes_por_consultas(db)
        data = []
        for r in rows:
            nombre = f"{r.nombre} {r.apellido}"
            data.append({"paciente": nombre, "consultas": int(r.consultas)})
        return pd.DataFrame(data, columns=["paciente", "consultas"])

    def _build_df_inactivos(self, db: Session) -> pd.DataFrame:
        rows = self.repo.pacientes_inactivos(db)
        data = []
        now = datetime.utcnow()
        for r in rows:
            nombre = f"{r.nombre} {r.apellido}"
            if isinstance(r.ultima_consulta, datetime):
                dias = (now - r.ultima_consulta).days
                fecha_label = r.ultima_consulta.strftime("%Y-%m-%d")
            else:
                dias = None
                fecha_label = str(r.ultima_consulta)
            data.append(
                {
                    "paciente": nombre,
                    "ultima_consulta": fecha_label,
                    "dias_desde_ultima_consulta": dias,
                }
            )
        return pd.DataFrame(data, columns=["paciente", "ultima_consulta", "dias_desde_ultima_consulta"])

    # --------------------------
    #   API principal
    # --------------------------
    def generar_pdf_reportes(self, db: Session) -> bytes:
        """
        Punto de entrada desde el router.
        Devuelve los bytes de un PDF con:
        - Pacientes nuevos por mes
        - Ranking por consultas
        - Pacientes inactivos
        """
        df_nuevos = self._build_df_nuevos_por_mes(db)
        df_ranking = self._build_df_ranking(db)
        df_inactivos = self._build_df_inactivos(db)

        chart_nuevos = self.charts.grafico_pacientes_nuevos_por_mes(df_nuevos)
        chart_ranking = self.charts.grafico_ranking_pacientes(df_ranking)
        chart_inactivos = self.charts.grafico_pacientes_inactivos(df_inactivos)

        pdf_bytes = self.pdf.create_pacientes_report(
            df_nuevos=df_nuevos,
            df_ranking=df_ranking,
            df_inactivos=df_inactivos,
            chart_nuevos=chart_nuevos,
            chart_ranking=chart_ranking,
            chart_inactivos=chart_inactivos,
        )
        return pdf_bytes

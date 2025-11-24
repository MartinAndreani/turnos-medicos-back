# app/reports/pacientes/repositories/patients_reports_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.db.models.pacientes import PacienteModel
from app.db.models.turnos import TurnoModel


class PatientsReportsRepository:
    """
    Consultas de reporting relacionadas con Pacientes.
    No devuelve DataFrames ni PDFs, solo datos crudos desde la DB.
    """

    def pacientes_nuevos_por_mes(self, db: Session):
        """
        Devuelve una lista de filas:
        - mes (datetime truncado al mes)
        - cantidad (int)
        Solo pacientes activos.
        """
        rows = (
            db.query(
                func.date_trunc("month", PacienteModel.created_at).label("mes"),
                func.count(PacienteModel.id_paciente).label("cantidad"),
            )
            .filter(PacienteModel.activo == True)  # noqa: E712
            .group_by("mes")
            .order_by("mes")
            .all()
        )
        return rows

    def ranking_pacientes_por_consultas(self, db: Session, limit: int = 10):
        """
        Devuelve el top N pacientes con más turnos registrados.
        Columnas:
        - id_paciente
        - nombre
        - apellido
        - consultas (count)
        """
        rows = (
            db.query(
                PacienteModel.id_paciente,
                PacienteModel.nombre,
                PacienteModel.apellido,
                func.count(TurnoModel.id_turno).label("consultas"),
            )
            .join(
                TurnoModel,
                TurnoModel.id_paciente == PacienteModel.id_paciente,
            )
            .group_by(
                PacienteModel.id_paciente,
                PacienteModel.nombre,
                PacienteModel.apellido,
            )
            .order_by(desc("consultas"))
            .limit(limit)
            .all()
        )
        return rows

    def pacientes_inactivos(self, db: Session, limit: int = 20):
        """
        Pacientes ordenados por fecha de última consulta ascendente
        (los que hace más tiempo que no vienen primero).

        Devuelve filas con:
        - id_paciente
        - nombre
        - apellido
        - ultima_consulta (datetime)
        """
        sub = (
            db.query(
                TurnoModel.id_paciente.label("id_paciente"),
                func.max(TurnoModel.fecha_hora_inicio).label("ultima_consulta"),
            )
            .group_by(TurnoModel.id_paciente)
            .subquery()
        )

        rows = (
            db.query(
                PacienteModel.id_paciente,
                PacienteModel.nombre,
                PacienteModel.apellido,
                sub.c.ultima_consulta,
            )
            .join(sub, sub.c.id_paciente == PacienteModel.id_paciente)
            .order_by(sub.c.ultima_consulta.asc())
            .limit(limit)
            .all()
        )
        return rows

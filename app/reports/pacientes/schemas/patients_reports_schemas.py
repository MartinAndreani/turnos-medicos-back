# app/reports/pacientes/schemas/patients_reports_schemas.py

from pydantic import BaseModel


class PacientesNuevosMesOut(BaseModel):
    mes: str
    cantidad: int


class RankingPacientesOut(BaseModel):
    paciente: str
    consultas: int


class PacientesInactivosOut(BaseModel):
    paciente: str
    ultima_consulta: str

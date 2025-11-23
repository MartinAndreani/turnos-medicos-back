from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ============================
#   TURNO CREATE
# ============================
class TurnoCreate(BaseModel):
    id_paciente: str
    id_medico: str
    id_consultorio: str

    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime

    motivo_consulta: Optional[str] = None


# ============================
#   TURNO UPDATE
# ============================
class TurnoUpdate(BaseModel):
    id_paciente: Optional[str] = None
    id_medico: Optional[str] = None
    id_consultorio: Optional[str] = None

    fecha_hora_inicio: Optional[datetime] = None
    fecha_hora_fin: Optional[datetime] = None

    motivo_consulta: Optional[str] = None
    id_estado: Optional[str] = None


# ============================
#   TURNO OUT
# ============================
class TurnoOut(BaseModel):
    id: UUID = Field(..., alias="id_turno")

    id_paciente: str
    id_medico: str
    id_consultorio: str

    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime

    id_estado: str
    motivo_consulta: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

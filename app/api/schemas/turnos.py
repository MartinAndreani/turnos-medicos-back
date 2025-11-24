# app/api/schemas/turnos.py

from uuid import UUID  # <--- Importante
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


# ============================
#   TURNO CREATE
# ============================
class TurnoCreate(BaseModel):
    id_paciente: UUID
    id_medico: UUID
    id_consultorio: UUID  # Asegúrate de validar que coincida con la asignación del médico

    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime

    motivo_consulta: Optional[str] = None


# ============================
#   TURNO UPDATE
# ============================
class TurnoUpdate(BaseModel):
    id_paciente: Optional[UUID] = None
    id_medico: Optional[UUID] = None
    id_consultorio: Optional[UUID] = None

    fecha_hora_inicio: Optional[datetime] = None
    fecha_hora_fin: Optional[datetime] = None

    motivo_consulta: Optional[str] = None
    # Asumo que id_estado también es un UUID. Si es int (ej: 1, 2), cámbialo a int.
    id_estado: Optional[UUID] = None 


# ============================
#   TURNO OUT
# ============================
class TurnoOut(BaseModel):
    # Mapeamos 'id_turno' (DB) a 'id' (JSON)
    id: UUID = Field(..., alias="id_turno")
    
    id_paciente: UUID
    id_medico: UUID
    id_consultorio: UUID

    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime

    id_estado: UUID  # O int, depende de tu tabla 'estados_turnos'
    motivo_consulta: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )
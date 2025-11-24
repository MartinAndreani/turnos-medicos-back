# app/api/schemas/historias_clinicas.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class HistoriaClinicaCreate(BaseModel):
    id_paciente: UUID
    id_medico: UUID
    id_turno: Optional[UUID] = None
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None


class HistoriaClinicaUpdate(BaseModel):
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None
    activo: Optional[bool] = None  # baja lógica / reactivación


class HistoriaClinicaOut(BaseModel):
    id: UUID = Field(..., alias="id_historia_clinica")
    id_paciente: UUID
    id_medico: UUID
    id_turno: Optional[UUID]
    fecha_registro: datetime
    diagnostico: Optional[str]
    tratamiento: Optional[str]
    observaciones: Optional[str]
    activo: bool

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )

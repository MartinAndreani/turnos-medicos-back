# app/api/schemas/historias_clinicas.py

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class HistoriaClinicaCreate(BaseModel):
    id_paciente: str
    id_medico: str
    id_turno: Optional[str] = None
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None


class HistoriaClinicaUpdate(BaseModel):
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None
    activo: Optional[bool] = None  # baja lógica / reactivación


class HistoriaClinicaOut(BaseModel):
    id: str
    id_paciente: str
    id_medico: str
    id_turno: Optional[str]
    fecha_registro: datetime
    diagnostico: Optional[str]
    tratamiento: Optional[str]
    observaciones: Optional[str]
    activo: bool

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )

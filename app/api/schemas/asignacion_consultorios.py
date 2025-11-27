from uuid import UUID
from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.domain.entities.enum import JornadaEnum

# CREATE
class AsignacionConsultorioCreateDTO(BaseModel):
    id_medico: UUID
    id_consultorio: UUID
    fecha_inicio: date
    fecha_fin: date
    
    dias_semana: List[int] # <--- CAMBIO: Lista
    
    hora_inicio: time
    hora_fin: time
    jornada: JornadaEnum

# UPDATE
class AsignacionConsultorioUpdateDTO(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    
    dias_semana: Optional[List[int]] = None # <--- CAMBIO
    
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    jornada: Optional[JornadaEnum] = None
    activo: Optional[bool] = None

# OUT
class AsignacionConsultorioResponseDTO(BaseModel):
    id: UUID = Field(..., alias="id_asignacion")
    id_medico: UUID
    id_consultorio: UUID
    fecha_inicio: date
    fecha_fin: date
    
    dias_semana: List[int] # <--- CAMBIO
    
    hora_inicio: time
    hora_fin: time
    jornada: JornadaEnum
    activo: bool

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
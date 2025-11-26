from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from datetime import time, date
from typing import List, Optional

# CREATE (Ya estaba bien, lo dejo por referencia)
class AgendaMedicoCreate(BaseModel):
    id_medico: UUID
    id_consultorio: UUID
    fecha_inicio: date
    fecha_fin: date
    dias_semana: List[int] # [0, 2, 4]
    hora_inicio: time
    hora_fin: time
    duracion_turno: int
    jornada: str

# UPDATE (Cambiamos a lista opcional)
class AgendaMedicoUpdate(BaseModel):
    dias_semana: Optional[List[int]] = None # <--- CAMBIO
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    duracion_turno: Optional[int] = None
    jornada: Optional[str] = None
    activo: Optional[bool] = None

# OUT (Cambiamos a lista obligatoria)
class AgendaMedicoOut(BaseModel):
    id: UUID = Field(..., alias="id_agenda") 
    id_medico: UUID
    fecha_inicio: date
    fecha_fin: date
    dias_semana: List[int] # <--- CAMBIO: Ahora devuelve la lista [0, 2, 4]
    hora_inicio: time
    hora_fin: time
    duracion_turno: int
    jornada: str
    activo: bool
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    
    

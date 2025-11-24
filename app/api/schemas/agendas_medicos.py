
from pydantic import BaseModel, ConfigDict, Field
from datetime import time
from typing import Optional


class AgendaMedicoCreate(BaseModel):
    id_medico: str
    dia_semana: int
    hora_inicio: time
    hora_fin: time
    duracion_turno: int
    jornada: str


class AgendaMedicoUpdate(BaseModel):
    dia_semana: Optional[int] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    duracion_turno: Optional[int] = None
    jornada: Optional[str] = None
    activo: Optional[bool] = None


class AgendaMedicoOut(BaseModel):
    id: str
    id_medico: str
    dia_semana: int
    hora_inicio: time
    hora_fin: time
    duracion_turno: int
    jornada: str
    activo: bool

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )
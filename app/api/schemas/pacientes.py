

from uuid import UUID
from pydantic import BaseModel,Field
from typing import Optional
from datetime import date

class PacienteCreate(BaseModel):
    dni: str
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    
    
    
class PacienteUpdate(BaseModel):
    nombre: Optional[str]
    apellido: Optional[str]
    fecha_nacimiento: Optional[date]
    direccion: Optional[str]
    telefono: Optional[str]
    activo: Optional[bool]

class PacienteOut(BaseModel):
    id: UUID = Field(..., alias="id_paciente")
    dni: str
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[date]
    direccion: Optional[str]
    telefono: Optional[str]
    activo: bool

class Config:
    orm_mode = True
    allow_population_by_field_name = True
# app/api/schemas/pacientes.py

from uuid import UUID  # <--- 1. Importamos UUID
from pydantic import BaseModel, ConfigDict, Field
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
    # 2. Agregamos "= None" para que no sea obligatorio enviarlos en el JSON
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None


class PacienteOut(BaseModel):
    # 3. Mapeamos 'id_paciente' a 'id'
    id: UUID = Field(..., alias="id_paciente")
    
    dni: str
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[date]
    direccion: Optional[str]
    telefono: Optional[str]
    activo: bool

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True
    )
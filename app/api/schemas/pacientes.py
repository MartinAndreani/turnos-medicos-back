


from pydantic import BaseModel, ConfigDict,Field
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
    id: str
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
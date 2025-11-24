
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date


class RecetaCreate(BaseModel):
    id_turno: str
    medicamentos: Optional[str] = None
    descripcion: Optional[str] = None


class RecetaUpdate(BaseModel):
    medicamentos: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class RecetaOut(BaseModel):
    id: str 
    id_turno: str
    fecha_emision: date
    medicamentos: Optional[str]
    descripcion: Optional[str]
    activo: bool

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )

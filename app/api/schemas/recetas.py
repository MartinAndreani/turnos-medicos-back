# app/api/schemas/recetas.py

from uuid import UUID  # <--- Importante
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date


class RecetaCreate(BaseModel):
    id_turno: UUID  # <--- Usamos UUID para validar que el turno sea válido
    medicamentos: Optional[str] = None
    descripcion: Optional[str] = None


class RecetaUpdate(BaseModel):
    medicamentos: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class RecetaOut(BaseModel):
    # Asumo que la PK en la base de datos es 'id_receta'
    id: UUID = Field(..., alias="id_receta") 
    
    id_turno: UUID
    fecha_emision: date
    medicamentos: Optional[str]
    descripcion: Optional[str]
    activo: bool

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )
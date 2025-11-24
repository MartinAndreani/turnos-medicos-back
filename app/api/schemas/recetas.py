# app/api/schemas/recetas.py

from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class RecetaCreate(BaseModel):
    id_turno: UUID
    medicamentos: Optional[str] = None
    descripcion: Optional[str] = None


class RecetaUpdate(BaseModel):
    medicamentos: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class RecetaOut(BaseModel):
    id: UUID = Field(..., alias="id_receta")
    id_turno: UUID
    fecha_emision: date
    medicamentos: Optional[str]
    descripcion: Optional[str]
    activo: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

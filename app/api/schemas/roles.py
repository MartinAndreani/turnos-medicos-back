# app/api/schemas/roles.py

from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class RolCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class RolOut(BaseModel):
    id: UUID = Field(..., alias="id_rol")
    nombre: str
    descripcion: Optional[str]
    activo: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

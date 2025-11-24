from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class EspecialidadCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class EspecialidadUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class EspecialidadOut(BaseModel):
    id: UUID = Field(..., alias="id_especialidad")
    nombre: str
    descripcion: Optional[str]
    activo: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

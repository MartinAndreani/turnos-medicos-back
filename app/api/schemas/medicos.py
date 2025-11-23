from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


# ============================
#   MÉDICO CREATE
# ============================
class MedicoCreate(BaseModel):
    matricula: str
    dni: str
    nombre: str
    apellido: str
    telefono: Optional[str] = None


# ============================
#   MÉDICO UPDATE
# ============================
class MedicoUpdate(BaseModel):
    matricula: Optional[str] = None
    dni: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None


# ============================
#   MÉDICO OUT
# ============================
class MedicoOut(BaseModel):
    id: UUID = Field(..., alias="id_medico")
    matricula: str
    dni: str
    nombre: str
    apellido: str
    telefono: Optional[str]
    activo: bool


    class Config:
        orm_mode = True
        allow_population_by_field_name = True

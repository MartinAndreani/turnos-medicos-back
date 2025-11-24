
from pydantic import BaseModel, ConfigDict, Field
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
    id: str
    matricula: str
    dni: str
    nombre: str
    apellido: str
    telefono: Optional[str]
    activo: bool


    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )

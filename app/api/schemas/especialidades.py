# app/api/schemas/especialidad.py

from uuid import UUID  # <--- Importante para validación
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# ============================
#   CREATE
# ============================
class EspecialidadCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


# ============================
#   UPDATE
# ============================
class EspecialidadUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


# ============================
#   OUT
# ============================
class EspecialidadOut(BaseModel):
    # Estandarizamos: 'id' en el JSON viene de 'id_especialidad' en la DB
    id: UUID = Field(..., alias="id_especialidad") 
    
    nombre: str
    descripcion: Optional[str]
    activo: bool
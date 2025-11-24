# app/api/schemas/roles.py

from uuid import UUID  # <--- Importante
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


# ============================
#   CREATE
# ============================
class RolCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


# ============================
#   UPDATE
# ============================
class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


# ============================
#   OUT
# ============================
class RolOut(BaseModel):
    # Mapeamos 'id_rol' (DB) a 'id' (JSON)
    id: UUID = Field(..., alias="id_rol") 
    
    nombre: str
    descripcion: Optional[str]
    activo: bool

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )
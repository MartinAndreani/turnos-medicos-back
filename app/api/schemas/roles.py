# app/api/schemas/roles.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
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

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
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

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )

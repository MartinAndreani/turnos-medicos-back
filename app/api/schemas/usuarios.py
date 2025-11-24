# app/api/schemas/usuarios.py

from uuid import UUID
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str
    # opción B: lista de IDs de rol
    roles_ids: Optional[List[UUID]] = None


class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    activo: Optional[bool] = None
    # si se envía, reemplaza completamente las asignaciones de roles
    roles_ids: Optional[List[UUID]] = None


class UsuarioOut(BaseModel):
    id: UUID = Field(..., alias="id_usuario")
    email: EmailStr
    activo: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

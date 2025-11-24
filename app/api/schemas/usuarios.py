from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, List


class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str
    # opción B: lista de IDs de rol
    roles_ids: Optional[List[str]] = None


class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    activo: Optional[bool] = None
    # si se envía, reemplaza completamente las asignaciones de roles
    roles_ids: Optional[List[str]] = None


class UsuarioOut(BaseModel):
    id: str 
    email: EmailStr
    activo: bool

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )

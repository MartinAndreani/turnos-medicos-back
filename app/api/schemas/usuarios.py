# app/api/schemas/usuarios.py

from uuid import UUID  # <--- Importante
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, List


# ============================
#   USUARIO CREATE
# ============================
class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str
    # Validamos que sea una lista de UUIDs válidos
    roles_ids: Optional[List[UUID]] = None


# ============================
#   USUARIO UPDATE
# ============================
class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    activo: Optional[bool] = None
    # Si se envía, reemplaza completamente las asignaciones de roles
    roles_ids: Optional[List[UUID]] = None


# ============================
#   USUARIO OUT
# ============================
class UsuarioOut(BaseModel):
    # Mapeamos 'id_usuario' (DB) a 'id' (JSON)
    id: UUID = Field(..., alias="id_usuario") 
    
    email: EmailStr
    activo: bool

    # Tip: A veces es útil devolver los roles aquí también, 
    # pero depende de si tu repositorio hace el join.
    # roles: List[RolOut] = [] 

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )
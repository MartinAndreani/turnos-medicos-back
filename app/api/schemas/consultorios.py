# app/api/schemas/consultorios.py

from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# ============================
#   CREATE
# ============================
class ConsultorioCreate(BaseModel):
    numero_consultorio: int
    piso: int


# ============================
#   UPDATE (Agregado por si lo necesitas)
# ============================
class ConsultorioUpdate(BaseModel):
    numero_consultorio: Optional[int] = None
    piso: Optional[int] = None
    activo: Optional[bool] = None


# ============================
#   OUT
# ============================
class ConsultorioOut(BaseModel):
    # Estandarizamos la salida: 'id' en el JSON viene de 'id_consultorio'
    id: UUID = Field(..., alias="id_consultorio") 
    
    numero_consultorio: int
    piso: int
    activo: bool

    model_config = ConfigDict(
        from_attributes=True,        
        populate_by_name=True       
    )
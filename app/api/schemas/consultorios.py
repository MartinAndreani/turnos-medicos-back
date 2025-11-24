



from pydantic import BaseModel, Field
from sqlalchemy import UUID


class ConsultorioCreate(BaseModel):
    numero_consultorio: int
    piso: int
    
class ConsultorioOut(BaseModel):
    id_consultorio: UUID = Field(...,alias="id_consultorio")
    numero_consultorio: int
    piso: int
    activo: bool

class Config:
    orm_mode = True
    allow_population_by_field_name = True

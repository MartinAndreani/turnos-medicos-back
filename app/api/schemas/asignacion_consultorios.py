from datetime import date
from pydantic import BaseModel, Field


class AsignacionConsultorioCreateDTO(BaseModel):
    id_medico: str
    id_consultorio: str
    fecha_inicio: date
    fecha_fin: date
    jornada: str = Field(..., pattern="^(mañana|tarde|noche)$")


class AsignacionConsultorioUpdateDTO(BaseModel):
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    jornada: str | None = Field(None, pattern="^(mañana|tarde|noche)$")
    activo: bool | None = None


class AsignacionConsultorioResponseDTO(BaseModel):
    id_asignacion: str
    id_medico: str
    id_consultorio: str
    fecha_inicio: date
    fecha_fin: date
    jornada: str
    activo: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

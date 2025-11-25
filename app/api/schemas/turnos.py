from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

# --- CREATE ---
class TurnoCreate(BaseModel):
    id_paciente: UUID
    id_medico: UUID
    # NO pedimos id_consultorio, lo calculamos nosotros
    
    fecha_hora_inicio: datetime
    # La fecha fin se puede calcular con la duración de la agenda, 
    # pero para simplificar pedimos inicio y fin o duración.
    # Asumiremos que el frontend manda el bloque completo o el backend lo calcula.
    # Por ahora pedimos ambas para validar.
    fecha_hora_fin: datetime 
    
    motivo_consulta: Optional[str] = None

# --- UPDATE STATE ---
class TurnoUpdateEstado(BaseModel):
    id_nuevo_estado: UUID
    motivo_cambio: str # Obligatorio para el historial
    actor: str # Quién hizo el cambio (ej: "Sistema", "Juan Perez")

# --- OUT ---
class TurnoOut(BaseModel):
    id: UUID = Field(..., alias="id_turno")
    id_paciente: UUID
    id_medico: UUID
    id_consultorio: UUID
    id_estado_turno: UUID
    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime
    motivo_consulta: Optional[str]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
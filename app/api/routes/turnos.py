from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.api.schemas.turnos import TurnoCreate, TurnoOut, TurnoUpdateEstado
from app.domain.services.turno_service import TurnoService

# Repos
from app.db.repositories.turno_repository import TurnoRepository
from app.db.repositories.agenda_medico_repository import AgendaMedicoRepository
from app.db.repositories.asignacion_consultorio_repository import AsignacionConsultorioRepository
from app.db.repositories.medico_repository import MedicoRepository

router = APIRouter(prefix="/turnos", tags=["Turnos"])

def get_service(db: Session = Depends(get_db)):
    return TurnoService(
        TurnoRepository(db),
        AgendaMedicoRepository(db),
        AsignacionConsultorioRepository(db),
        MedicoRepository(db)
    )

@router.get("/", response_model=List[TurnoOut])
def listar_turnos(
    id_medico: Optional[UUID] = Query(None, description="Filtrar por médico"),
    id_paciente: Optional[UUID] = Query(None, description="Filtrar por paciente"),
    fecha_desde: Optional[datetime] = Query(None, description="Fecha inicio del rango"),
    fecha_hasta: Optional[datetime] = Query(None, description="Fecha fin del rango"),
    service: TurnoService = Depends(get_service)
):
    """
    Obtiene una lista de turnos. 
    Se pueden aplicar filtros opcionales.
    """
    # Convertimos UUIDs a string para el servicio si es necesario, 
    # aunque SQLAlchemy suele manejar UUIDs objetos bien.
    return service.get_all(
        id_medico=str(id_medico) if id_medico else None,
        id_paciente=str(id_paciente) if id_paciente else None,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )

@router.get("/{id_turno}", response_model=TurnoOut)
def obtener_turno(
    id_turno: UUID,
    service: TurnoService = Depends(get_service)
):
    try:
        return service.get_by_id(str(id_turno))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.post("/", response_model=TurnoOut, status_code=status.HTTP_201_CREATED)
def crear_turno(dto: TurnoCreate, service: TurnoService = Depends(get_service)):
    try:
        return service.create(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{id_turno}/estado", response_model=TurnoOut)
def cambiar_estado(id_turno: UUID, dto: TurnoUpdateEstado, service: TurnoService = Depends(get_service)):
    try:
        return service.change_state(str(id_turno), dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
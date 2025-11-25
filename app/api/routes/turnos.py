from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
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
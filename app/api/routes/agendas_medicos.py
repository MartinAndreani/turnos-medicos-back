from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.api.schemas.agendas_medicos import AgendaMedicoCreate, AgendaMedicoUpdate, AgendaMedicoOut
from app.domain.services.agenda_medico_service import AgendaMedicoService

from app.db.repositories.agenda_medico_repository import AgendaMedicoRepository
from app.db.repositories.asignacion_consultorio_repository import AsignacionConsultorioRepository
from app.db.repositories.medico_repository import MedicoRepository

router = APIRouter(prefix="/agendas-medicos", tags=["Agendas Médicos"])

def get_service(db: Session = Depends(get_db)):
    return AgendaMedicoService(
        AgendaMedicoRepository(db),
        AsignacionConsultorioRepository(db),
        MedicoRepository(db)
    )

# response_model es AgendaMedicoOut (singular), no List[...]
@router.post("/", response_model=AgendaMedicoOut, status_code=201)
def create_agenda_masiva(
    dto: AgendaMedicoCreate, 
    service: AgendaMedicoService = Depends(get_service)
):
    try:
        # El servicio devuelve un objeto AgendaMedico único
        return service.create_masivo(dto)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@router.put("/{id_agenda}", response_model=AgendaMedicoOut)
def update_agenda(
    id_agenda: UUID, 
    dto: AgendaMedicoUpdate, 
    service: AgendaMedicoService = Depends(get_service)
):
    updated = service.update(str(id_agenda), dto)
    if not updated:
        raise HTTPException(status_code=404, detail="Agenda no encontrada")
    return updated

@router.delete("/{id_agenda}", status_code=204)
def delete_agenda(
    id_agenda: UUID, 
    service: AgendaMedicoService = Depends(get_service)
):
    if not service.delete(str(id_agenda)):
        raise HTTPException(status_code=404, detail="Agenda no encontrada")
    return
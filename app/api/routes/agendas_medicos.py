from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.agendas_medicos import AgendaMedicoCreate, AgendaMedicoUpdate, AgendaMedicoOut
from app.db.database import get_db
from app.db.repositories.agenda_medico_repository import AgendaMedicoRepository
from app.db.repositories.medico_repository import MedicoRepository
from app.domain.services.agenda_medico_service import AgendaMedicoService

router = APIRouter(prefix="/agendas-medicos", tags=["agenda_medico"])

def get_service(db: Session = Depends(get_db)):
    agenda_repo = AgendaMedicoRepository(db)
    medico_repo = MedicoRepository(db)
    return AgendaMedicoService(agenda_repo, medico_repo)



@router.post("/", response_model=AgendaMedicoOut, status_code=status.HTTP_201_CREATED)
def create_agenda(dto: AgendaMedicoCreate, service: AgendaMedicoService = Depends(get_service)):
    try:
        return service.create(dto)
    except ValueError as ex:
        
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(ex))


@router.put("/{id_agenda}", response_model=AgendaMedicoOut)
def update_agenda(id_agenda: UUID, dto: AgendaMedicoUpdate, service: AgendaMedicoService = Depends(get_service)):
    try:
        return service.update(id_agenda, dto)
    except ValueError as ex:
        msg = str(ex)
        if "no encontrada" in msg:
            raise HTTPException(status.HTTP_404_NOT_FOUND, msg)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, msg)


@router.delete("/{id_agenda}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agenda(id_agenda: UUID, service: AgendaMedicoService = Depends(get_service)):
    ok = service.delete(id_agenda)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Agenda no encontrada")
    return
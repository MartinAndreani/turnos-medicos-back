from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db
from app.domain.services.asignacion_consultorio_service import AsignacionConsultorioService
from app.db.repositories.asignacion_consultorio_repository import AsignacionConsultorioRepository
from app.db.repositories.medico_repository import MedicoRepository
from app.db.repositories.consultorio_repository import ConsultorioRepository
from app.api.schemas.asignacion_consultorios import *

router = APIRouter(prefix="/asignaciones-consultorio", tags=["Asignación de Consultorios"])


def get_service(db: Session = Depends(get_db)):
    repo = AsignacionConsultorioRepository(db)
    repo_medico = MedicoRepository(db)
    repo_consultorio = ConsultorioRepository(db)
    return AsignacionConsultorioService(repo, repo_medico, repo_consultorio)


@router.post("/", response_model=AsignacionConsultorioResponseDTO)
def create_asignacion(dto: AsignacionConsultorioCreateDTO, svc: AsignacionConsultorioService = Depends(get_service)):
    try:
        return svc.create(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id_asignacion}", response_model=AsignacionConsultorioResponseDTO)
def get_asignacion(id_asignacion: UUID, svc: AsignacionConsultorioService = Depends(get_service)):
    asignacion = svc.get(id_asignacion)
    if not asignacion:
        raise HTTPException(status_code=404, detail="No existe asignación")
    return asignacion


@router.get("/", response_model=list[AsignacionConsultorioResponseDTO])
def list_asignaciones(skip: int = 0, limit: int = 100, svc: AsignacionConsultorioService = Depends(get_service)):
    return svc.list(skip=skip, limit=limit)


@router.put("/{id_asignacion}", response_model=AsignacionConsultorioResponseDTO)
def update_asignacion(id_asignacion: UUID, dto: AsignacionConsultorioUpdateDTO, svc: AsignacionConsultorioService = Depends(get_service)):
    try:
        return svc.update(id_asignacion, dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id_asignacion}")
def delete_asignacion(id_asignacion: UUID, svc: AsignacionConsultorioService = Depends(get_service)):
    ok = svc.delete(id_asignacion)
    if not ok:
        raise HTTPException(status_code=404, detail="No existe asignación")
    return {"deleted": True}

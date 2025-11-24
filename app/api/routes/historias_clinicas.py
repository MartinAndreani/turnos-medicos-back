# app/api/routes/historias_clinicas.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.historias_clinicas import (
    HistoriaClinicaCreate,
    HistoriaClinicaUpdate,
    HistoriaClinicaOut,
)
from app.db.database import get_db
from app.db.repositories.historia_clinica_repository import HistoriaClinicaRepository
from app.db.repositories.paciente_repository import PacienteRepository
from app.db.repositories.medico_repository import MedicoRepository
from app.db.repositories.turno_repository import TurnoRepository
from app.domain.services.historia_clinica_service import HistoriaClinicaService

router = APIRouter(
    prefix="/historias-clinicas",
    tags=["historias_clinicas"],
)


def get_service(db: Session = Depends(get_db)) -> HistoriaClinicaService:
    hc_repo = HistoriaClinicaRepository(db)
    paciente_repo = PacienteRepository(db)
    medico_repo = MedicoRepository(db)
    turno_repo = TurnoRepository(db)
    return HistoriaClinicaService(hc_repo, paciente_repo, medico_repo, turno_repo)


# -------- LISTAR TODAS (activos) --------
@router.get("/", response_model=list[HistoriaClinicaOut])
def list_historias_clinicas(
    skip: int = 0,
    limit: int = 100,
    service: HistoriaClinicaService = Depends(get_service),
):
    return service.list(skip=skip, limit=limit)


# -------- LISTAR POR PACIENTE --------
@router.get("/paciente/{id_paciente}", response_model=list[HistoriaClinicaOut])
def list_historias_por_paciente(
    id_paciente: str,
    skip: int = 0,
    limit: int = 100,
    service: HistoriaClinicaService = Depends(get_service),
):
    return service.list_by_paciente(id_paciente, skip=skip, limit=limit)


# -------- OBTENER UNA --------
@router.get("/{id_historia_clinica}", response_model=HistoriaClinicaOut)
def get_historia_clinica(
    id_historia_clinica: str,
    service: HistoriaClinicaService = Depends(get_service),
):
    hc = service.get(id_historia_clinica)
    if not hc:
        raise HTTPException(404, "Historia clínica no encontrada")
    return hc


# -------- CREAR --------
@router.post("/", response_model=HistoriaClinicaOut, status_code=status.HTTP_201_CREATED)
def create_historia_clinica(
    payload: HistoriaClinicaCreate,
    service: HistoriaClinicaService = Depends(get_service),
):
    try:
        return service.create(payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


# -------- ACTUALIZAR --------
@router.put("/{id_historia_clinica}", response_model=HistoriaClinicaOut)
def update_historia_clinica(
    id_historia_clinica: str,
    dto: HistoriaClinicaUpdate,
    service: HistoriaClinicaService = Depends(get_service),
):
    try:
        return service.update(id_historia_clinica, dto)
    except ValueError as ex:
        msg = str(ex)
        if "no encontrada" in msg:
            raise HTTPException(404, detail=msg)
        raise HTTPException(400, detail=msg)


# -------- BAJA LÓGICA --------
@router.delete("/{id_historia_clinica}", status_code=status.HTTP_204_NO_CONTENT)
def delete_historia_clinica(
    id_historia_clinica: str,
    service: HistoriaClinicaService = Depends(get_service),
):
    ok = service.delete(id_historia_clinica)
    if not ok:
        raise HTTPException(404, "Historia clínica no encontrada")
    return

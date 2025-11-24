from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.especialidades import (
    EspecialidadCreate,
    EspecialidadUpdate,
    EspecialidadOut,
)
from app.db.database import get_db
from app.db.repositories.especialidad_repository import EspecialidadRepository
from app.domain.services.especialidad_service import EspecialidadService


router = APIRouter(prefix="/especialidades", tags=["especialidades"])


@router.get("/", response_model=list[EspecialidadOut])
def list_especialidades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = EspecialidadService(EspecialidadRepository(db))
    return service.list(skip=skip, limit=limit)


@router.get("/{id_especialidad}", response_model=EspecialidadOut)
def get_especialidad(id_especialidad: str, db: Session = Depends(get_db)):
    service = EspecialidadService(EspecialidadRepository(db))
    esp = service.get(id_especialidad)
    if not esp:
        raise HTTPException(404, "Especialidad no encontrada")
    return esp


@router.post("/", response_model=EspecialidadOut, status_code=status.HTTP_201_CREATED)
def create_especialidad(payload: EspecialidadCreate, db: Session = Depends(get_db)):
    service = EspecialidadService(EspecialidadRepository(db))
    try:
        return service.create(payload)
    except ValueError as ex:
        raise HTTPException(400, str(ex))


@router.put("/{id_especialidad}", response_model=EspecialidadOut)
def update_especialidad(id_especialidad: str, dto: EspecialidadUpdate, db: Session = Depends(get_db)):
    service = EspecialidadService(EspecialidadRepository(db))
    try:
        return service.update(id_especialidad, dto)
    except ValueError as ex:
        raise HTTPException(400, str(ex))


@router.delete("/{id_especialidad}", status_code=status.HTTP_204_NO_CONTENT)
def delete_especialidad(id_especialidad: str, db: Session = Depends(get_db)):
    service = EspecialidadService(EspecialidadRepository(db))
    ok = service.delete(id_especialidad)
    if not ok:
        raise HTTPException(404, "Especialidad no encontrada")
    return

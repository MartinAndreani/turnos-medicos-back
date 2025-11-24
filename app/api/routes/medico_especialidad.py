# app/api/routes/medico_especialidades.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repositories.medico_especialidad_repository import MedicoEspecialidadRepository
from app.db.repositories.medico_repository import MedicoRepository
from app.db.repositories.especialidad_repository import EspecialidadRepository
from app.domain.services.medico_especialidad_service import MedicoEspecialidadService
from app.api.schemas.especialidades import EspecialidadOut


router = APIRouter(
    prefix="/medicos/{id_medico}/especialidades",
    tags=["medico-especialidades"],
)


def get_service(db: Session = Depends(get_db)) -> MedicoEspecialidadService:
    me_repo = MedicoEspecialidadRepository(db)
    medico_repo = MedicoRepository(db)
    esp_repo = EspecialidadRepository(db)
    return MedicoEspecialidadService(me_repo, medico_repo, esp_repo)


# ===========================
# LISTAR ESPECIALIDADES DEL MÉDICO
# ===========================
@router.get("/", response_model=list[EspecialidadOut])
def list_especialidades_de_medico(
    id_medico: str,
    service: MedicoEspecialidadService = Depends(get_service),
):
    try:
        return service.listar_especialidades(id_medico)
    except ValueError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


# ===========================
# ASIGNAR ESPECIALIDAD
# ===========================
@router.post("/{id_especialidad}", response_model=EspecialidadOut, status_code=status.HTTP_201_CREATED)
def asignar_especialidad_a_medico(
    id_medico: str,
    id_especialidad: str,
    service: MedicoEspecialidadService = Depends(get_service),
):
    try:
        especialidad = service.asignar(id_medico, id_especialidad)
        return especialidad
    except ValueError as ex:
        # 400 si es regla de negocio, 404 si es no encontrado
        msg = str(ex)
        if "no existe" in msg or "no encontrado" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)


# ===========================
# QUITAR ESPECIALIDAD
# ===========================
@router.delete("/{id_especialidad}", status_code=status.HTTP_204_NO_CONTENT)
def quitar_especialidad_de_medico(
    id_medico: str,
    id_especialidad: str,
    service: MedicoEspecialidadService = Depends(get_service),
):
    try:
        service.quitar(id_medico, id_especialidad)
    except ValueError as ex:
        msg = str(ex)
        if "no encontrado" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)
    return

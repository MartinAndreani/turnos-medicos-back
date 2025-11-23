# app/api/routes/medicos.py

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repositories.medico_repository import MedicoRepository
from app.domain.services.medico_service import MedicoService


# ==========================================================
#  INSTANCIA DEL ROUTER
# ==========================================================
router = APIRouter(
    prefix="/medicos",
    tags=["Medicos"]
)


# ==========================================================
#  DEPENDENCIA PARA INYECTAR EL SERVICE
# ==========================================================
def get_service(db: Session = Depends(get_db)) -> MedicoService:
    repo = MedicoRepository(db)
    return MedicoService(repo)


# ==========================================================
#  ENDPOINTS ABMC — SIN DTO
# ==========================================================

# ----- LISTAR -----
@router.get("/")
def list_medicos(
    skip: int = 0,
    limit: int = 100,
    service: MedicoService = Depends(get_service)
):
    return service.list(skip=skip, limit=limit)


# ----- CREAR -----
@router.post("/")
def create_medico(
    payload: dict = Body(...),
    service: MedicoService = Depends(get_service)
):
    """
    Espera un JSON como:
    {
        "matricula": "...",
        "dni": "...",
        "nombre": "...",
        "apellido": "...",
        "telefono": "...",
        "id_usuario": "..."
    }
    """
    try:
        return service.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----- OBTENER POR ID -----
@router.get("/{id_medico}")
def get_medico(
    id_medico: str,
    service: MedicoService = Depends(get_service)
):
    medico = service.get(id_medico)
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return medico


# ----- ACTUALIZAR -----
@router.put("/{id_medico}")
def update_medico(
    id_medico: str,
    payload: dict = Body(...),
    service: MedicoService = Depends(get_service)
):
    """
    Campos opcionales:
    {
        "matricula": "...",
        "dni": "...",
        "nombre": "...",
        "apellido": "...",
        "telefono": "...",
        "activo": true/false,
        "id_usuario": "..."
    }
    """
    try:
        return service.update(id_medico, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----- DELETE (SOFT DELETE) -----
@router.delete("/{id_medico}")
def delete_medico(
    id_medico: str,
    service: MedicoService = Depends(get_service)
):
    success = service.delete(id_medico)
    if not success:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return {"status": "deleted"}


# ==========================================================
#  ENDPOINTS DE ESTADO
# ==========================================================
@router.put("/{id_medico}/activar")
def activar_medico(
    id_medico: str,
    service: MedicoService = Depends(get_service)
):
    try:
        return service.activar(id_medico)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id_medico}/desactivar")
def desactivar_medico(
    id_medico: str,
    service: MedicoService = Depends(get_service)
):
    try:
        return service.desactivar(id_medico)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

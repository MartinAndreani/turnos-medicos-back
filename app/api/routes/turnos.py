# app/api/routes/turnos.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repositories.turno_repository import TurnoRepository
from app.domain.services.turno_service import TurnoService


router = APIRouter(prefix="/turnos", tags=["turnos"])


# ============================================
#                 LISTAR
# ============================================
@router.get("/")
def list_turnos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = TurnoRepository(db)
    service = TurnoService(repo)
    return service.list(skip=skip, limit=limit)


# ============================================
#             OBTENER POR ID
# ============================================
@router.get("/{id_turno}")
def get_turno(id_turno: str, db: Session = Depends(get_db)):
    repo = TurnoRepository(db)
    turno = repo.get_by_id(id_turno)

    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    return turno


# ============================================
#                 CREAR
# ============================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_turno(payload: dict, db: Session = Depends(get_db)):
    repo = TurnoRepository(db)
    service = TurnoService(repo)

    try:
        turno = service.create(payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    return turno


# ============================================
#                 UPDATE
# ============================================
@router.put("/{id_turno}")
def update_turno(id_turno: str, payload: dict, db: Session = Depends(get_db)):
    repo = TurnoRepository(db)
    service = TurnoService(repo)

    try:
        turno = service.update(id_turno, payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    return turno


# ============================================
#            BAJA LOGICA (CANCELAR)
# ============================================
@router.delete("/{id_turno}", status_code=status.HTTP_204_NO_CONTENT)
def delete_turno(id_turno: str, db: Session = Depends(get_db)):
    repo = TurnoRepository(db)
    service = TurnoService(repo)

    ok = service.delete(id_turno)

    if not ok:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    return


# ============================================
#       LISTAR TURNOS POR MÉDICO
# ============================================
@router.get("/medico/{id_medico}")
def list_turnos_por_medico(
    id_medico: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    repo = TurnoRepository(db)
    service = TurnoService(repo)
    return service.list_by_medico(id_medico, skip=skip, limit=limit)


# ============================================
#       LISTAR TURNOS POR PACIENTE
# ============================================
@router.get("/paciente/{id_paciente}")
def list_turnos_por_paciente(
    id_paciente: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    repo = TurnoRepository(db)
    service = TurnoService(repo)
    return service.list_by_paciente(id_paciente, skip=skip, limit=limit)

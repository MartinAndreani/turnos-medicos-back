# app/api/routes/recetas.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repositories.receta_repository import RecetaRepository
from app.db.repositories.turno_repository import TurnoRepository
from app.domain.services.receta_service import RecetaService
from app.api.schemas.recetas import RecetaCreate, RecetaUpdate, RecetaOut


router = APIRouter(prefix="/recetas", tags=["recetas"])


# ------------------------GET----------------------------------
@router.get("/", response_model=list[RecetaOut])
def list_recetas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    receta_repo = RecetaRepository(db)
    turno_repo = TurnoRepository(db)
    service = RecetaService(receta_repo, turno_repo)
    return service.list(skip=skip, limit=limit)


@router.get("/{id_receta}", response_model=RecetaOut)
def get_receta(id_receta: str, db: Session = Depends(get_db)):
    receta_repo = RecetaRepository(db)
    turno_repo = TurnoRepository(db)
    service = RecetaService(receta_repo, turno_repo)

    receta = service.get(id_receta)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta


# ------------------------GET POR TURNO------------------------
@router.get("/turno/{id_turno}", response_model=list[RecetaOut])
def list_recetas_por_turno(id_turno: str, db: Session = Depends(get_db)):
    receta_repo = RecetaRepository(db)
    turno_repo = TurnoRepository(db)
    service = RecetaService(receta_repo, turno_repo)
    return service.list_by_turno(id_turno)


# ------------------------POST---------------------------------
@router.post("/", response_model=RecetaOut, status_code=status.HTTP_201_CREATED)
def create_receta(payload: RecetaCreate, db: Session = Depends(get_db)):
    receta_repo = RecetaRepository(db)
    turno_repo = TurnoRepository(db)
    service = RecetaService(receta_repo, turno_repo)

    try:
        receta = service.create(payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    return receta


# ------------------------PUT----------------------------------
@router.put("/{id_receta}", response_model=RecetaOut)
def update_receta(id_receta: str, dto: RecetaUpdate, db: Session = Depends(get_db)):
    receta_repo = RecetaRepository(db)
    turno_repo = TurnoRepository(db)
    service = RecetaService(receta_repo, turno_repo)

    try:
        return service.update(id_receta, dto)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


# ------------------------DELETE-------------------------------
@router.delete("/{id_receta}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receta(id_receta: str, db: Session = Depends(get_db)):
    receta_repo = RecetaRepository(db)
    turno_repo = TurnoRepository(db)
    service = RecetaService(receta_repo, turno_repo)

    ok = service.delete(id_receta)
    if not ok:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return

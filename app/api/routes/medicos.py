# app/api/routes/medicos.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repositories.medico_repository import MedicoRepository
from app.domain.services.medico_service import MedicoService

# Cuando tengas schemas, se colocan aquí:
from app.api.schemas.medicos import MedicoCreate, MedicoUpdate, MedicoOut


router = APIRouter(prefix="/medicos", tags=["medicos"])



# ------------------------GET----------------------------------

@router.get("/", response_model=list[MedicoOut])
def list_medicos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = MedicoRepository(db)
    service = MedicoService(repo)
    return service.list(skip=skip, limit=limit)

@router.get("/{id_medico}", response_model=MedicoOut)
def get_medico(id_medico: str, db: Session = Depends(get_db)):
    repo = MedicoRepository(db)
    medico = repo.get_by_id(id_medico)
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return medico

# ------------------------POST---------------------------------
@router.post("/",response_model=MedicoOut, status_code=status.HTTP_201_CREATED)
def create_medico(payload: MedicoCreate, db: Session = Depends(get_db)):
    repo = MedicoRepository(db)
    service = MedicoService(repo)
    try:
        medico = service.create(payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    return medico

# ------------------------PUT----------------------------------
@router.put("/{id_medico}", response_model=MedicoOut)
def update_medico(id_medico: str, dto: MedicoUpdate, db: Session = Depends(get_db)):
    repo = MedicoRepository(db)
    service = MedicoService(repo)
    try:
        return service.update(id_medico, dto)
    except ValueError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


# ------------------------DELETE-------------------------------
@router.delete("/{id_medico}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medico(id_medico: str, db: Session = Depends(get_db)):
    repo = MedicoRepository(db)
    service = MedicoService(repo)

    ok = service.delete(id_medico)

    if not ok:
        raise HTTPException(status_code=404, detail="Médico no encontrado")

    return

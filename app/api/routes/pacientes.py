# app/api/routes/pacientes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.schemas.pacientes import PacienteCreate, PacienteUpdate, PacienteOut
from app.db.database import get_db
from app.db.repositories.paciente_repository import PacienteRepository
from app.domain.services.paciente_service import PacienteService


router = APIRouter(prefix="/pacientes", tags=["pacientes"])


# ------------------------GET----------------------------------
@router.get("/", response_model=list[PacienteOut])
def list_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = PacienteRepository(db)
    service = PacienteService(repo)
    return service.list(skip=skip, limit=limit)

@router.get("/{id_paciente}", response_model=PacienteOut)
def get_paciente(id_paciente: str, db: Session = Depends(get_db)):
    repo = PacienteRepository(db)
    paciente = repo.get_by_id(id_paciente)
    if not paciente:
        raise HTTPException(404, "Paciente no encontrado")
    return paciente

# ------------------------POST---------------------------------
@router.post("/", response_model=PacienteOut, status_code=status.HTTP_201_CREATED)
def create_paciente(payload: PacienteCreate, db: Session = Depends(get_db)):
    repo = PacienteRepository(db)
    service = PacienteService(repo)
    try:
        paciente = service.create(payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    return paciente


# ------------------------PUT----------------------------------
@router.put("/{id_paciente}", response_model=PacienteOut)
def update_paciente(id_paciente: str, dto: PacienteUpdate, db: Session = Depends(get_db)):
    repo = PacienteRepository(db)
    service = PacienteService(repo)
    try:
        return service.update(id_paciente, dto)
    except ValueError as ex:
        raise HTTPException(404, str(ex))
    
    
    
# ------------------------DELETE-------------------------------
@router.delete("/{id_paciente}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paciente(id_paciente: str, db: Session = Depends(get_db)):
    repo = PacienteRepository(db)
    service = PacienteService(repo)
    ok = service.delete(id_paciente)
    if not ok:
        raise HTTPException(404, "Paciente no encontrado")
    return

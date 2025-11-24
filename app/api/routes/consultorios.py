


from fastapi import APIRouter, Depends, HTTPException, status
from app.api.schemas.consultorios import ConsultorioCreate, ConsultorioOut
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.repositories.consultorio_repository import ConsultorioRepository
from app.domain.services.consultorio_service import ConsultorioService

router = APIRouter(prefix="/consultorios", tags=["consultorios"])



# ------------------------GET----------------------------------
@router.get("/", response_model=list[ConsultorioOut])
def list_consultorios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = ConsultorioRepository(db)
    service = ConsultorioService(repo)
    return service.list(skip=skip, limit=limit)


@router.get("/{id_consultorio}", response_model=ConsultorioOut)
def get_consultorio(id_consultorio: str, db: Session = Depends(get_db)):
    repo = ConsultorioRepository(db)
    consultorio = repo.get_by_id(id_consultorio)
    if not consultorio:
        raise HTTPException(404, "Consultorio no encontrado")
    return consultorio

# ------------------------POST----------------------------------
@router.post("/", response_model = ConsultorioOut, status_code = status.HTTP_201_CREATED)
def create_consultorio(payload: ConsultorioCreate, db: Session = Depends(get_db)):
    repo = ConsultorioRepository(db)
    service = ConsultorioService(repo)
    try:
        consultorio = service.create(payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    return consultorio

# ------------------------DELETE----------------------------------
@router.delete("/{id_consultorio}", status_code=status.HTTP_204_NO_CONTENT)
def delete_consultorio(id_consultorio: str, db: Session = Depends(get_db)):
    repo = ConsultorioRepository(db)
    service = ConsultorioService(repo)
    ok = service.delete(id_consultorio)
    if not ok:
        raise HTTPException(404, "Consultorio no encontrado")
    return
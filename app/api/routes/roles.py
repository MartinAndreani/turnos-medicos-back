# app/api/routes/roles.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.roles import RolCreate, RolUpdate, RolOut
from app.db.database import get_db
from app.db.repositories.rol_repository import RolRepository
from app.domain.services.rol_service import RolService

router = APIRouter(prefix="/roles", tags=["roles"])


def get_service(db: Session = Depends(get_db)) -> RolService:
    repo = RolRepository(db)
    return RolService(repo)


@router.get("/", response_model=list[RolOut])
def list_roles(
    skip: int = 0,
    limit: int = 100,
    service: RolService = Depends(get_service)
):
    return service.list(skip, limit)


@router.get("/{id_rol}", response_model=RolOut)
def get_rol(
    id_rol: str,
    service: RolService = Depends(get_service)
):
    rol = service.get(id_rol)
    if not rol:
        raise HTTPException(404, "Rol no encontrado")
    return rol


@router.post("/", response_model=RolOut, status_code=status.HTTP_201_CREATED)
def create_rol(
    payload: RolCreate,
    service: RolService = Depends(get_service)
):
    try:
        return service.create(payload)
    except ValueError as ex:
        raise HTTPException(400, str(ex))


@router.put("/{id_rol}", response_model=RolOut)
def update_rol(
    id_rol: str,
    dto: RolUpdate,
    service: RolService = Depends(get_service)
):
    try:
        return service.update(id_rol, dto)
    except ValueError as ex:
        if "no encontrado" in str(ex):
            raise HTTPException(404, str(ex))
        raise HTTPException(400, str(ex))

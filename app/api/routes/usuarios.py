# app/api/routes/usuarios.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.usuarios import UsuarioCreate, UsuarioUpdate, UsuarioOut
from app.db.database import get_db
from app.db.repositories.usuario_repository import UsuarioRepository
from app.db.repositories.rol_repository import RolRepository
from app.db.repositories.rol_x_usuario_repository import RolXUsuarioRepository
from app.domain.services.usuario_service import UsuarioService


router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def get_service(db: Session = Depends(get_db)) -> UsuarioService:
    usuario_repo = UsuarioRepository(db)
    rol_repo = RolRepository(db)
    rxu_repo = RolXUsuarioRepository(db)
    return UsuarioService(usuario_repo, rol_repo, rxu_repo)


# ----------- GET LIST -----------
@router.get("/", response_model=list[UsuarioOut])
def list_usuarios(
    skip: int = 0,
    limit: int = 100,
    service: UsuarioService = Depends(get_service),
):
    return service.list(skip=skip, limit=limit)


# ----------- GET BY ID ----------
@router.get("/{id_usuario}", response_model=UsuarioOut)
def get_usuario(
    id_usuario: str,
    service: UsuarioService = Depends(get_service),
):
    usuario = service.get(id_usuario)
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")
    return usuario


# ----------- POST ---------------
@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def create_usuario(
    payload: UsuarioCreate,
    service: UsuarioService = Depends(get_service),
):
    try:
        return service.create(payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


# ----------- PUT ----------------
@router.put("/{id_usuario}", response_model=UsuarioOut)
def update_usuario(
    id_usuario: str,
    dto: UsuarioUpdate,
    service: UsuarioService = Depends(get_service),
):
    try:
        return service.update(id_usuario, dto)
    except ValueError as ex:
        msg = str(ex)
        if "no encontrado" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)


# ----------- DELETE ------------
@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(
    id_usuario: str,
    service: UsuarioService = Depends(get_service),
):
    ok = service.delete(id_usuario)
    if not ok:
        raise HTTPException(404, "Usuario no encontrado")
    return

# app/api/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.auth import LoginRequest, Token
from app.db.database import get_db
from app.db.repositories.usuario_repository import UsuarioRepository
from app.domain.services.auth_service import AuthService
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    repo = UsuarioRepository(db)
    service = AuthService(repo)

    try:
        usuario = service.authenticate(payload.email, payload.password)
    except ValueError as ex:
        # 401 Unauthorized
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ex),
        )

    # Contenido del token: podés agregar más claims si querés
    token_data = {
        "sub": usuario.id_usuario,  # ID del usuario
        "email": usuario.email,
    }
    access_token = create_access_token(token_data)

    return Token(access_token=access_token)

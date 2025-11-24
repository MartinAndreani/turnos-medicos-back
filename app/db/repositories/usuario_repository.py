# app/db/repositories/usuario_repository.py

from uuid import uuid4
from sqlalchemy.orm import Session

from app.db.models.usuarios import UsuarioModel
from app.domain.entities.usuarios import Usuario


def _row_to_domain(row: UsuarioModel) -> Usuario:
    return Usuario(
        id_usuario=str(row.id_usuario),
        email=row.email,
        password=row.password,
        activo=row.activo,
    )


class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    # ========= QUERIES BÁSICAS =========

    def get_by_id(self, id_usuario: str) -> Usuario | None:
        row = self.session.get(UsuarioModel, id_usuario)
        return _row_to_domain(row) if row else None

    def get_by_email(self, email: str) -> Usuario | None:
        row = (
            self.session.query(UsuarioModel)
            .filter(UsuarioModel.email == email)
            .first()
        )
        return _row_to_domain(row) if row else None

    def list(self, skip: int = 0, limit: int = 100) -> list[Usuario]:
        rows = (
            self.session.query(UsuarioModel)
            .filter(UsuarioModel.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [_row_to_domain(r) for r in rows]

    # ========= SAVE (CREATE/UPDATE) =========

    def save(self, usuario: Usuario) -> Usuario:
        row = self.session.get(UsuarioModel, usuario.id_usuario)

        if not row:
            row = UsuarioModel(
                id_usuario=usuario.id_usuario or str(uuid4())
            )

        row.email = usuario.email
        row.password = usuario.password
        row.activo = usuario.activo

        try:
            self.session.add(row)
            self.session.commit()
            self.session.refresh(row)
        except Exception:
            self.session.rollback()
            raise

        return _row_to_domain(row)

    # ========= BAJA LÓGICA =========

    def delete(self, id_usuario: str) -> bool:
        row = self.session.get(UsuarioModel, id_usuario)
        if not row:
            return False

        try:
            row.activo = False
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

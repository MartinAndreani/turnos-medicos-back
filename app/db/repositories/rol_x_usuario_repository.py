# app/db/repositories/rolxusuario_repository.py

from sqlalchemy import delete, select, insert
from sqlalchemy.orm import Session

from app.db.models.rolesxusuario import RolXUsuarioModel
from app.db.models.roles import RolModel


class RolXUsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def exists(self, id_usuario: str, id_rol: str) -> bool:
        stmt = (
            select(RolXUsuarioModel)
            .where(RolXUsuarioModel.id_usuario == id_usuario)
            .where(RolXUsuarioModel.id_rol == id_rol)
        )
        return self.session.execute(stmt).first() is not None

    def add(self, id_usuario: str, id_rol: str) -> None:
        try:
            self.session.execute(
                insert(RolXUsuarioModel).values(
                    id_usuario=id_usuario,
                    id_rol=id_rol,
                )
            )
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def remove_all_for_user(self, id_usuario: str) -> None:
        try:
            self.session.execute(
                delete(RolXUsuarioModel).where(
                    RolXUsuarioModel.id_usuario == id_usuario
                )
            )
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def list_roles_for_user(self, id_usuario: str) -> list[RolModel]:
        # Devuelve los modelos RolModel asociados (por si después los querés usar)
        return (
            self.session.query(RolModel)
            .join(RolXUsuarioModel, RolModel.id_rol == RolXUsuarioModel.id_rol)
            .filter(RolXUsuarioModel.id_usuario == id_usuario)
            .all()
        )

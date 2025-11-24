# app/db/repositories/rol_repository.py

from uuid import uuid4
from sqlalchemy.orm import Session

from app.db.models.roles import RolModel
from app.domain.entities.roles import Rol


def _row_to_domain(row: RolModel) -> Rol:
    return Rol(
        id_rol=str(row.id_rol),
        nombre=row.nombre,
        descripcion=row.descripcion,
        activo=row.activo,
    )


class RolRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id_rol: str) -> Rol | None:
        row = self.session.get(RolModel, id_rol)
        return _row_to_domain(row) if row else None

    def get_by_nombre(self, nombre: str) -> Rol | None:
        row = self.session.query(RolModel).filter_by(nombre=nombre).first()
        return _row_to_domain(row) if row else None

    def list(self, skip: int = 0, limit: int = 100) -> list[Rol]:
        rows = (
            self.session.query(RolModel)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [_row_to_domain(r) for r in rows]

    def save(self, rol: Rol) -> Rol:
        row = self.session.get(RolModel, rol.id_rol)

        if not row:
            row = RolModel(id_rol=rol.id_rol or str(uuid4()))

        row.nombre = rol.nombre
        row.descripcion = rol.descripcion
        row.activo = rol.activo

        try:
            self.session.add(row)
            self.session.commit()
            self.session.refresh(row)
        except Exception:
            self.session.rollback()
            raise

        return _row_to_domain(row)

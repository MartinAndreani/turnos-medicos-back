
from sqlalchemy.orm import Session
from app.db.models.consultorios import ConsultorioModel
from app.domain.entities.consultorios import Consultorio


def _row_to_domain(row: ConsultorioModel) -> Consultorio:
    return Consultorio(
        id_consultorio= row.id_consultorio,
        nombre = row.nombre,
        direccion = row.direccion,
        telefono = row.telefono,
        activo = row.activo,
        id_usuario = row.id_usuario,
    )
    
    
    
class ConsultorioRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def get_by_id(self, id_consultorio: str) -> Consultorio | None:
        row = self.session.get(ConsultorioModel, id_consultorio)
        return _row_to_domain(row) if row else None
    
    def list(self, skip: int = 0, limit: int = 100) -> list[Consultorio]:
        rows = (
            self.session.query(ConsultorioModel)
            .filter(ConsultorioModel.activo == True)   
            .offset(skip)
            .limit(limit)
            .all()
        )

        return [_row_to_domain(row) for row in rows]
    
    def list_all(self):
        return self.session.query(ConsultorioModel).all()
    
    
    def save(self,consultorio: Consultorio) -> Consultorio:
        if not row:
            row = ConsultorioModel(id_consultorio=consultorio.id_consultorio)
        row.numero_consultorio = consultorio.numero_consultorio
        row.piso = consultorio.piso
        row.activo = consultorio.activo
        try:
            self.session.add(row)
            self.session.commit()
            self.session.refresh(row)
        except:
            self.session.rollback()
            raise
        return _row_to_domain(row)
    
    def delete(self, id_consultorio: str) -> bool:
        row = self.session.get(ConsultorioModel, id_consultorio)
        if not row:
            return False
        try:
            self.session.delete(row)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            raise
        
    
    
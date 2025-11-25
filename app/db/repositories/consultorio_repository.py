from sqlalchemy.orm import Session
from app.db.models.consultorios import ConsultorioModel
from app.domain.entities.consultorios import Consultorio


def _row_to_domain(row: ConsultorioModel) -> Consultorio:
    return Consultorio(
        id_consultorio=str(row.id_consultorio), # Aseguramos convertir a str si es UUID
        # CORREGIDO: Usamos los campos reales de consultorio (numero y piso)
        # en lugar de nombre/direccion que parecían de otra entidad.
        numero_consultorio=row.numero_consultorio,
        piso=row.piso,
        activo=row.activo
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
        # Nota: Aquí deberías devolver dominios también, no modelos crudos
        rows = self.session.query(ConsultorioModel).all()
        return [_row_to_domain(row) for row in rows]
    
    
    def save(self, consultorio: Consultorio) -> Consultorio:
        # 1. PRIMERO BUSCAMOS: Definimos 'row' antes de usarlo
        row = self.session.get(ConsultorioModel, consultorio.id_consultorio)

        if not row:
            # 2. SI NO EXISTE: Creamos instancia nueva y la agregamos a la session
            row = ConsultorioModel(id_consultorio=consultorio.id_consultorio)
            self.session.add(row) # <--- Importante agregarla

        # 3. ACTUALIZAMOS DATOS (Común para crear y actualizar)
        row.numero_consultorio = consultorio.numero_consultorio
        row.piso = consultorio.piso
        row.activo = consultorio.activo

        try:
            self.session.commit()
            self.session.refresh(row)
        except Exception as e:
            self.session.rollback()
            raise e
            
        return _row_to_domain(row)
    
    def delete(self, id_consultorio: str) -> bool:
        row = self.session.get(ConsultorioModel, id_consultorio)
        if not row:
            return False
        try:
            # Opción A: Borrado físico
            # self.session.delete(row)
            
            # Opción B: Borrado lógico (Recomendado, solo desactivar)
            row.activo = False
            
            self.session.commit()
            return True
        except:
            self.session.rollback()
            raise
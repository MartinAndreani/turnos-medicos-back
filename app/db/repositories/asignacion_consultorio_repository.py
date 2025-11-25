from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from app.db.models.asignacion_consultorios import AsignacionConsultorioModel

class AsignacionConsultorioRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, asignacion_data: dict):
        row = AsignacionConsultorioModel(**asignacion_data)
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return row

    def get_overlap(self, id_consultorio, dias_nuevos: List[int], hora_inicio, hora_fin, fecha_inicio, fecha_fin):
        """
        Valida si el consultorio tiene conflicto en:
        1. Algún día de la lista (Array Overlap).
        2. Rango Horario.
        3. Rango de Fechas.
        """
        return (
            self.session.query(AsignacionConsultorioModel)
            .filter(
                AsignacionConsultorioModel.id_consultorio == UUID(str(id_consultorio)),
                AsignacionConsultorioModel.activo == True,
                
                # 1. Intersección de Arrays (Postgres '&&' operator)
                # Si comparten al menos un día, esto da True
                AsignacionConsultorioModel.dias_semana.overlap(dias_nuevos),
                
                # 2. Hora
                AsignacionConsultorioModel.hora_inicio < hora_fin,
                AsignacionConsultorioModel.hora_fin > hora_inicio,
                
                # 3. Fecha
                AsignacionConsultorioModel.fecha_inicio <= fecha_fin,
                AsignacionConsultorioModel.fecha_fin >= fecha_inicio
            )
            .first()
        )
    
    # ... resto de métodos ...
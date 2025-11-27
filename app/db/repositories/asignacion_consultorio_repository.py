from uuid import UUID
from datetime import date, time
from typing import List
from sqlalchemy.orm import Session
from app.db.models.asignacion_consultorios import AsignacionConsultorioModel

class AsignacionConsultorioRepository:
    def __init__(self, session: Session):
        self.session = session

    # ... (tus métodos existentes create, save, get_overlap, delete, get_by_id) ...
    
    def create(self, asignacion_data: dict):
        row = AsignacionConsultorioModel(**asignacion_data)
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return row

    def get_overlap(self, id_consultorio, dias_nuevos: List[int], hora_inicio, hora_fin, fecha_inicio, fecha_fin, jornada):
        # Nota: Este es el get_overlap que arreglamos antes para la CREACIÓN de agendas
        # (valida choque de arrays)
        return (
            self.session.query(AsignacionConsultorioModel)
            .filter(
                AsignacionConsultorioModel.id_consultorio == UUID(str(id_consultorio)),
                AsignacionConsultorioModel.activo == True,
                AsignacionConsultorioModel.dias_semana.overlap(dias_nuevos),
                AsignacionConsultorioModel.hora_inicio < hora_fin,
                AsignacionConsultorioModel.hora_fin > hora_inicio,
                AsignacionConsultorioModel.fecha_inicio <= fecha_fin,
                AsignacionConsultorioModel.fecha_fin >= fecha_inicio,
                AsignacionConsultorioModel.jornada == jornada
            )
            .first()
        )

    def delete(self, id_asignacion: str) -> bool:
        row = self.session.get(AsignacionConsultorioModel, UUID(id_asignacion))
        if not row: return False
        row.activo = False
        self.session.commit()
        return True
        
    def get_by_id(self, id_asignacion: UUID):
         return self.session.query(AsignacionConsultorioModel).filter_by(id_asignacion=id_asignacion).first()

    # --- NUEVO MÉTODO PARA TURNOS ---
    def find_for_turn(self, id_medico: str, fecha: date, dia: int, start: time, end: time):
        """
        Busca qué consultorio tiene asignado el médico para un momento específico.
        """
        return self.session.query(AsignacionConsultorioModel).filter(
            AsignacionConsultorioModel.id_medico == UUID(id_medico),
            AsignacionConsultorioModel.activo == True,
            
            # 1. Validar Vigencia Mensual
            AsignacionConsultorioModel.fecha_inicio <= fecha,
            AsignacionConsultorioModel.fecha_fin >= fecha,
            
            # 2. Validar Día (Array contains)
            AsignacionConsultorioModel.dias_semana.contains([dia]),
            
            # 3. Validar Horario (Contención estricta)
            AsignacionConsultorioModel.hora_inicio <= start,
            AsignacionConsultorioModel.hora_fin >= end
        ).first()
    

    def list(self, skip: int = 0, limit: int = 100):
        rows = (
            self.session.query(AsignacionConsultorioModel)
            .filter(AsignacionConsultorioModel.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return rows
    

    def get_overlap_update(
        self, id_consultorio, dias_nuevos, hora_inicio, hora_fin, fecha_inicio, fecha_fin, jornada, id_excluir
    ):
        return (
            self.session.query(AsignacionConsultorioModel)
            .filter(
                AsignacionConsultorioModel.id_consultorio == UUID(str(id_consultorio)),
                AsignacionConsultorioModel.activo == True,
                AsignacionConsultorioModel.id_asignacion != UUID(str(id_excluir)),
                AsignacionConsultorioModel.dias_semana.overlap(dias_nuevos),
                AsignacionConsultorioModel.hora_inicio < hora_fin,
                AsignacionConsultorioModel.hora_fin > hora_inicio,
                AsignacionConsultorioModel.fecha_inicio <= fecha_fin,
                AsignacionConsultorioModel.fecha_fin >= fecha_inicio,
                AsignacionConsultorioModel.jornada == jornada
            )
            .first()
        )
    

    def update(self, id_asignacion, data: dict):
        row = self.session.get(AsignacionConsultorioModel, UUID(str(id_asignacion)))
        if not row:
            return None

        for key, value in data.items():
            setattr(row, key, value)

        self.session.commit()
        self.session.refresh(row)
        return row
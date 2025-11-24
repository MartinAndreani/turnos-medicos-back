# app/db/repositories/asignacion_consultorio_repository.py

from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.asignacion_consultorios import AsignacionConsultorioModel
from datetime import date


class AsignacionConsultorioRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, asignacion: AsignacionConsultorioModel):
        self.db.add(asignacion)
        self.db.commit()
        self.db.refresh(asignacion)
        return asignacion

    def get_by_id(self, id_asignacion: UUID):
        return self.db.query(AsignacionConsultorioModel).filter_by(id_asignacion=id_asignacion).first()

    def delete(self, id_asignacion: UUID) -> bool:
        asignacion = self.get_by_id(id_asignacion)
        if not asignacion:
            return False
        asignacion.activo = False
        self.db.commit()
        return True

    def list(self, skip=0, limit=100):
        return (
            self.db.query(AsignacionConsultorioModel)
            .filter_by(activo=True)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    #VALIDA SOLAPAMIENTO DE CONSULTARIO
    def get_overlap(self, id_consultorio, jornada, fecha_inicio, fecha_fin):
        return (
            self.db.query(AsignacionConsultorioModel)
            .filter(
                AsignacionConsultorioModel.id_consultorio == id_consultorio,
                AsignacionConsultorioModel.jornada == jornada,
                AsignacionConsultorioModel.activo == True,
                AsignacionConsultorioModel.fecha_inicio <= fecha_fin,
                AsignacionConsultorioModel.fecha_fin >= fecha_inicio,
            )
            .first()
        )


    #VALIDA SOLAPAMIENTO DE MEDICO
    def get_overlap_medico(self, id_medico, jornada, fecha_inicio, fecha_fin):
        return (
            self.db.query(AsignacionConsultorioModel)
            .filter(
                AsignacionConsultorioModel.id_medico == id_medico,
                AsignacionConsultorioModel.jornada == jornada,
                AsignacionConsultorioModel.activo == True,
                AsignacionConsultorioModel.fecha_inicio <= fecha_fin,
                AsignacionConsultorioModel.fecha_fin >= fecha_inicio,
            )
            .first()
        )
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models.historias_clinicas import HistoriaClinicaModel

class HistoriaClinicaReportsRepository:

    def __init__(self, db: Session):
        self.db = db

    def obtener_diagnosticos_frecuentes(self, limite: int = 10):
        return (
            self.db.query(
                HistoriaClinicaModel.diagnostico,
                func.count(HistoriaClinicaModel.id_historia_clinica).label("cantidad")
            )
            .filter(HistoriaClinicaModel.diagnostico.isnot(None))
            .group_by(HistoriaClinicaModel.diagnostico)
            .order_by(func.count(HistoriaClinicaModel.id_historia_clinica).desc())
            .limit(limite)
            .all()
        )

    def obtener_tratamientos_frecuentes(self, limite: int = 10):
        return (
            self.db.query(
                HistoriaClinicaModel.tratamiento,
                func.count(HistoriaClinicaModel.id_historia_clinica).label("cantidad")
            )
            .filter(HistoriaClinicaModel.tratamiento.isnot(None))
            .group_by(HistoriaClinicaModel.tratamiento)
            .order_by(func.count(HistoriaClinicaModel.id_historia_clinica).desc())
            .limit(limite)
            .all()
        )
    
    def obtener_registros_por_paciente(self, id_paciente: str):
        return (
            self.db.query(HistoriaClinicaModel)
            .filter(
                HistoriaClinicaModel.id_paciente == id_paciente,
                HistoriaClinicaModel.activo == True
            )
            .order_by(HistoriaClinicaModel.fecha_registro.asc())
            .all()
        )

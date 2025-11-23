from uuid import uuid4
from sqlalchemy.orm import Session
from app.db.models.pacientes import PacienteModel
from app.domain.entities.pacientes import Paciente


def _row_to_domain(row: PacienteModel) -> Paciente:
    return Paciente(
        id_paciente= row.id_paciente,
        dni = row.dni,
        nombre = row.nombre,
        apellido = row.apellido,
        fecha_nacimiento = row.fecha_nacimiento,
        direccion = row.direccion,
        telefono = row.telefono,
        activo = row.activo,
        id_usuario = row.id_usuario,

    )
    
    
class PacienteRepository:
    def __init__(self, session: Session):
        self.session = session
    
    #BUSCA POR ID
    def get_by_id(self, id_paciente: str) -> Paciente | None:
        row = self.session.get(PacienteModel, id_paciente)
        return _row_to_domain(row) if row else None
    
    #BUSCA POR DNI
    def get_by_dni(self, dni: str) -> Paciente | None:
        row = self.session.query(PacienteModel).filter_by(dni=dni).first()
        return _row_to_domain(row) if row else None
    
    #LISTA PACIENTE, PAGINADO
    def list(self, skip: int = 0, limit: int = 100) -> list[Paciente]:
        rows = (
            self.session.query(PacienteModel)
            .filter(PacienteModel.activo == True)   
            .offset(skip)
            .limit(limit)
            .all()
        )

        return [_row_to_domain(row) for row in rows]
    
    
    def list_all(self):
        return self.session.query(PacienteModel).all()

    
    # CREA PACIENTE - MODIFICAR 
    def save(self, paciente: Paciente) -> Paciente:
        row = self.session.get(PacienteModel, paciente.id_paciente)
        if not row: 
            row = PacienteModel(id_paciente=paciente.id_paciente or str(uuid4()))
        row.dni = paciente.dni
        row.nombre = paciente.nombre
        row.apellido = paciente.apellido
        row.fecha_nacimiento = paciente.fecha_nacimiento
        row.direccion = paciente.direccion
        row.telefono = paciente.telefono
        row.activo = paciente.activo
        row.id_usuario = paciente.id_usuario
        
        try:
            self.session.add(row)
            self.session.commit()
            self.session.refresh(row)
        except: 
            self.session.rollback()
            raise
        return _row_to_domain(row)
    
    
    def delete(self, id_paciente: str) -> bool:
        row = self.session.get(PacienteModel, id_paciente)
        if not row:
            return False

        try:
            row.activo = False
            self.session.commit()
            return True
        except:
            self.session.rollback()
            raise


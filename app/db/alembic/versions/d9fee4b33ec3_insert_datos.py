"""insert datos

Revision ID: d9fee4b33ec3
Revises: a27c2313e139
Create Date: 2025-11-22 17:10:14.490591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9fee4b33ec3'
down_revision: Union[str, Sequence[str], None] = 'a27c2313e139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    #Roles
    op.execute(
        """
        INSERT INTO roles (nombre, descripcion, activo)
        VALUES 
        ('ADMIN', 'Administrador del sistema', true),
        ('MEDICO', 'Medico del sistema', true),
        ('RECEPCIONISTA', 'Recepcionista del sistema', true),
        ('PACIENTE', 'Paciente del sistema', true);
        """
    )
    
    
    #Estados Turnos
    op.execute(
        """
        INSERT INTO estados_turnos (nombre, descripcion, activo)
        VALUES
        ('AGENDADO', 'El paciente lo elige y se crea el registro en Turnos.', true),
        ('PENDIENTE', 'Turno pendiente de confirmacion', true),
        ('CONFIRMADO', 'El paciente confirma asistencia al turno.', true),
        ('EN SALA DE ESPERA', 'El paciente se encuentra en la sala de espera del consultorio.', true),
        ('EN ATENCION', 'El paciente se encuentra siendo atendido por el medico.', true),
        ('ATENDIDO', 'El paciente ha sido atendido y el turno finalizo correctamente.', true),
        ('AUSENTE', 'El paciente no se presento al turno.', true),
        ('CANCELADO POR PACIENTE', 'El paciente cancelo el turno.', true),
        ('CANCELADO POR MEDICO', 'El medico cancelo el turno.', true);
        """
    )
    

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM roles;")
    op.execute("DELETE FROM estados_turnos;")
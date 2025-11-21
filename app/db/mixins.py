


from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column( TIMESTAMP(timezone = True), server_default = func.now(), nullable = False)
    updated_at: Mapped[datetime] = mapped_column( TIMESTAMP(timezone = True), server_default = func.now(), onupdate = func.now(), nullable = False)    
    
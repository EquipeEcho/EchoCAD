from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base

# table de registro de arquivos de upload
# será usado depois pra facilitar o acesso aos arquivos
class FileCad(Base):
    __tablename__ = 'files_cad'

    filename: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False) 
    file_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    upload_at: Mapped[datetime] = mapped_column(server_default=func.now(), init=False)
"""
Файл для определения моделей базы данных
"""

from sqlalchemy import Column, String, Integer, DateTime
from database import Base
from datetime import datetime, timezone


class MediaFile(Base):
    __tablename__ = "file_inform"

    id = Column(String, primary_key=True, index=True)
    file_path = Column(String)
    file_type = Column(String)
    file_size = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


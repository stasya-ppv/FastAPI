"""
Файл для определения моделей базы данных
"""

from sqlmodel import SQLModel, Field
from datetime import datetime


class MediaFile(SQLModel, table=True):
    id: str = Field(primary_key=True, index=True)
    file_path: str
    file_type: str
    file_size: int
    created_at: datetime = Field(default_factory=datetime.utcnow)



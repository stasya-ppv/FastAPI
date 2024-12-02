"""
Файл для операций с базой данных, таких как добавление и извлечение файлов.
"""

from sqlmodel import Session
from models import MediaFile


def create_media_file(db: Session, file_uuid: str, file_path: str, file_type: str, file_size: int):
    media_file = MediaFile(
        id=file_uuid,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
    )
    db.add(media_file)
    db.commit()
    db.refresh(media_file)
    return media_file


def get_media_file_by_id(db: Session, file_id: str):
    return db.get(MediaFile, file_id)

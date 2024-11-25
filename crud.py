"""
Файл для операций с базой данных, таких как добавление и извлечение файлов.
"""

from sqlalchemy.orm import Session
from models import MediaFile

# Добавление файла в базу данных
def create_media_file(db: Session, file_uuid: str, file_path: str, file_type: str, file_size: int):
    db_file = MediaFile(
        id=file_uuid,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

# Получение информации о файле по UUID
def get_media_file_by_id(db: Session, file_id: str):
    return db.query(MediaFile).filter(MediaFile.id == file_id).first()

"""
Файл для конфигурации SQLAlchemy, создания сессий и работы с базой данных
"""
from sqlmodel import SQLModel, create_engine, Session

username = "postgres"
password = "qwerty123"

DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@localhost:5432/media_db"

engine = create_engine(DATABASE_URL, echo=True)


def get_db():
    with Session(engine) as session:
        yield session

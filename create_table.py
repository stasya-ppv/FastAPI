from sqlalchemy import create_engine
from database import Base, DATABASE_URL  # Импортируйте Base из вашего файла database.py
from models import MediaFile

# Создайте подключение к базе данных
engine = create_engine(DATABASE_URL)  # или URL для другой СУБД

# Удаление всех таблиц
Base.metadata.drop_all(engine)

# Повторное создание всех таблиц
Base.metadata.create_all(engine)

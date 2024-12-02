"""
Чтобы проверить работу API в интернете, необходимо перейти по http://localhost:8000/docs
Чтобы проверить работу методов через командную строку Windows
    1. Надо перейти в каталог с данным кодом и запустить его
        uvicorn main:app --reload
    2. Для загрузки файла:
        curl -X 'PUT' "http://127.0.0.1:8000/upload/{file_uuid}" -F "file=@path_to_your_file"
        file_id — это уникальный id для загружаемого файла.
        path_to_your_file — это путь к файлу на вашем компьютере.
    3. Для скачивания файла:
    с превью:
        curl -X 'GET' "http://127.0.0.1:8000/download/{file_uuid}?width=200&height=200"
    без превью:
        curl -X 'GET' "http://127.0.0.1:8000/download/{file_uuid}"
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse, StreamingResponse
from PIL import Image
from io import BytesIO
import cv2
import os
import uvicorn
import uuid
from database import get_db
from crud import create_media_file, get_media_file_by_id
from sqlmodel import Session

app = FastAPI()

# Папка для хранения загруженных файлов
UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.put("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Загружает файл (изображение или видео) на сервер с уникальным ID (file_id).
    """

    file_extension = file.filename.split(".")[-1]
    file_uuid = str(uuid.uuid4())

    if file_extension in ["png", "jpg", "jpeg"]:
        file_type = "IMG"
    elif file_extension in ["mp4", "avi"]:
        file_type = "VID"
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_path = os.path.join(UPLOAD_DIRECTORY, f"{file_uuid}.{file_extension}")

    with open(file_path, "wb", encoding='utf-8') as buffer:
        buffer.write(await file.read())

    # Сохранение информации о файле в базе данных
    file_size = os.path.getsize(file_path)
    create_media_file(db=db, file_uuid=file_uuid, file_path=file_path, file_type=file_type, file_size=file_size)

    return {"message": "File uploaded successfully", "file_id": file_uuid, "file_extension": file_extension}


@app.get("/download/{file_id}")
async def download_file(file_id: str, width: int = None, height: int = None, db: Session = Depends(get_db)):
    """
    Загружает файл с сервера по ID. Если это изображение и указаны ширина и высота, возвращает превью.
    Если это видео, возвращает превью первого кадра как изображение.
    """
    media_file = get_media_file_by_id(db=db, file_id=file_id)

    if not media_file:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = media_file.file_path
    file_extension = file_path.split(".")[-1]

    # Обработка изображения
    if file_extension in ["png", "jpg", "jpeg"]:
        if width and height:
            with Image.open(file_path) as img:
                img = img.resize((width, height))
                preview_io = BytesIO()
                img.save(preview_io, format="PNG")
                preview_io.seek(0)
                return StreamingResponse(preview_io, media_type="image/png",
                                         headers={"Content-Disposition": f"attachment; filename={file_id}_preview.png"})
        return FileResponse(file_path, media_type=f"image/{file_extension}", filename=f"{file_id}.{file_extension}")

    # Обработка видео
    elif file_extension in ["mp4", "avi"]:
        if width and height:
            cap = cv2.VideoCapture(file_path)
            success, frame = cap.read()
            cap.release()
            if not success:
                raise HTTPException(status_code=500, detail="Failed to capture video frame")

            # Изменяем размер кадра для превью
            frame = cv2.resize(frame, (width, height))
            _, buffer = cv2.imencode('.png', frame)
            preview_io = BytesIO(buffer.tobytes())
            return StreamingResponse(preview_io, media_type="image/png",
                                     headers={"Content-Disposition": f"attachment; filename={file_id}_preview.png"})

        # Если не требуется превью, возвращаем видеофайл
        return FileResponse(file_path, media_type="video/mp4", filename=f"{file_id}.{file_extension}")


if __name__ == "__main__":
    # Параметры запуска сервера
    host = "0.0.0.0"
    port = 8000
    print(f"Starting server at http://localhost:{port}/docs")

    # Запуск сервера с указанными параметрами
    uvicorn.run(app, host=host, port=port)

import shutil
import os
import torch
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from ultralytics import YOLO
import mapping as mp

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


app = FastAPI()

origins = ["http://localhost:63342"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Директория, в которую будут сохранены загруженные файлы
UPLOAD_DIR = "data/uploaded_files"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

model = YOLO('../data/weights/best.pt')


def mapping(result):
    index = int(torch.argmax(result[0].probs.data.to('cpu')))
    letter = result[0].names[index]
    mapping_letter = mp.mapping_abc[letter]
    return mapping_letter


def predict(image_path):
    result = model(image_path, device=DEVICE)
    mapping_letter = mapping(result)
    return mapping_letter


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Создаем путь для сохранения файла
    image_path = os.path.join(UPLOAD_DIR, file.filename)

    # Сохраняем файл на сервере
    with open(image_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = predict(image_path)

    # Возвращаем информацию о загруженном файле
    return {"filename": file.filename, "file_path": image_path}


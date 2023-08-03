import os
import shutil
import torch
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from typing import Dict

import mapping as mp
from constants import global_config

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
app = FastAPI()

origins = ["https://df86-88-201-168-105.ngrok-free.app",
           "http://127.0.0.1:8080",
           "http://127.0.0.1:63342",
           "http://localhost:63342"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["multipart/form-data"],
)

UPLOAD_DIR = global_config.UPLOAD_DIR
MODEL_DIR = global_config.MODEL_DIR
model = YOLO(MODEL_DIR)


def results_processing(results: YOLO, letter_index: int) -> bool:
    predict_index = int(torch.argmax(results[0].probs.data.to('cpu')))
    predict_letter_index = results[0].names[predict_index]
    predict_letter = mp.mapping_abc[predict_letter_index]
    drawn_letter = mp.draw_mapping_abc[letter_index]
    if predict_letter.lower() == drawn_letter:
        result = True
        probs = results[0].probs.data[predict_index].to('cpu')
        if probs <= .95:
            result = False
    else:
        result = False
    return result


def predict(image_path: str, letter_index: int) -> bool:
    results = model(image_path, device=DEVICE)
    result = results_processing(results, letter_index)
    return result


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), letter_index: int = Form(...)) -> Dict[str, bool]:

    # Создаем путь для сохранения файла
    assert file.filename is not None
    image_path = os.path.join(UPLOAD_DIR, file.filename)

    # Сохраняем файл на сервере
    with open(image_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = predict(image_path, letter_index)
    return {"result": result}

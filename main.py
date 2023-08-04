"""
    Основная логика приложения.
    Модуль получает изображение, распознает рукописную букву,
    возвращает ответ.
"""

import os
import shutil
from typing import Dict
import torch
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO

import mapping as mp
from constants import global_config

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
app = FastAPI()
app.mount("/public", StaticFiles(directory="public", html=True), name="static")

# Определяем хосты, который разрешены запросы.
origins = [""]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["multipart/form-data"],
)

UPLOAD_DIR = os.path.abspath(global_config.UPLOAD_DIR)
MODEL_DIR = os.path.abspath(global_config.MODEL_DIR)
model = YOLO(MODEL_DIR)


def results_processing(results: YOLO, letter_index: int) -> bool:
    """
        Функция для обработки результатов работы модели:
        Находит букву с максимальной вероятностью,
        сравнивает ее с нарисованной буквой.
        :param results: Объект YOLO;
        :param letter_index: Индекс нарисованной буквы;
        :return: Буквы совпали: True, нет: False;
    """
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
    """
        Функция получает предсказание модели,
        передает в функцию results_processing для обработки.
        :param image_path: Путь к изображению;
        :param letter_index: Индекс нарисованной буквы;
        :return: Буквы совпали: True, нет: False;
    """
    results = model(image_path, device=DEVICE)
    result = results_processing(results, letter_index)
    return result


@app.get("/public")
async def root() -> FileResponse:
    """
        Функция отдает на фронт статичную html страницу.
    """
    return FileResponse('public/index.html', media_type="text/html")


@app.post("/upload")
async def upload_image(file: UploadFile = File(...),
                       letter_index: int = Form(...)) -> Dict[str, bool]:
    """
        Функция получает изображение и индекс буквы с фронта,
        сохраняет изображение, передает его модели.
        :param file: Изображение с нарисованной буквой;
        :param letter_index: Индекс нарисованной буквы;
        :return: Буквы совпали: True, нет: False;
    """

    # Создаем путь для сохранения файла
    assert file.filename is not None
    image_path = os.path.join(UPLOAD_DIR, file.filename)

    # Сохраняем файл на сервере
    with open(image_path, "wb") as file_handle:
        shutil.copyfileobj(file.file, file_handle)

    result = predict(image_path, letter_index)
    return {"result": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
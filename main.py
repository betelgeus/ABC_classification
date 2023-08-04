"""
    Основная логика приложения.
    Модуль получает изображение, распознает рукописную букву,
    возвращает ответ.
"""

import os
import shutil
from typing import Dict
import torch
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO

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

UPLOAD_DIR = os.path.abspath(global_config.UPLOAD_DIR)
print("++++++++++")
print("MAIN UPLOAD_DIR", UPLOAD_DIR)
print("++++++++++")
MODEL_DIR = os.path.abspath(global_config.MODEL_DIR)
print("++++++++++")
print("MAIN MODEL_DIR", MODEL_DIR)
print("++++++++++")
model = YOLO(MODEL_DIR)


def results_processing(results: YOLO, letter_index: int) -> bool:
    """
        Функция для обработки результатов работы модели:
        Находит букву с максимальной вероятностью,
        сравнивает ее с нарисованной буквой.
        :param results: объект YOLO;
        :param letter_index: индекс нарисованной буквы;
        :return: буквы совпали: True, нет: False;
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
        :param image_path: путь к изображению;
        :param letter_index: индекс нарисованной буквы;
        :return: буквы совпали: True, нет: False;
    """
    results = model(image_path, device=DEVICE)
    result = results_processing(results, letter_index)
    return result


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...),
                       letter_index: int = Form(...)) -> Dict[str, bool]:
    """
        Функция получает изображение и индекс буквы с фронта,
        сохраняет изображение, передает его модели.
        :param file: изображение с нарисованной буквой;
        :param letter_index: индекс нарисованной буквы;
        :return: буквы совпали: True, нет: False;
    """

    # Создаем путь для сохранения файла
    assert file.filename is not None
    image_path = os.path.join(UPLOAD_DIR, file.filename)

    # Сохраняем файл на сервере
    with open(image_path, "wb") as file_handle:
        shutil.copyfileobj(file.file, file_handle)

    result = predict(image_path, letter_index)
    return {"result": result}

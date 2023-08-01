import os
import shutil
import torch
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
# from ultralytics import YOLO
from pathlib import Path
import mapping as mp

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

app = FastAPI()

origins = ["http://localhost:63342", "https://9f32-88-201-168-105.ngrok-free.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["multipart/form-data"],
)

UPLOAD_DIR = "data/uploaded_files"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
# model = YOLO('./data/weights/printed_and_written.pt')


def results_processing(results, letter_index):
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


def predict(image_path, letter_index):
    results = model(image_path, device=DEVICE)
    result = results_processing(results, letter_index)
    return result


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), letter_index: int = Form(...)):
    # Создаем путь для сохранения файла
    image_path = os.path.join(UPLOAD_DIR, file.filename)

    # Сохраняем файл на сервере
    with open(image_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = predict(image_path, letter_index)
    return {"result": result}

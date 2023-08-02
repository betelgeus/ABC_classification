"""
Тестируем на моках
"""

import os
from fastapi.testclient import TestClient  # Импортируем тестовый клиент
from unittest.mock import patch  # Импортируем библиотеку с моками
from dotenv import load_dotenv
from main import app  # Импортируем приложение FastAPI()
from main import predict  # Импортируем predict функцию, чтобы ее замокать


# Создаем директорию для загрузки файлов
UPLOAD_DIR = os.getenv("TEST_DATA_DIR")


def test_upload_image():
    client = TestClient(app)
    try:
        # Загружаем тестовый файл и данные формы
        with open(os.path.join(UPLOAD_DIR, "1690920920325.png"), "rb") as f:
            files = {"file": ("1690920920325_2.png", f, "image/png")}
            data = {"letter_index": "1"}

            # Замокаем функцию predict и вернем фиксированный результат
            with patch("main.predict") as mock_predict:
                mock_predict.return_value = True

                # Отправляем POST-запрос на сервер
                response = client.post("/upload/", files=files, data=data)

        # Проверяем, что запрос успешно обработан
        assert response.status_code == 200

        # Проверяем, что результат предсказания успешен
        assert response.json() == {"result": True}

        # Проверяем, что файл успешно сохранен
        assert os.path.exists(os.path.join(UPLOAD_DIR, "1690920920325_2.png"))
    finally:
        os.remove(os.path.join(UPLOAD_DIR, "1690920920325_2.png"))

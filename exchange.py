import os
import tempfile
from fastapi.testclient import TestClient
from app import app

# Импортируем predict функцию, чтобы ее замокать
from app import predict

# Импортируем библиотеку unittest.mock
from unittest.mock import patch

# Создаем временную директорию для загрузки файлов
UPLOAD_DIR = tempfile.mkdtemp()

def test_upload_image():
    client = TestClient(app)

    # Загружаем тестовый файл и данные формы
    with open("test_image.jpg", "rb") as f:
        files = {"file": ("test_image.jpg", f, "image/jpeg")}
        data = {"letter_index": 1}

        # Замокаем функцию predict и вернем фиксированный результат
        with patch("app.predict") as mock_predict:
            mock_predict.return_value = {"success": True}

            # Отправляем POST-запрос на сервер
            response = client.post("/upload/", files=files, data=data)

    # Проверяем, что запрос успешно обработан
    assert response.status_code == 200

    # Проверяем, что результат предсказания успешен
    assert response.json() == {"result": {"success": True}}

    # Проверяем, что файл успешно сохранен
    assert os.path.exists(os.path.join(UPLOAD_DIR, "test_image.jpg"))
"""
   Модуль содержит глобальные переменные
"""
import os


class GlobalConfig:
    """
        Класс для инициализации глобальных переменных
        MODEL_DIR: веса модели
        UPLOAD_DIR: папка с сохраненными изображениями
        TEST_DOWNLOAD_DIR: папка с изображениями для тестов
    """
    def __init__(self) -> None:
        self.MODEL_DIR = "./data/weights/printed_and_written.pt"
        self.UPLOAD_DIR = "./data/uploaded_files/"

        self.TEST_DOWNLOAD_DIR = "./data/test_data/"


global_config = GlobalConfig()

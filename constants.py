"""
   Модуль содержит глобальные переменные
"""
import os


class GlobalConfig:
    """
        Класс для инициализации глобальных переменных
        MODEL_DIR: веса модели
        UPLOAD_DIR: папка с сохраненными изображениями
        TEST_MODEL_DIR: веса модели для запуска тестов
        TEST_DATA_DIR: папка с изображениями для тестов
    """
    def __init__(self) -> None:
        self.MODEL_DIR = "./data/weights/printed_and_written.pt"
        self.UPLOAD_DIR = "./data/uploaded_files/"
        self.TEST_MODEL_DIR = "./tests/data/weights/printed_and_written.pt"
        self.TEST_DATA_DIR = "./tests/data/uploaded_files/"


global_config = GlobalConfig()

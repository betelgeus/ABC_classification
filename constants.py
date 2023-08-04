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
        """
            Прохождение тестов:
            локально:
                все пути ./
            Dev CI #33
                все пути ./
                /home/runner/work/ABC_classification/ABC_classification/data/uploaded_files/1690920920325_1.png

        """
        self.MODEL_DIR = "./data/weights/printed_and_written.pt"
        self.UPLOAD_DIR = "../data/uploaded_files/"

        self.TEST_DOWNLOAD_DIR = "./data/test_data/"


global_config = GlobalConfig()

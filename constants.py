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
        """
            Прохождение тестов:
            локально:
                все пути ./
            git:
                все пути ../
                    падает на загрузке модели, хотя вроде путь правильный
                    No such file or directory:
                    '/home/runner/work/ABC_classification/data/weights/printed_and_written.pt
                путь UPLOAD_DIR ../, остальные ./
                    проходит два теста, падает на последнем
                    FileNotFoundError: [Errno 2]
                    No such file or directory: '/home/runner/work/ABC_classification/data/uploaded_files/1690920920325_1.png'
                DEV CI #24 путь TEST_UPLOAD_DIR ../, остальные ./
                    проходит два теста, падает на последнем
                    FileNotFoundError: [Errno 2]
                     No such file or directory: '/home/runner/work/ABC_classification/ABC_classification/data/uploaded_files/1690920920325_1.png'
                DEV CI #25 путь TEST_UPLOAD_DIR, TEST_DATA_DIR ../, остальные ./
                    падают все тесты
                DEV CI #26
                            self.MODEL_DIR = "./data/weights/printed_and_written.pt"
                            self.UPLOAD_DIR = "./data/uploaded_files/"
                            self.TEST_MODEL_DIR = "../data/weights/printed_and_written.pt"
                            self.TEST_DATA_DIR = "../data/uploaded_files/"
                            self.TEST_UPLOAD_DIR = "../data/uploaded_files/"
                    падают все тесты
                    UPLOAD_DIR /home/runner/work/ABC_classification/ABC_classification/data/uploaded_files
                    MODEL_DIR /home/runner/work/ABC_classification/ABC_classification/data/weights/printed_and_written.pt
                DEV CI #27



        """
        self.MODEL_DIR = "./data/weights/printed_and_written.pt"
        self.UPLOAD_DIR = "./data/uploaded_files/"
        self.TEST_MODEL_DIR = "../data/weights/printed_and_written.pt"
        self.TEST_DATA_DIR = "../data/uploaded_files/"
        self.TEST_UPLOAD_DIR = "../data/uploaded_files/"



global_config = GlobalConfig()

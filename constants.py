import os


class GlobalConfig:
    def __init__(self):
        self.MODEL_DIR = "./data/weights/printed_and_written.pt"
        self.UPLOAD_DIR = os.path.abspath("./data/uploaded_files/")
        self.TEST_MODEL_DIR = os.path.abspath("./tests/data/weights/printed_and_written.pt")
        self.TEST_DATA_DIR = os.path.abspath("./tests/data/uploaded_files/")


global_config = GlobalConfig()

print(global_config.UPLOAD_DIR)
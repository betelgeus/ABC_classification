class GlobalConfig:
    def __init__(self):
        self.MODEL_DIR = "./data/weights/printed_and_written.pt"
        self.TEST_MODEL_DIR = "../tests/data/weights/printed_and_written.pt"
        self.TEST_DATA_DIR = "../tests/data/uploaded_files/"


global_config = GlobalConfig()

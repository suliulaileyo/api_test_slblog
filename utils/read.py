import os

import configparser

ini_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"config","setting.ini")

class FileRead:
    def __init__(self):
        self.ini_path = ini_path

    """
    读取ini配置文件
    """
    def read_ini(self):
        config = configparser.ConfigParser()
        config.read(self.ini_path, encoding="utf8")
        return config

base_data = FileRead()
print(base_data.read_ini())
# print(hex(base_data.read_ini()))
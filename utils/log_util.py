import logging
import os
import time

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) # 获取项目根目录路径
log_path = os.path.join(root_path, "log")

class Logger:
    def __init__(self):
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        # 定义日志位置和文件名
        self.logname = os.path.join(log_path, "{}.log".format(time.strftime("%Y-%m-%d")))
        # 定义一个日志容器
        self.logger = logging.getLogger("log")
        # 设置日志打印级别
        self.logger.setLevel(logging.DEBUG)
        # 创建日志输出格式
        # 格式包含：时间、文件名 行号、日志级别、日志消息
        self.formater = logging.Formatter(
            '[%(asctime)s][%(filename)s %(lineno)d][%(levelname)s]: %(message)s'
        )
        # 创建一个FileHandler,用于将日志写入文件
        self.filelogger = logging.FileHandler(self.logname,mode='a',encoding="utf8")
        # 创建一个 StreamHandler,用于将日志打印到控制台
        self.console = logging.StreamHandler()
        # 设置控制台处理器的日志级别也为DEBUG
        self.console.setLevel(logging.DEBUG)
        # 设置文件处理器的日志级别也为DEBUG
        self.filelogger.setLevel(logging.DEBUG)
        # 将之前定义的格式应用到文件和控制台处理器上
        self.filelogger.setFormatter(self.formater)
        self.console.setFormatter(self.formater)

        # 将两个处理器(输出渠道)添加到日志器中
        # 这样，当日志器记录日志时，消息会同时发送给这两个处理器
        self.logger.addHandler(self.filelogger)
        self.logger.addHandler(self.console)

# 创建一个 Logger 类的实例，并立即获取其内部的 logger 属性。
# 这样，在其他模块中通过 `from main import logger` 导入的就是一个配置好的日志器对象.
logger = Logger().logger
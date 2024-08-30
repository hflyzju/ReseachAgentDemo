import logging
from logging.handlers import RotatingFileHandler
import os

# 日志初始化函数
def init_logging(log_dir, log_filename="app.log", max_log_size=1024*1024*5, backup_count=5):
    # 如果日志文件夹不存在，创建日志文件夹
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 定义日志文件的完整路径
    log_file_path = os.path.join(log_dir, log_filename)

    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # 设置日志记录的等级

    # 创建一个handler，用于写入日志文件
    file_handler = RotatingFileHandler(log_file_path, maxBytes=max_log_size, backupCount=backup_count)
    file_handler.setLevel(logging.INFO)  # 设置handler级别

    # 创建一个handler，用于将日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 设置handler级别

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)



if __name__ == '__main__':
    # 使用示例
    # 初始化日志配置
    log_directory = "log"
    init_logging(log_directory)

    # 在其他模块中使用
    # 仅需导入logging模块并获取root logger即可
    import logging
    logger = logging.getLogger()

    # 记录日志
    logger.info("This is an info message")
    logger.error("This is an error message")


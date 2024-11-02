# bin/custom_log.py
import logging
import datetime
import pathlib
import asyncio
from typing import Any, Dict


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'pastime'):
            record.pastime = 'N/A'
        return super().format(record)


def setup_custom_logger(name):
    formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pastime)s')

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)  # 只显示 WARNING 及以上级别的日志

    # 文件处理器
    log_folder = pathlib.Path("log")
    log_folder.mkdir(exist_ok=True)  # 确保 log 文件夹存在
    file_handler = logging.FileHandler(log_folder / "true_log.txt", encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)  # 记录所有级别的日志

    logger = logging.getLogger(name)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger


def handle_exception(_: asyncio.AbstractEventLoop, context: Dict[str, Any]) -> None:
    # 获取异常信息
    exception = context.get("exception")
    message = context.get("message", "Unhandled exception")

    # 记录异常信息
    if exception or message != "Unhandled exception":
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        error_log_file = pathlib.Path(f"log/error_log_{timestamp}.txt")
        with open(error_log_file, 'a', encoding='utf-8') as file:
            file.write(f"{timestamp} - {message}\n")
            if exception:
                file.write(f"{timestamp} - {exception}\n")

        # 打印异常信息到控制台
        logging.error(f"{timestamp} - {message}")
        if exception:
            logging.error(f"{timestamp} - {exception}")


# 设置全局异常处理器
loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_exception)

# def sanitize_filename(filename):
#     # 替换非法字符为下划线
#     return re.sub(r'[<>:"/\\|?*]', '_', filename)
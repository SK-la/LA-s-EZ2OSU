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
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

def handle_exception(_: asyncio.AbstractEventLoop, context: Dict[str, Any]) -> None:
    # 获取异常信息
    exception = context.get("exception")
    message = context.get("message", "Unhandled exception")

    # 记录异常信息
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    error_log_file = pathlib.Path(f"error_log_{timestamp}.txt")
    with open(error_log_file, 'a', encoding='utf-8') as file:
        file.write(f"{timestamp} - {message}\n")
        if exception:
            file.write(f"{exception}\n")

    # 打印异常信息到控制台
    logging.error(f"{timestamp} - {message}")
    if exception:
        logging.error(exception)

# 设置全局异常处理器
loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_exception)

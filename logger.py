import logging
import os
import functools
import time
from constants import Constants

class Logger:
    """
    Класс для логирования с поддержкой файлов.
    Логи записываются только в файл log.txt, без вывода в консоль.
    """
    _logger = None
    _LOG_NAME = Constants.LOG_NAME

    @classmethod
    def _initialize_logger(cls):
        if cls._logger is not None:
            return cls._logger

        log_dir = os.path.dirname(Constants.CACHE_FILE)
        os.makedirs(log_dir, exist_ok=True)
        cls.log_path = os.path.join(log_dir, cls._LOG_NAME)

        cls._logger = logging.getLogger('finx')
        cls._logger.setLevel(logging.DEBUG)
        cls._logger.handlers = []

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = logging.FileHandler(cls.log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        cls._logger.addHandler(file_handler)
        return cls._logger

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._initialize_logger()
        return cls._logger

    @staticmethod
    def debug(message):
        Logger.get_logger().debug(message)

    @staticmethod
    def info(message):
        Logger.get_logger().info(message)

    @staticmethod
    def warning(message):
        Logger.get_logger().warning(message)

    @staticmethod
    def error(message, exc_info=False):
        Logger.get_logger().error(message, exc_info=exc_info)

    @staticmethod
    def critical(message, exc_info=False):
        Logger.get_logger().critical(message, exc_info=exc_info)

    @classmethod
    def clear_logs(cls):
        """Очищает файл логов корректно и безопасно."""
        if True:
            log_path = cls.log_path
            
            # Закрываем все handlers перед очисткой
            if cls._logger is not None:
                for handler in cls._logger.handlers[:]:
                    handler.close()
                    cls._logger.removeHandler(handler)
            
            # Удаляем файл если существует
            if os.path.exists(log_path):
                os.remove(log_path)
            
            # Переинициализируем логгер чтобы создал новый файл
            cls._logger = None
            cls._initialize_logger()
            
            cls.info("Логи очищены и переинициализированы")


def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        start_time = time.perf_counter() 
        
        Logger.debug(f"Запуск '{func_name}': args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.perf_counter() - start_time
            Logger.info(f"'{func_name}' за {execution_time:.2f}с. Результат: {result}")
            return result
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            Logger.error(f"Ошибка в '{func_name}' ({execution_time:.2f}с): {str(e)}", exc_info=True)
            raise
    return wrapper

def log_execution_simple(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        try:
            result = func(*args, **kwargs)
            Logger.info(f"'{func_name}' -> {result}")
            return result
        except Exception as e:
            Logger.error(f"'{func_name}' -> Ошибка: {str(e)}", exc_info=True)
            raise
    return wrapper

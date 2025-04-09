import logging     # Стандартная библиотека Python для логирования
import os         # Библиотека для работы с операционной системой и файлами
from datetime import datetime  # Библиотека для работы с датой и временем


class AppLogger:
    """
    Класс для логирования работы приложения.

    Возможности:
    - Сохранение логов в файлы (с именем в формате текущей даты).
    - Вывод логов в консоль.
    - Поддержка разных уровней логирования (debug, info, warning, error).
    - Форматирование сообщений с временными метками.
    """

    def __init__(self):
        """
        Инициализация системы логирования.

        Настраивает директорию хранения логов, форматирование сообщений
        и обработчики для записи в файл и вывода в консоль.
        """
        # Директория для хранения лог-файлов
        self.logs_dir = "logs"
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

        # Формирование имени файла с логами
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.logs_dir, f"chat_app_{current_date}.log")

        # Настройка формата сообщений
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Обработчик для записи логов в файл
        file_handler = logging.FileHandler(
            log_file,
            encoding='utf-8'  # Кодировка для поддержки Unicode
        )
        file_handler.setFormatter(formatter)

        # Обработчик для вывода логов в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Создание основного логгера приложения
        self.logger = logging.getLogger('ChatApp')
        self.logger.setLevel(logging.DEBUG)  # Уровень логирования (все сообщения)
        self.logger.addHandler(file_handler)  # Добавление вывода в файл
        self.logger.addHandler(console_handler)  # Добавление вывода в консоль

    def info(self, message: str):
        """
        Логирование информационного сообщения.

        Используется для записи обычных событий, передачи статуса приложения.

        Args:
            message (str): Текст сообщения.
        """
        self.logger.info(message)

    def error(self, message: str, exc_info=None):
        """
        Логирование ошибки.

        Записывает критические ошибки и исключения с подробной информацией.

        Args:
            message (str): Текст сообщения об ошибке.
            exc_info: Информация об исключении (например, стек вызовов).
                      Если `exc_info=True`, добавляет полное окно стека.
        """
        self.logger.error(message, exc_info=exc_info)

    def debug(self, message: str):
        """
        Логирование отладочного сообщения.

        Используется для записи данных, полезных при разработке и тестировании.

        Args:
            message (str): Текст отладочного сообщения.
        """
        self.logger.debug(message)

    def warning(self, message: str):
        """
        Логирование предупреждения.

        Используется для записи сообщений о потенциальных проблемах.

        Args:
            message (str): Текст предупреждающего сообщения.
        """
        self.logger.warning(message)

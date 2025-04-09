import psutil      # Библиотека для мониторинга системных ресурсов (CPU, память, потоки)
import time        # Библиотека для работы с временными метками и измерения интервалов
from datetime import datetime  # Библиотека для работы с датой и временем


class PerformanceMonitor:
    """
    Класс для мониторинга производительности приложения.

    Функционал:
    - Отслеживание использования CPU
    - Отслеживание использования памяти
    - Количество активных потоков
    - Время работы приложения
    - Проверка состояния системы
    """

    def __init__(self):
        """
        Инициализация монитора производительности.

        Настраивает:
        - Время старта мониторинга
        - Историю метрик
        - Процесс для анализа
        - Пороговые значения для метрик
        """
        self.start_time = time.time()  # Время запуска для расчёта uptime
        self.metrics_history = []      # История собранных метрик
        self.process = psutil.Process()  # Текущий процесс приложения

        # Пороговые значения для анализа производительности
        self.thresholds = {
            'cpu_percent': 80.0,     # Максимальная загрузка CPU (%)
            'memory_percent': 75.0,  # Максимальное использование RAM (%)
            'thread_count': 50       # Максимальное количество потоков
        }

    def get_metrics(self) -> dict:
        """
        Получение текущих метрик производительности.

        Returns:
            dict: Текущие показатели (CPU, память, потоки, uptime).
            Если возникает ошибка — возвращается словарь с ключом 'error'.
        """
        try:
            # Сбор данных о производительности
            metrics = {
                'timestamp': datetime.now(),      # Время замера
                'cpu_percent': self.process.cpu_percent(),  # Использование CPU
                'memory_percent': (
                    self.process.memory_percent()  # Использование памяти
                ),
                'thread_count': len(
                    self.process.threads()  # Количество потоков
                ),
                'uptime': time.time() - self.start_time  # Время работы
            }

            # Добавление данных в историю метрик
            self.metrics_history.append(metrics)

            # Лимит хранения истории (последние 1000 записей)
            if len(self.metrics_history) > 1000:
                self.metrics_history.pop(0)

            return metrics

        except Exception as e:
            # Возврат информации об ошибке сбора метрик
            return {
                'error': str(e),
                'timestamp': datetime.now()
            }

    def check_health(self) -> dict:
        """
        Проверка состояния системы.

        Сравнивает текущие метрики с пороговыми значениями и определяет
        потенциальные проблемы с производительностью.

        Returns:
            dict: Статус системы: 'healthy', 'warning' или 'error'.
            Содержит список предупреждений при необходимости.
        """
        metrics = self.get_metrics()  # Получение текущих метрик

        # Если была ошибка при сборе метрик
        if 'error' in metrics:
            return {'status': 'error', 'error': metrics['error']}

        # Инициализация состояния системы
        health_status = {
            'status': 'healthy',
            'warnings': [],
            'timestamp': metrics['timestamp']
        }

        # Проверка CPU
        if metrics['cpu_percent'] > self.thresholds['cpu_percent']:
            health_status['warnings'].append(
                f"High CPU usage: {metrics['cpu_percent']}%"
            )
            health_status['status'] = 'warning'

        # Проверка памяти
        if metrics['memory_percent'] > self.thresholds['memory_percent']:
            health_status['warnings'].append(
                f"High memory usage: {metrics['memory_percent']}%"
            )
            health_status['status'] = 'warning'

        # Проверка потоков
        if metrics['thread_count'] > self.thresholds['thread_count']:
            health_status['warnings'].append(
                f"High thread count: {metrics['thread_count']}"
            )
            health_status['status'] = 'warning'

        return health_status

    def get_average_metrics(self) -> dict:
        """
        Расчёт средних значений метрик за всю историю наблюдений.

        Returns:
            dict: Словарь со средними значениями CPU, памяти, потоков,
                  либо сообщение об отсутствии данных.
        """
        # Проверка наличия данных для расчёта
        if not self.metrics_history:
            return {"error": "No metrics available"}

        # Вычисление средних метрик
        avg_metrics = {
            'avg_cpu': sum(
                m['cpu_percent'] for m in self.metrics_history
            ) / len(self.metrics_history),
            'avg_memory': sum(
                m['memory_percent'] for m in self.metrics_history
            ) / len(self.metrics_history),
            'avg_threads': sum(
                m['thread_count'] for m in self.metrics_history
            ) / len(self.metrics_history),
            'samples_count': len(self.metrics_history)  # Количество замеров
        }

        return avg_metrics

    def log_metrics(self, logger) -> None:
        """
        Логирование текущих метрик и состояния системы.

        Записывает в лог:
        - Значения метрик производительности.
        - Предупреждения на основе пороговых значений.

        Args:
            logger: Экземпляр логгера для записи данных.
        """
        metrics = self.get_metrics()   # Текущие метрики
        health = self.check_health()   # Состояние системы

        # Логирование текущих метрик, если нет ошибок
        if 'error' not in metrics:
            logger.info(
                f"Performance metrics - "
                f"CPU: {metrics['cpu_percent']:.1f}%, "
                f"Memory: {metrics['memory_percent']:.1f}%, "
                f"Threads: {metrics['thread_count']}, "
                f"Uptime: {metrics['uptime']:.0f}s"
            )

        # Логирование предупреждений о производительности
        if health['status'] == 'warning':
            for warning in health['warnings']:
                logger.warning(f"Performance warning: {warning}")

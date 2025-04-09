import time                  # Библиотека для работы с временными метками и измерения интервалов
from datetime import datetime  # Библиотека для работы с датой и временем в удобном формате


class Analytics:
    """
    Класс для сбора и анализа данных об использовании приложения.

    Отслеживает различные метрики:
    - Статистику по моделям
    - Время ответа
    - Использование токенов
    - Длину сообщений
    - Общую длительность сессии
    """

    def __init__(self, cache):
        """
        Инициализация системы аналитики.

        Args:
            cache (ChatCache): Класс для работы с базой данных.

        Создаются структуры для хранения данных:
        - Времени начала сессии
        - Статистики использования моделей
        - Истории сообщений
        """
        self.cache = cache
        self.start_time = time.time()
        self.model_usage = {}
        self.session_data = []

        # Загрузка исторических данных из базы
        self._load_historical_data()

    def _load_historical_data(self):
        """
        Загрузка исторических данных из базы.
        Обновляет статистику и историю сообщений из сохранённых данных.
        """
        history = self.cache.get_analytics_history()

        for record in history:
            timestamp, model, message_length, response_time, tokens_used = (
                record
            )

            # Обновление статистики моделей
            if model not in self.model_usage:
                self.model_usage[model] = {'count': 0, 'tokens': 0}
            self.model_usage[model]['count'] += 1
            self.model_usage[model]['tokens'] += tokens_used

            # Добавление сообщения в историю сессии
            self.session_data.append({
                'timestamp': datetime.strptime(timestamp,
                                               '%Y-%m-%d %H:%M:%S.%f'),
                'model': model,
                'message_length': message_length,
                'response_time': response_time,
                'tokens_used': tokens_used
            })

    def track_message(self, model, message_length, response_time, tokens_used):
        """
        Отслеживание метрик для одного сообщения.

        Сохраняет общую статистику и историю сообщений.

        Args:
            model (str): Идентификатор использованной модели.
            message_length (int): Длина сообщения в символах.
            response_time (float): Время ответа в секундах.
            tokens_used (int): Количество использованных токенов.
        """
        timestamp = datetime.now()

        # Сохранение данных сообщения в базе
        self.cache.save_analytics(
            timestamp, model, message_length, response_time, tokens_used
        )

        # Добавление новой модели в статистику, если модель ещё не использована
        if model not in self.model_usage:
            self.model_usage[model] = {'count': 0, 'tokens': 0}

        # Обновление статистики модели
        self.model_usage[model]['count'] += 1
        self.model_usage[model]['tokens'] += tokens_used

        # Добавление сообщения в историю
        self.session_data.append({
            'timestamp': timestamp,
            'model': model,
            'message_length': message_length,
            'response_time': response_time,
            'tokens_used': tokens_used
        })

    def get_statistics(self):
        """
        Возвращает общую статистику использования приложения.

        Returns:
            dict: Расчётные данные, включая:
                - Количество сообщений
                - Использованные токены
                - Длительность сессии
                - Средние метрики
                - Статистика по моделям.
        """
        # Расчёт длительности сессии
        total_time = time.time() - self.start_time

        # Подсчёт токенов и сообщений
        total_tokens = sum(model['tokens']
                           for model in self.model_usage.values())
        total_messages = sum(model['count']
                             for model in self.model_usage.values())

        # Формирование статистики
        return {
            'total_messages': total_messages,
            'total_tokens': total_tokens,
            'session_duration': total_time,

            # Средних сообщений в минуту, избегая деления на малое значение
            'messages_per_minute': (
                (total_messages * 60) / total_time if total_time > 0 else 0),

            # Среднее количество токенов на сообщение
            'tokens_per_message': (
                total_tokens / total_messages if total_messages > 0 else 0
            ),

            # Детальная статистика использования моделей
            'model_usage': self.model_usage
        }

    def export_data(self):
        """
        Экспорт собранных данных сессии.

        Returns:
            list: История сообщений с временными метками,
                  моделями и метриками.
        """
        return self.session_data

    def clear_data(self):
        """
        Полная очистка данных аналитики.

        Сбрасывает:
        - Статистику использования моделей.
        - Историю сообщений.
        - Время начала текущей сессии.
        """
        self.model_usage.clear()  # Очистка статистики
        self.session_data.clear()  # Очистка истории сообщений
        self.start_time = time.time()  # Перезапуск времени сессии

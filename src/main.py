import flet as ft  # Фреймворк для создания кроссплатформенных приложений с современным UI
from api.openrouter import OpenRouterClient  # Клиент для взаимодействия с AI API через OpenRouter
from ui.styles import AppStyles  # Модуль с настройками стилей интерфейса
from ui.components import MessageBubble, ModelSelector, AuthWindow  # Компоненты пользовательского интерфейса
from utils.cache import ChatCache  # Модуль для кэширования истории чата
from utils.logger import AppLogger  # Модуль для логирования работы приложения
from utils.analytics import Analytics  # Модуль для сбора и анализа статистики использования
from utils.monitor import PerformanceMonitor  # Модуль для мониторинга производительности
import random
import time  # Библиотека для работы с временными метками
import json  # Библиотека для работы с JSON-данными
from datetime import datetime  # Класс для работы с датой и временем
import os  # Библиотека для работы с операционной системой
import webbrowser  # Библиотека для работы с веб-браузерами


class ChatApp:
    """
    Основной класс приложения чата с аутентификацией.
    Управляет всей логикой работы приложения, включая UI и
    взаимодействие с API.
    """

    def __init__(self):
        """
        Базовая инициализация компонентов приложения.
        Полная инициализация происходит после успешной аутентификации.
        """
        # Системные компоненты
        self.cache = ChatCache()
        self.logger = AppLogger()

        # Переменные, связанные с API
        self.api_client = None
        self.analytics = None
        self.monitor = None

        # UI-компоненты
        self.page = None
        self.auth_window = None
        self.main_window = None
        self.balance_text = None
        self.chat_history = None
        self.message_input = None
        self.model_dropdown = None

        # Папка для экспорта истории чата
        self.exports_dir = "exports"
        os.makedirs(self.exports_dir, exist_ok=True)

    @staticmethod
    def generate_pin() -> str:
        """
        Генерация 4-значного PIN-кода.

        Returns:
            str: Cлучайный 4-значный PIN-код.
        """
        return ''.join(random.choices('0123456789', k=4))

    async def validate_api_key(self, key: str) -> bool:
        """
        Проверка валидности API-ключа через запрос баланса.

        Args:
            key (str): Переданный API-ключ.

        Returns:
            bool: True, если ключ валиден, False в противном случае.
        """
        try:
            temp_client = OpenRouterClient()
            temp_client.api_key = key
            balance = temp_client.get_balance()
            return balance and balance != "Ошибка"
        except Exception as e:
            self.logger.error(f"Ошибка валидации ключа: {e}")
            return False

    def init_app(self, api_key: str) -> bool:
        """
        Полная инициализация приложения после аутентификации.

        Args:
            api_key (str): Переданный API-ключ.

        Returns:
            bool: True, если инициализация прошла успешно.
        """
        try:
            self.api_client = OpenRouterClient()
            self.api_client.api_key = api_key
            self.analytics = Analytics(self.cache)
            self.monitor = PerformanceMonitor()

            # Получение списка моделей для dropdown
            models = self.api_client.get_models()
            self.model_dropdown = ModelSelector(models=models)

            # Создание текста "Баланс"
            self.balance_text = ft.Text(
                "Баланс: Загрузка...",
                **AppStyles.BALANCE_TEXT
            )
            self.update_balance()
            return True
        except Exception as e:
            self.logger.error(f"Ошибка инициализации приложения: {e}")
            return False

    def update_balance(self):
        """Обновление отображения баланса API."""
        try:
            balance = self.api_client.get_balance()
            self.balance_text.value = f"Баланс: {balance}"
            self.balance_text.color = ft.Colors.GREEN_400
        except Exception as e:
            self.balance_text.value = "Баланс: н/д"
            self.balance_text.color = ft.Colors.RED_400
            self.logger.error(f"Ошибка обновления баланса: {e}")

    def load_chat_history(self):
        """Загрузка истории чата из локального кэша."""
        try:
            history = self.cache.get_chat_history()
            for msg in reversed(history):
                _, model, user_message, ai_response, timestamp, tokens = msg
                self.chat_history.controls.extend([
                    MessageBubble(message=user_message, is_user=True),
                    MessageBubble(message=ai_response, is_user=False),
                ])
        except Exception as e:
            self.logger.error(f"Ошибка загрузки истории чата: {e}")

    async def send_message_click(self, _):
        """
        Асинхронная отправка сообщения от пользователя через API.

        Args:
            _: Событие клика кнопки.
        """
        if not self.message_input.value:
            return

        try:
            # Обновляем состояние перед отправкой
            self.message_input.border_color = ft.Colors.BLUE_400
            self.page.update()

            start_time = time.time()
            user_message = self.message_input.value
            self.message_input.value = ""
            self.page.update()

            # Отображение сообщения пользователя в чате
            self.chat_history.controls.append(
                MessageBubble(message=user_message, is_user=True)
            )

            # Показ индикатора загрузки
            loading = ft.ProgressRing()
            self.chat_history.controls.append(loading)
            self.page.update()

            # Выполнение запроса к API
            response = await self.api_client.send_message(
                user_message, self.model_dropdown.value
            )
            self.chat_history.controls.remove(loading)

            # Обработка ответа от API
            if "error" in response:
                response_text = f"Ошибка: {response['error']}"
                tokens_used = 0
                self.logger.error(f"Ошибка API: {response['error']}")
            else:
                response_text = response["choices"][0]["message"]["content"]
                tokens_used = response.get("usage", {}).get("total_tokens", 0)

            # Сохранение сообщений в кэш
            self.cache.save_message(
                model=self.model_dropdown.value,
                user_message=user_message,
                ai_response=response_text,
                tokens_used=tokens_used,
            )

            # Добавление ответа ИИ в историю чата
            self.chat_history.controls.append(
                MessageBubble(message=response_text, is_user=False)
            )

            # Сохранение статистики
            response_time = time.time() - start_time
            self.analytics.track_message(
                model=self.model_dropdown.value,
                message_length=len(user_message),
                response_time=response_time,
                tokens_used=tokens_used,
            )

            self.monitor.log_metrics(self.logger)
            self.page.update()
        except Exception as e:
            self.logger.error(f"Ошибка отправки сообщения: {e}")
            self.message_input.border_color = ft.Colors.RED_500
            self.show_error_snack(str(e))

    def show_error_snack(self, message: str):
        """
        Показ уведомления об ошибке.

        Args:
            message (str): Текст сообщения.
        """
        snack = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.RED_500),
            bgcolor=ft.Colors.GREY_900,
            duration=5000,
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    async def show_analytics(self, _):
        """
        Отображение статистики использования приложения.

        Args:
            _: Событие клика кнопки.
        """
        stats = self.analytics.get_statistics()
        dialog = ft.AlertDialog(
            title=ft.Text("Аналитика"),
            content=ft.Column([
                ft.Text(f"Всего сообщений: {stats['total_messages']}"),
                ft.Text(f"Всего токенов: {stats['total_tokens']}"),
                ft.Text(
                    f"Среднее токенов/сообщение: {stats['tokens_per_message']:.2f}"
                ),
                ft.Text(
                    f"Сообщений в минуту: {stats['messages_per_minute']:.2f}"
                )
            ]),
            actions=[
                ft.TextButton("Закрыть", on_click=lambda e: self.close_dialog(dialog)),
            ],
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    async def clear_history(self, _):
        """
        Очистка истории чата: удаление данных из кэша
        и обновление интерфейса.

        Args:
            _: Событие клика кнопки.
        """
        try:
            self.cache.clear_history()
            self.analytics.clear_data()
            self.chat_history.controls.clear()
            self.page.update()
        except Exception as e:
            self.logger.error(f"Ошибка очистки истории: {e}")
            self.show_error_snack(f"Ошибка очистки истории: {str(e)}")

    async def confirm_clear_history(self, _):
        """
        Отображение диалогового окна для подтверждения очистки истории.

        Args:
            _: Событие клика кнопки.
        """
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение удаления"),
            content=ft.Text(
                "Вы уверены? Это действие нельзя отменить!"
            ),
            actions=[
                ft.TextButton(
                    "Отмена",
                    on_click=lambda e: self.close_dialog(dialog)
                ),
                ft.TextButton(
                    "Очистить", on_click=self.clear_history
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    async def save_dialog(self, _):
        """
        Сохранение истории диалога в JSON файл в директорию экспорта.

        Args:
            _: Событие клика кнопки.
        """
        try:
            history = self.cache.get_chat_history()
            dialog_data = [{
                "timestamp": msg[4],
                "model": msg[1],
                "user_message": msg[2],
                "ai_response": msg[3],
                "tokens_used": msg[5]
            } for msg in history]

            filename = (
                f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            filepath = os.path.join(self.exports_dir, filename)

            # Сохранение данных в файл
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(
                    dialog_data,
                    f,
                    ensure_ascii=False,
                    indent=2,
                    default=str
                )

            # Уведомление о сохранении
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Диалог сохранен"),
                content=ft.Column([
                    ft.Text("Путь сохранения:"),
                    ft.Text(filepath, selectable=True,
                            weight=ft.FontWeight.BOLD),
                ]),
                actions=[
                    ft.TextButton(
                        "OK",
                        on_click=lambda _: self.close_dialog(dialog)
                    ),
                    ft.TextButton(
                        "Открыть папку",
                        on_click=lambda _: os.startfile(self.exports_dir),
                    ),
                ],
            )
            self.page.overlay.append(dialog)
            dialog.open = True
            self.page.update()

        except Exception as e:
            self.logger.error(f"Ошибка сохранения: {e}")
            self.show_error_snack(f"Ошибка сохранения: {str(e)}")

    def close_dialog(self, dialog):
        """
        Закрытие диалогового окна.

        Args:
            dialog: Диалоговое окно, которое требуется закрыть.
        """
        dialog.open = False
        self.page.update()
        if dialog in self.page.overlay:
            self.page.overlay.remove(dialog)

    def create_main_layout(self):
        """
        Создание основного макета приложения
        с элементами управления.

        Returns:
            ft.Column: Основной макет интерфейса.
        """
        if not self.model_dropdown:
            raise ValueError("Model dropdown не инициализирован")

        # Создание текстового поля для ввода сообщения
        self.message_input = ft.TextField(**AppStyles.MESSAGE_INPUT)

        # Лист с историей чата
        self.chat_history = ft.ListView(**AppStyles.CHAT_HISTORY)

        # Загрузка кэшированной истории чата
        self.load_chat_history()

        # Создание кнопки "Сохранить"
        save_button = ft.ElevatedButton(
            text="Сохранить",
            on_click=self.save_dialog,
            **AppStyles.SAVE_BUTTON
        )

        # Создание кнопки "Очистить"
        clear_button = ft.ElevatedButton(
            text="Очистить",
            on_click=self.confirm_clear_history,
            **AppStyles.CLEAR_BUTTON
        )

        # Создание кнопки "Отправить"
        send_button = ft.ElevatedButton(
            text="Отправить",
            on_click=self.send_message_click,
            **AppStyles.SEND_BUTTON
        )

        # Создание кнопки "Аналитика"
        analytics_button = ft.ElevatedButton(
            text="Аналитика",
            on_click=self.show_analytics,
            **AppStyles.ANALYTICS_BUTTON
        )

        # Создание кнопки "Пополнить"
        replenish_button = ft.ElevatedButton(
            text=AppStyles.REPLENISH_BUTTON["text"],  # Текст кнопки из стилей
            on_click=lambda _: webbrowser.open("https://openrouter.ai/settings/credits"),  # Ссылка на пополнение
            style=AppStyles.REPLENISH_BUTTON["style"],  # Применение стилей из AppStyles
            tooltip=AppStyles.REPLENISH_BUTTON["tooltip"],  # Подсказка
            width=AppStyles.REPLENISH_BUTTON["width"],  # Ширина кнопки
            height=AppStyles.REPLENISH_BUTTON["height"],  # Высота кнопки
        )

        # Контейнер для текста баланса с кнопкой "Пополнить"
        balance_container = ft.Row(
            controls=[
                self.balance_text,  # Отображение текста баланса
                replenish_button,  # Кнопка "Пополнить"
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Размещение элементов с пробелом между ними
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Вертикальное выравнивание
        )

        # Контейнер для списка моделей
        model_selection = ft.Column(
            controls=[
                self.model_dropdown.search_field,  # Поле ввода фильтра списка моделей
                self.model_dropdown,  # Выпадающий список моделей
                balance_container,  # Баланс и кнопка пополнения
            ],
            **AppStyles.MODEL_SELECTION_COLUMN
        )

        # Контейнер для кнопок управления
        control_buttons = ft.Row(
            controls=[save_button, analytics_button, clear_button],  # Кнопки управления
            **AppStyles.CONTROL_BUTTONS_ROW
        )

        # Строка ввода сообщения и кнопки "Отправить"
        input_row = ft.Row(
            controls=[self.message_input, send_button],  # Поле для ввода текста + кнопка
            **AppStyles.INPUT_ROW
        )

        # Колонка управления
        controls_column = ft.Column(
            controls=[input_row, control_buttons],  # Добавляем строку ввода и кнопки управления
            **AppStyles.CONTROLS_COLUMN
        )

        # Возвращаем итоговый интерфейс
        return ft.Column(
            controls=[
                model_selection,  # Выбор модели
                self.chat_history,  # История чата
                controls_column,  # Управляющая колонка
            ],
            **AppStyles.MAIN_COLUMN
        )

    async def handle_auth(self, value):
        """
        Обработка логики аутентификации (API-ключ или PIN).

        Args:
            value (str): Введённое пользователем значение.
        """
        stored_key, stored_pin = self.cache.get_auth_data()

        # Впервые выполняем вход
        if not stored_key:
            is_valid = await self.validate_api_key(value)
            if is_valid:
                pin = self.generate_pin()
                self.cache.save_auth_data(value, pin)
                await self.show_pin_dialog(pin)
                if self.init_app(value):
                    self.show_main_window()
            else:
                # Отображение сообщения об ошибке при неверном ключе API
                self.auth_window.error_text.value = "Неверный ключ API"
                self.auth_window.error_text.visible = True
                self.auth_window.update()  # Обновляем AuthWindow для отображения ошибки
        else:
            # Проверка введённого PIN-кода
            if value == stored_pin:
                if self.init_app(stored_key):
                    self.show_main_window()
            else:
                # Отображение ошибки, если PIN неверный
                self.auth_window.error_text.value = "Неверный PIN"
                self.auth_window.error_text.visible = True
                self.auth_window.update()  # Обновляем AuthWindow для отображения ошибки

    def handle_reset(self):
        """
        Обработчик сброса настроек входа и очищения данных авторизации.
        """
        # Шаг 1: Очищаем данные аутентификации
        self.cache.clear_auth_data()

        # Шаг 2: Настраиваем окно аутентификации для ввода API-ключа
        self.auth_window.input_field.label = "Введите API ключ"
        self.auth_window.input_field.value = ""
        self.auth_window.error_text.visible = False  # Скрываем ошибки (если есть)

        # Шаг 3: Обновляем видимость окон
        self.auth_window.visible = True  # Делаем окно авторизации видимым
        self.main_window.visible = False  # Делаем основное окно скрытым

        # Шаг 4: Обновляем интерфейс
        self.page.clean()  # Полностью очищаем страницу
        self.page.add(self.auth_window, self.main_window)  # Добавляем обновленные элементы
        self.page.update()

    async def show_pin_dialog(self, pin):
        """
        Отображение диалога с информацией о PIN-коде.

        Args:
            pin (str): Сгенерированный PIN-код для пользователя.
        """
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("PIN-код создан"),
            content=ft.Column([
                ft.Text("Запомните ваш PIN-код для входа:"),
                ft.Text(pin, size=24, weight=ft.FontWeight.BOLD)
            ]),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.close_dialog(dialog)),
            ]
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def show_main_window(self):
        """
        Переход от окна авторизации к основному интерфейсу приложения.
        """
        self.auth_window.visible = False
        self.main_window.visible = True
        self.main_window.content = self.create_main_layout()
        self.page.update()

    async def main(self, page: ft.Page):
        """
        Основной метод запуска страницы.

        Args:
            page: Переданная страница интерфейса Flet.
        """
        self.page = page
        for key, value in AppStyles.PAGE_SETTINGS.items():
            setattr(page, key, value)
        AppStyles.set_window_size(page)

        # Создание окон
        self.auth_window = AuthWindow(
            on_submit=self.handle_auth,
            on_reset=self.handle_reset,
        )
        self.main_window = ft.Container(visible=False)

        # Проверка сохранённых данных аутентификации
        stored_key, _ = self.cache.get_auth_data()
        if stored_key:
            self.auth_window.input_field.label = "Введите PIN"

        page.add(self.auth_window, self.main_window)
        self.logger.info("Приложение запущено")

    @staticmethod
    def main_entry():
        """Точка входа в приложение"""
        app = ChatApp()
        ft.app(target=app.main)


if __name__ == "__main__":
    ChatApp.main_entry()

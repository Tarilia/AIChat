import flet as ft  # Фреймворк для создания пользовательского интерфейса
from src.ui.styles import AppStyles  # Импорт стилей приложения


class MessageBubble(ft.Container):
    """
    Компонент "пузырька" сообщения в чате.

    Отображает сообщения пользователя и AI с разными стилями, позиционированием.
    """

    def __init__(self, message: str, is_user: bool):
        # Инициализация базового класса Container
        super().__init__()

        # Отступы внутри "пузырька"
        self.padding = 10

        # Закругленные края пузырька
        self.border_radius = 10

        # Настройка фона:
        # - Синий цвет, если сообщение от пользователя
        # - Серый цвет, если сообщение от AI
        self.bgcolor = (
            ft.Colors.BLUE_700 if is_user else ft.Colors.GREY_700
        )

        # Выравнивание пузырька:
        # - Справа – от пользователя
        # - Слева – от AI
        self.alignment = (
            ft.alignment.center_right if is_user
            else ft.alignment.center_left
        )

        # Внешние отступы (между пузырьками):
        # - Пользователь: большой отступ слева
        # - AI: большой отступ справа
        # - Небольшие отступы сверху и снизу
        self.margin = ft.margin.only(
            left=50 if is_user else 0,
            right=0 if is_user else 50,
            top=5,
            bottom=5
        )

        # Текст сообщения внутри пузырька
        self.content = ft.Column(
            controls=[
                ft.Text(
                    value=message,          # Исходный текст передается сюда
                    color=ft.Colors.WHITE,  # Белый цвет текста
                    size=16,                # Размер шрифта
                    selectable=True,        # Дает возможность выделить текст
                    weight=ft.FontWeight.W_400  # Толщина шрифта: нормальная
                )
            ],
            tight=True  # Плотное расположение элементов
        )


class ModelSelector(ft.Dropdown):
    """
    Выпадающий список для выбора AI модели с дополнительной функцией поиска.

    Args:
        models (list): Список доступных моделей в формате:
                      [{"id": "model-id", "name": "Model Name"}, ...]
    """

    def __init__(self, models: list):
        # Инициализация базового класса Dropdown
        super().__init__()

        # Применение стилей для выпадающего списка из преднастроек
        for key, value in AppStyles.MODEL_DROPDOWN.items():
            setattr(self, key, value)

        # Удобный текст для подсказки
        self.label = None  # Убираем метку над полем
        self.hint_text = "Выбор модели"  # Надпись внутри

        # Создание опций (моделей) на основе входящего списка
        self.options = [
            ft.dropdown.Option(
                key=model['id'],    # Уникальный идентификатор модели
                text=model['name']  # Название модели
            ) for model in models
        ]

        # Сохранение полного списка опций для поиска
        self.all_options = self.options.copy()

        # Установка начального значения (первая модель в списке)
        self.value = models[0]['id'] if models else None

        # Поле поиска, для фильтрации моделей в выпадающем списке
        self.search_field = ft.TextField(
            on_change=self.filter_options,  # Вызывается при изменении текста
            hint_text="Поиск модели",      # Подсказка внутри поля
            **AppStyles.MODEL_SEARCH_FIELD  # Применение стилей
        )

    def filter_options(self, e):
        """
        Фильтрация списка моделей на основе текста из поля поиска.

        Args:
            e: Событие изменения текста в поле поиска.
        """
        # Получаем текст из поля поиска в нижнем регистре
        search_text = (
            self.search_field.value.lower()
            if self.search_field.value else ""
        )

        # Если строка поиска пуста, возвращаем весь список
        if not search_text:
            self.options = self.all_options
        else:
            # Фильтруем список по названию модели или её идентификатору
            self.options = [
                opt for opt in self.all_options
                if search_text in opt.text.lower()
                or search_text in opt.key.lower()
            ]

        # Обновляем интерфейс (выпадающий список)
        e.page.update()


class AuthWindow(ft.UserControl):
    """
    Окно аутентификации для ввода API ключа.

    Args:
        on_submit (callable): Функция для обработки нажатия кнопки "Войти".
        on_reset (callable): Функция для обработки нажатия кнопки "Сбросить".
    """

    def __init__(self, on_submit=None, on_reset=None):
        # Инициализация базового класса UserControl
        super().__init__()
        self.on_submit = on_submit  # Событие на нажатие "Войти"
        self.on_reset = on_reset    # Событие на нажатие "Сбросить"
        self.visible = True         # Компонент видим по умолчанию

        # Поле для ввода API ключа
        self.input_field = ft.TextField(
            label="Введите API ключ",
            password=True,           # Скрывать вводимые данные
            can_reveal_password=True,  # Кнопка для показа/скрытия ввода
            **AppStyles.AUTH_INPUT    # Применение стилей
        )

        # Текст ошибки (по умолчанию скрыт)
        self.error_text = ft.Text(
            visible=False,          # Ошибка не видима по умолчанию
            color=ft.colors.RED_400  # Красный цвет текста для ошибок
        )

        # Кнопка подтверждения (ввод API ключа)
        self.submit_button = ft.ElevatedButton(
            text="Войти",
            on_click=self.handle_submit,
            **AppStyles.AUTH_BUTTON  # Применение стилей к кнопке
        )

        # Кнопка сброса настроек
        self.reset_button = ft.ElevatedButton(
            text="Сбросить",
            on_click=self.handle_reset,
            **AppStyles.AUTH_BUTTON  # Применение стилей к кнопке
        )

    def build(self):
        """
        Построение интерфейса окна аутентификации.
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Авторизация", **AppStyles.AUTH_TITLE
                    ),
                    self.input_field,        # Поле для ввода API ключа
                    self.error_text,         # Текст ошибки
                    ft.Row(                  # Кнопки управления
                        controls=[
                            self.submit_button,
                            self.reset_button
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            **AppStyles.AUTH_CONTAINER  # Применение стилей к контейнеру
        )

    async def handle_submit(self, _):
        """
        Асинхронный обработчик события нажатия кнопки "Войти".

        Args:
            _: параметр события кнопки, передается автоматически.
        """
        if self.on_submit:
            await self.on_submit(self.input_field.value)

    def handle_reset(self, _):
        """
        Обработчик события кнопки "Сбросить".

        Args:
            _: параметр события кнопки, передается автоматически.
        """
        if self.on_reset:
            self.on_reset()

import flet as ft  # Импортируем фреймворк Flet для создания пользовательского интерфейса


class AppStyles:
    """Константы стилей для пользовательского интерфейса приложения."""

    # Стили для окна авторизации
    AUTH_CONTAINER = {
        "width": 400,  # Ширина контейнера
        "padding": 20,  # Внутренние отступы контейнера
        "bgcolor": ft.colors.SURFACE_VARIANT,  # Цвет фона контейнера
        "border_radius": 10,  # Радиус скругления углов
        "alignment": ft.alignment.center  # Выравнивание содержимого контейнера по центру
    }

    # Стили заголовка в окне авторизации
    AUTH_TITLE = {
        "size": 24,  # Размер текста заголовка
        "weight": ft.FontWeight.BOLD,  # Жирное начертание текста
        "color": ft.colors.PRIMARY  # Основной цвет текста заголовка
    }

    # Стили текстового поля для ввода данных авторизации
    AUTH_INPUT = {
        "width": 300,  # Ширина текстового поля
        "border_color": ft.colors.BLUE_700,  # Цвет границы текстового поля
        "focused_border_color": ft.colors.BLUE_ACCENT,  # Цвет при фокусе на поле
        "cursor_color": ft.colors.BLUE_ACCENT,  # Цвет курсора в текстовом поле
        "text_size": 16  # Размер текста внутри поля
    }

    # Стили кнопки авторизации
    AUTH_BUTTON = {
        "width": 120,  # Ширина кнопки
        "height": 40,  # Высота кнопки
        "style": ft.ButtonStyle(
            # Цвет текста кнопки при разных состояниях
            color={
                ft.ControlState.DEFAULT: ft.colors.WHITE,  # По умолчанию
                ft.ControlState.HOVERED: ft.colors.BLUE_700,  # При наведении
            },
            # Цвет фона кнопки при разных состояниях
            bgcolor={
                ft.ControlState.DEFAULT: ft.colors.GREEN_700,  # По умолчанию
                ft.ControlState.HOVERED: ft.colors.GREEN_400,  # Наведение
            },
            # Внутренние отступы текста внутри кнопки
            padding=10
        )
    }

    # Общие настройки страницы приложения
    PAGE_SETTINGS = {
        "title": "AI Chat",  # Заголовок окна приложения
        "vertical_alignment": ft.MainAxisAlignment.CENTER,  # Вертикальное выравнивание
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,  # Горизонтальное выравнивание
        "padding": 20,  # Отступы от краев окна
        "bgcolor": ft.Colors.GREY_900,  # Темный цвет фона
        "theme_mode": ft.ThemeMode.DARK,  # Режим темной темы
    }

    # Настройки для контейнера истории чата
    CHAT_HISTORY = {
        "expand": True,  # Использовать все доступное пространство
        "spacing": 10,  # Отступ между сообщениями
        "height": 400,  # Фиксированная высота области чата
        "auto_scroll": True,  # Автоматическая прокрутка к новым сообщениям
        "padding": 20,  # Внутренние отступы контейнера
    }

    # Стили текстового поля для ввода сообщений
    MESSAGE_INPUT = {
        "width": 400,  # Ширина поля ввода
        "height": 50,  # Высота поля ввода
        "multiline": False,  # Ввод разрешен на одной строке
        "text_size": 16,  # Размер текста внутри поля
        "color": ft.Colors.WHITE,  # Цвет текста
        "bgcolor": ft.Colors.GREY_800,  # Цвет фона текстового поля
        "border_color": ft.Colors.BLUE_100,  # Цвет границы поля ввода
        "cursor_color": ft.Colors.WHITE,  # Цвет курсора
        "content_padding": 10,  # Расстояние между границей и текстом
        "border_radius": 8,  # Радиус скругления углов поля ввода
        "hint_text": "Введите сообщение здесь...",  # Подсказка для пустого поля
        "shift_enter": True,  # Комбинация Shift+Enter для отправки
    }

    # Кнопка отправки сообщений
    SEND_BUTTON = {
        "icon": ft.icons.SEND,  # Иконка кнопки
        "style": ft.ButtonStyle(
            color=ft.Colors.WHITE,  # Цвет текста кнопки
            bgcolor=ft.Colors.BLUE_700,  # Цвет фона кнопки
            padding=10,  # Внутренние отступы кнопки
        ),
        "tooltip": "Отправить сообщение",  # Всплывающая подсказка
        "height": 40,  # Высота кнопки
        "width": 130,  # Ширина кнопки
    }

    # Кнопка сохранения диалога
    SAVE_BUTTON = {
        "icon": ft.icons.SAVE,  # Иконка кнопки
        "style": ft.ButtonStyle(
            color=ft.Colors.WHITE,  # Цвет текста кнопки
            bgcolor=ft.Colors.BLUE_700,  # Цвет фона кнопки
            padding=10,  # Внутренние отступы кнопки
        ),
        "tooltip": "Сохранить диалог в файл",  # Всплывающая подсказка
        "width": 130,  # Ширина кнопки
        "height": 40,  # Высота кнопки
    }

    # Кнопка очистки истории чата
    CLEAR_BUTTON = {
        "icon": ft.icons.DELETE,  # Иконка кнопки
        "style": ft.ButtonStyle(
            color=ft.Colors.WHITE,  # Цвет текста кнопки
            bgcolor=ft.Colors.RED_700,  # Цвет фона кнопки
            padding=10,  # Внутренние отступы кнопки
        ),
        "tooltip": "Очистить историю чата",  # Всплывающая подсказка
        "width": 130,  # Ширина кнопки
        "height": 40,  # Высота кнопки
    }

    # Кнопка аналитики
    ANALYTICS_BUTTON = {
        "icon": ft.icons.ANALYTICS,  # Иконка
        "style": ft.ButtonStyle(
            color=ft.Colors.WHITE,  # Цвет текста
            bgcolor=ft.Colors.GREEN_700,  # Цвет фона
            padding=10,  # Внутренние отступы
        ),
        "tooltip": "Показать аналитику",  # Подсказка
        "width": 130,  # Ширина
        "height": 40,  # Высота
    }

    # Строка ввода с текстовым полем и кнопкой
    INPUT_ROW = {
        "spacing": 10,  # Расстояние между элементами
        "alignment": ft.MainAxisAlignment.SPACE_BETWEEN,  # Разделение на две стороны
        "width": 920,  # Общая ширина строки
    }

    # Строка с кнопками управления
    CONTROL_BUTTONS_ROW = {
        "spacing": 20,  # Расстояние между кнопками
        "alignment": ft.MainAxisAlignment.CENTER,  # Центровка кнопок
    }

    # Колонка с элементами управления
    CONTROLS_COLUMN = {
        "spacing": 20,  # Отступ между элементами
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,  # Центровка по горизонтали
    }

    # Главная колонка приложения
    MAIN_COLUMN = {
        "expand": True,  # Использовать всё пространство
        "spacing": 20,  # Отступ между элементами
        "alignment": ft.MainAxisAlignment.CENTER,  # Центровка по вертикали
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,  # Центровка по горизонтали
    }

    # Поле поиска модели
    MODEL_SEARCH_FIELD = {
        "width": 400,  # Ширина поля
        "border_radius": 8,  # Радиус углов
        "bgcolor": ft.Colors.GREY_900,  # Цвет фона поля
        "border_color": ft.Colors.GREY_700,  # Цвет границы поля
        "color": ft.Colors.WHITE,  # Цвет текста
        "content_padding": 10,  # Внутренний отступ текста
        "cursor_color": ft.Colors.WHITE,  # Цвет курсора
        "focused_border_color": ft.Colors.BLUE_400,  # Цвет границы при фокусе
        "focused_bgcolor": ft.Colors.GREY_800,  # Цвет фона при фокусе
        "hint_style": ft.TextStyle(
            color=ft.Colors.GREY_400,  # Цвет подсказки (hint)
            size=14,  # Размер текста подсказки
        ),
        "prefix_icon": ft.icons.SEARCH,  # Иконка поиска
        "height": 45,  # Высота поля
    }

    # Колонка выбора модели
    MODEL_SELECTION_COLUMN = {
        "spacing": 10,  # Расстояние между элементами в колонке
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,  # Центровка по горизонтали
        "width": 400,  # Фиксированная ширина колонки
    }

    # Выпадающий список для выбора модели
    MODEL_DROPDOWN = {
        "width": 400,  # Ширина списка
        "height": 45,  # Высота списка
        "border_radius": 8,  # Скругленные углы
        "bgcolor": ft.Colors.GREY_900,  # Цвет фона
        "border_color": ft.Colors.GREY_700,  # Цвет границ
        "color": ft.Colors.WHITE,  # Цвет текста внутри списка
        "content_padding": 10,  # Внутренний отступ текста
        "focused_border_color": ft.Colors.BLUE_400,  # Цвет границы при фокусе
        "focused_bgcolor": ft.Colors.GREY_800,  # Цвет фона при фокусе
    }

    # Пополнение баланса
    REPLENISH_BUTTON = {
        "text": "Пополнить",  # Текст кнопки
        "style": ft.ButtonStyle(
            color=ft.Colors.WHITE,  # Цвет текста
            bgcolor=ft.Colors.GREEN_700,  # Цвет фона
            padding=10,  # Внутренние отступы
        ),
        "tooltip": "Пополнить баланс",  # Подсказка
        "width": 130,  # Ширина кнопки
        "height": 40,  # Высота кнопки
    }

    # Контейнер для отображения баланса
    BALANCE_CONTAINER = {
        "padding": 10,  # Внутренние отступы
        "bgcolor": ft.Colors.GREY_900,  # Цвет фона
        "border_radius": 8,  # Скругление углов
        "border": ft.border.all(1, ft.Colors.GREY_700),  # Граница
    }

    # Текст отображения баланса
    BALANCE_TEXT = {
        "size": 16,  # Размер текста
        "color": ft.Colors.GREEN_400,  # Цвет текста
        "weight": ft.FontWeight.BOLD,  # Жирный шрифт
    }

    @staticmethod
    def set_window_size(page: ft.Page):
        """
        Устанавливает фиксированный размер окна приложения.

        Args:
            page (ft.Page): Объект страницы приложения.
        """
        page.window.width = 600  # Ширина окна
        page.window.height = 800  # Высота окна
        page.window.resizable = False  # Отключить изменение размеров

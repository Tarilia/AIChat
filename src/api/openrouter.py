import aiohttp  # Библиотека для реализации асинхронной работы с HTTP
import requests  # Библиотека для выполнения HTTP-запросов к API
from src.utils.logger import AppLogger  # Импорт собственного логгера для отслеживания работы


class OpenRouterClient:
    """
    Клиент для взаимодействия с OpenRouter API.

    OpenRouter предоставляет унифицированный доступ к различным языковым
    моделям (GPT, Claude и др.) через единый API интерфейс.
    """

    def __init__(self):
        """
        Инициализация клиента OpenRouter.
        """
        # Инициализация логгера для отслеживания работы клиента
        self.logger = AppLogger()

        # Инициализация базовых параметров
        self._api_key = None
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = None
        self.available_models = None

        # Логирование успешной инициализации клиента
        self.logger.info("OpenRouterClient initialized successfully")

    @property
    def api_key(self):
        """
        Получение API ключа.

        Returns:
            str: Текущий API ключ.
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        """
        Установка API ключа и настройка заголовков.

        Args:
            value (str): Новый API ключ.

        Raises:
            ValueError: Если API ключ пустой.
        """
        if not value:
            self.logger.error("API key cannot be empty")
            raise ValueError("API key cannot be empty")

        self._api_key = value
        self.headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }

        # Загрузка доступных моделей
        self.available_models = self.get_models()
        self.logger.info("API key set successfully")

    def get_models(self):
        """
        Получение списка доступных языковых моделей.

        Returns:
            list: Список моделей [{"id": "model-id", "name": "Model Name"}, ...]

        Note:
            При ошибках возвращается список базовых моделей.
        """
        if not self.headers:
            self.logger.error("Headers not initialized. Set API key first")
            return self._get_default_models()

        self.logger.debug("Fetching available models")

        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            models_data = response.json()
            self.logger.info(f"Retrieved {len(models_data['data'])} models")
            return [
                {"id": model["id"], "name": model["name"]}
                for model in models_data["data"]
            ]
        except requests.exceptions.Timeout:
            self.logger.error("Request timed out")
            return self._get_default_models()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}", exc_info=True)
            return self._get_default_models()
        except KeyError:
            self.logger.error("Malformed JSON response")
            return self._get_default_models()

    def _get_default_models(self):
        """
        Возвращает список базовых моделей по умолчанию.

        Returns:
            list: Список стандартных моделей.
        """
        models_default = [
            {"id": "deepseek-coder", "name": "DeepSeek"},
            {"id": "claude-3-sonnet", "name": "Claude 3.5 Sonnet"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"}
        ]
        self.logger.info(f"Using default models: {len(models_default)}")
        return models_default

    async def send_message(self, message: str, model: str):
        """
        Отправка сообщения выбранной языковой модели.

        Args:
            message (str): Сообщение для модели.
            model (str): Идентификатор модели.

        Returns:
            dict: Ответ модели или сообщение об ошибке.
        """
        if not self.headers:
            return {"error": "API key not set"}

        self.logger.debug(f"Sending message to model: {model}")

        data = {
            "model": model,
            "messages": [{"role": "user", "content": message}]
        }

        try:
            self.logger.debug("Making API request")
            # Асинхронный запрос через aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=data,
                    timeout=30
                ) as response:
                    response_data = await response.json()
                    self.logger.info("Successfully received response from API")
                    return response_data

        except Exception as e:
            error_msg = f"API request failed: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return {"error": str(e)}

    def get_balance(self):
        """
        Получение текущего баланса аккаунта.

        Returns:
            str: Баланс в формате '$X.XX' или 'Ошибка' при неудаче.
        """
        try:
            # Запрос баланса через API
            response = requests.get(
                f"{self.base_url}/credits",
                headers=self.headers
            )
            data = response.json()

            if data:
                data = data.get("data", {})
                # Вычисление доступного баланса
                balance = data.get("total_credits", 0) - data.get(
                    "total_usage", 0)
                return f"${balance:.2f}"

            return "Ошибка"
        except Exception as e:
            error_msg = f"API request failed: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return "Ошибка"

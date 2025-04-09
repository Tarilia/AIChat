import sqlite3      # Библиотека для работы с SQLite базой данных
import threading   # Библиотека для обеспечения потокобезопасности


class ChatCache:
    """
    Класс для кэширования истории чата в SQLite базе данных.
    """

    def __init__(self):
        """Инициализация системы кэширования."""
        self.db_name = 'chat_cache.db'
        self.local = threading.local()
        self._initialize_database()

    def get_connection(self):
        """
        Получение соединения с базой данных для текущего потока.
        """
        if not hasattr(self.local, 'connection'):
            self.local.connection = sqlite3.connect(
                self.db_name, check_same_thread=False
            )
        return self.local.connection

    def _initialize_database(self):
        """
        Инициализация базы данных и создание необходимых таблиц.
        """
        queries = [
            '''CREATE TABLE IF NOT EXISTS messages (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   model TEXT,
                   user_message TEXT,
                   ai_response TEXT,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                   tokens_used INTEGER
               )''',
            '''CREATE TABLE IF NOT EXISTS analytics_messages (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                   model TEXT,
                   message_length INTEGER,
                   response_time FLOAT,
                   tokens_used INTEGER
               )''',
            '''CREATE TABLE IF NOT EXISTS auth_data (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   api_key TEXT NOT NULL,
                   pin TEXT NOT NULL,
                   created_at DATETIME DEFAULT CURRENT_TIMESTAMP
               )'''
        ]
        conn = self.get_connection()
        cursor = conn.cursor()
        for query in queries:
            cursor.execute(query)
        conn.commit()

    def execute_query(self, query, params=None, fetch=False):
        """
        Общий метод для выполнения SQL-запросов.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        params = params or ()
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = None
        return result

    def save_message(self, model, user_message, ai_response, tokens_used):
        """
        Сохранение нового сообщения в базу данных.
        """
        query = '''
            INSERT INTO messages (model, user_message, ai_response, tokens_used)
            VALUES (?, ?, ?, ?)
        '''
        self.execute_query(query, (model, user_message, ai_response, tokens_used))

    def save_auth_data(self, api_key, pin):
        """
        Сохранение данных аутентификации.
        """
        query_delete = "DELETE FROM auth_data"
        query_insert = '''
            INSERT INTO auth_data (api_key, pin) VALUES (?, ?)
        '''
        self.execute_query(query_delete)
        self.execute_query(query_insert, (api_key, pin))

    def get_auth_data(self):
        """
        Получение сохраненных данных аутентификации.
        """
        query = '''
            SELECT api_key, pin FROM auth_data 
            ORDER BY created_at DESC LIMIT 1
        '''
        result = self.execute_query(query, fetch=True)
        return result[0] if result else (None, None)

    def clear_auth_data(self):
        """
        Очистка данных аутентификации.
        """
        query = "DELETE FROM auth_data"
        self.execute_query(query)

    def get_chat_history(self, limit=50):
        """
        Получение последних сообщений из истории чата.
        """
        query = '''
            SELECT id, model, user_message, ai_response, timestamp, tokens_used
            FROM messages
            ORDER BY timestamp DESC
            LIMIT ?
        '''
        return self.execute_query(query, params=(limit,), fetch=True)

    def save_analytics(self, timestamp, model, message_length,
                       response_time, tokens_used):
        """
        Сохранение данных аналитики в базу данных.
        """
        query = '''
            INSERT INTO analytics_messages (timestamp, model, message_length,
            response_time, tokens_used)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.execute_query(query, (timestamp, model, message_length,
                                   response_time, tokens_used))

    def get_analytics_history(self):
        """
        Получение всей истории аналитики.
        """
        query = '''
            SELECT timestamp, model, message_length, response_time, tokens_used
            FROM analytics_messages
            ORDER BY timestamp ASC
        '''
        return self.execute_query(query, fetch=True)

    def clear_history(self):
        """
        Очистка истории сообщений.
        """
        query = "DELETE FROM messages"
        self.execute_query(query)

    def get_formatted_history(self):
        """
        Получение форматированной истории чата.
        """
        query = '''
            SELECT id, model, user_message, ai_response, timestamp, tokens_used
            FROM messages
            ORDER BY timestamp ASC
        '''
        rows = self.execute_query(query, fetch=True)
        return [
            {
                "id": row[0],
                "model": row[1],
                "user_message": row[2],
                "ai_response": row[3],
                "timestamp": row[4],
                "tokens_used": row[5]
            }
            for row in rows
        ]

    def __del__(self):
        """
        Закрытие соединения с базой данных.
        """
        if hasattr(self.local, 'connection'):
            self.local.connection.close()

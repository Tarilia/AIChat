# Инструкция по установке и сборке

## Системные требования

- Windows 10/11 или Linux
- Python 3.7 или выше
- pip (Python package manager)
- Минимум 2 ГБ свободного места на диске
- Стабильное интернет-соединение

## Установка зависимостей

1. Установите Python с официального сайта:
   https://www.python.org/downloads/

2. Убедитесь, что Python и pip установлены корректно:
```cmd
python --version
pip --version
```

3. Создайте виртуальное окружение:
```python -m venv venv
```
   - Активация виртуального окружения
   - Для Windows:
```
   .\venv\Scripts\activate
```
   - Для Linux/Mac:
```
   source venv/bin/activate
```

4. Установите необходимые пакеты:
```cmd
pip install -r requirements.txt
```

## Сборка приложения

### Windows

1. Перейдите в директорию проекта
2. Запустите сборку:
```cmd
python build.py
```
3. Исполняемый файл будет создан в директории `bin/AIChat.exe`

### Linux

1. Перейдите в директорию проекта
2. Запустите сборку:
```bash
python3 build.py
```
3. Исполняемый файл будет создан в директории `bin/aichat`
4. Сделайте файл исполняемым:
```bash
chmod +x bin/aichat
```
5. Для Ubuntu: 
 - может понадобиться установка дополнительных библиотек:
```pip install libgtk-3-0
pip install libgstreamer-plugins-base1.0-0
pip install libmpv1
```
 - и замена абсолютных путей на относительные. Вместо этого, также, можно добавить в начало main.py, перед импортами:
```import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

## Примечания

- Логи сборки можно найти в папке `build/logs/`
- При возникновении проблем:
  1. Убедитесь что есть доступ в интернет
  2. Проверьте наличие свободного места
  3. Попробуйте запустить сборку повторно
  4. Проверьте логи в папке `build/logs/`

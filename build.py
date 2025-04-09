import sys  # Для доступа к системным параметрам и функциям
import shutil  # Для операций с файлами и директориями
import subprocess  # Для запуска внешних процессов
from pathlib import Path  # Для удобной работы с путями файловой системы


def build_windows():
    """
    Сборка исполняемого файла для Windows с помощью PyInstaller.

    Устанавливаются зависимости, создаётся исполняемый файл, который перемещается
    в папку bin.
    """
    print("Building Windows executable...")

    # Устанавливаем зависимости из requirements.txt
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ])

    # Создаём папку bin, если она не существует
    bin_dir = Path("bin")
    bin_dir.mkdir(exist_ok=True)

    # Запускаем PyInstaller с указанием параметров сборки
    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=AI Chat",
        "--clean",
        "--noupx",
        "--uac-admin",
        "src/main.py"
    ])

    # Перемещаем собранный файл в папку bin
    try:
        shutil.move("dist/AI Chat.exe", "bin/AIChat.exe")
        print("Windows build completed! Executable location: bin/AIChat.exe")
    except shutil.Error:
        print("Windows build completed! Executable location: dist/AI Chat.exe")


def build_linux():
    """
    Сборка исполняемого файла для Linux с помощью PyInstaller.

    Устанавливаются зависимости, создаётся исполняемый файл, который перемещается
    в папку bin.
    """
    print("Building Linux executable...")

    # Устанавливаем зависимости из requirements.txt
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ])

    # Создаём папку bin, если она не существует
    bin_dir = Path("bin")
    bin_dir.mkdir(exist_ok=True)

    # Запускаем PyInstaller с указанием параметров сборки
    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=assets/icon.ico",
        "--name=aichat",
        "src/main.py"
    ])

    # Перемещаем собранный файл в папку bin
    try:
        shutil.move("dist/aichat", "bin/aichat")
        print("Linux build completed! Executable location: bin/aichat")
    except shutil.Error:
        print("Linux build completed! Executable location: dist/aichat")


def main():
    """
    Основная функция сборки.

    Определяет текущую ОС и вызывает соответствующую функцию сборки.
    """
    # Проверка операционной системы и вызов подходящей функции
    if sys.platform.startswith('win'):
        build_windows()  # Windows
    elif sys.platform.startswith('linux'):
        build_linux()  # Linux
    else:
        print("Unsupported platform")  # Для других ОС


# Точка входа в программу
if __name__ == "__main__":
    main()

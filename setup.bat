@echo off
echo ========================================
echo  Настройка окружения для AssistDev бота
echo ========================================
echo.

REM Проверяем, установлен ли Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден в PATH!
    echo Установите Python 3.10+ с сайта python.org
    pause
    exit /b 1
)

echo [1/4] Создание виртуального окружения...
python -m venv venv
if errorlevel 1 (
    echo [ОШИБКА] Не удалось создать виртуальное окружение
    pause
    exit /b 1
)

echo [2/4] Активация виртуального окружения...
call venv\Scripts\activate.bat

echo [3/4] Обновление pip...
python -m pip install --upgrade pip

echo [4/4] Установка зависимостей...
pip install -r requirements.txt

echo.
echo ========================================
echo  Установка завершена!
echo ========================================
echo.
echo Далее:
echo 1. Создайте файл .env из .env.example
echo    copy .env.example .env
echo 2. Заполните BOT_TOKEN и API ключи в .env
echo 3. Запустите бота:
echo    python -m assistdev_bot.bot
echo.
pause

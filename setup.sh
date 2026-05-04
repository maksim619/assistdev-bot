#!/bin/bash
# Настройка окружения для AssistDev бота (Linux/Mac)

echo "========================================"
echo "  Настройка окружения для AssistDev бота"
echo "========================================"
echo ""

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    echo "[ОШИБКА] Python3 не найден!"
    echo "Установите Python 3.10+"
    exit 1
fi

echo "[1/4] Создание виртуального окружения..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "[ОШИБКА] Не удалось создать виртуальное окружение"
    exit 1
fi

echo "[2/4] Активация виртуального окружения..."
source venv/bin/activate

echo "[3/4] Обновление pip..."
pip install --upgrade pip

echo "[4/4] Установка зависимостей..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "  Установка завершена!"
echo "========================================"
echo ""
echo "Далее:"
echo "1. Создайте файл .env из .env.example"
echo "   cp .env.example .env"
echo "2. Заполните BOT_TOKEN и API ключи в .env"
echo "3. Запустите бота:"
echo "   python -m assistdev_bot.bot"
echo ""

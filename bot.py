import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import random

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет!')

# Список из 10 возможных ответов
RESPONSES = [
    "чево?",
    "да, скорее всего",
    "не могу знать",
    "вот так и живем",
    "добро",
    "ничего не понятно",
    "охайо!",
    "рад тебя видеть!",
    "кринжатина",
    "салют!"
]

# Обработчик любого текстового сообщения
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = random.choice(RESPONSES)
    await update.message.reply_text(response)

# Основная функция запуска бота
def main():
    # Получаем токен из переменной окружения
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise ValueError("Переменная окружения BOT_TOKEN не установлена")

    # Создаём приложение
    application = Application.builder().token(token).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()

import os
import json
import spacy
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

ENV_FILE = ".env"
nlp = spacy.load("ru_core_news_sm")

def get_token():
    if not os.path.exists(ENV_FILE):
        token = input("Введите токен Telegram-бота: ").strip()
        with open(ENV_FILE, "w") as f:
            f.write(f"BOT_TOKEN={token}\n")
        print("Токен сохранён в .env")
        return token
    else:
        load_dotenv(ENV_FILE)
        token = os.getenv("BOT_TOKEN")

        if not token:
            token = input("Введите токен Telegram-бота: ").strip()
            with open(ENV_FILE, "w") as f:
                f.write(f"BOT_TOKEN={token}\n")
        return token


def load_responses():
    with open("responses.json", "r", encoding="utf-8") as f:
        return json.load(f)

RESPONSES = load_responses()

def generate_response(text: str):
    doc = nlp(text.lower())

    for token in doc:
        lemma = token.lemma_
        if lemma in RESPONSES:
            return RESPONSES[lemma]
    return "Извините, я пока не знаю как на это ответить, спросите что-нибудь другое"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравствуйте! Вас приветствует бот университета Синергия, напишите ваш вопрос.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = generate_response(update.message.text)
    await update.message.reply_text(response)

def main():
    token = get_token()

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
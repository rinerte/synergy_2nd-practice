import os
import json
import spacy
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

ENV_FILE = ".env"

nlp = spacy.load("ru_core_news_sm")

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

def main():
    while True:
        user_input = input("Введите вопрос (или 'выход'): ")

        if user_input.lower()=="выход":
            break

        answer = generate_response(user_input)
        print(answer)

if __name__ == "__main__":
    main()
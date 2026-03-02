import json
import spacy

nlp = spacy.load("ru_core_news_sm")

def load_responses():
    with open("responses.json", "r", encoding="utf-8") as f:
        return json.load(f)

RESPONSES = load_responses()

def find_keyword(text: str):
    doc = nlp(text.lower())

    for token in doc:
        lemma = token.lemma_
        if lemma in RESPONSES:
            return lemma
    return None

def main():
    while True:
        user_input = input("Введите вопрос (или 'выход'): ")

        if user_input.lower()=="выход":
            break

        keyword = find_keyword(user_input)

        if keyword:
            print(f"Найдено ключевое слово: {keyword}")
        else:
            print("Ключевое слово не найдено")

if __name__ == "__main__":
    main()
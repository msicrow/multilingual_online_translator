import requests
from bs4 import BeautifulSoup


def send_and_receive(phrase, trans_to):
    language = {"en": "french-english", "fr": "english-french"}
    headers = {"User-Agent": "Mozilla/5.0"}
    base_url = "https://context.reverso.net/translation/"
    url = base_url + f"{language[trans_to]}/{phrase}"
    r = requests.get(url, headers=headers)
    print(r.status_code, "OK" if r else "Fail")
    return r.content


def translate(page_content):
    words = []
    sentences = []

    soup = BeautifulSoup(page_content, "html.parser")

    print("\nContext examples:\nTranslations:")
    word_tags = soup.find_all("a", class_="translation")
    for tag in word_tags:
        words.append(tag.text.strip())
    for word in words[1:]:
        print(word)

    print("\nExamples:")
    example_tags = soup.find_all("div", class_="ltr")
    for ex_tag in example_tags:
        sentences.append(ex_tag.text.strip())
    sep_sentences = [j + ":" if not i % 2 else j + "\n" for i, j in enumerate(sentences[2:])]
    for sentence in sep_sentences:
        print(sentence)


def languages():
    trans_from = input("Type the language that are translating from:")
    trans_to = input("Type the language that you wish to translate to:")
    return trans_from, trans_to


def main():
    translate_to = input("Type 'en' if you want to translate from French into English, "
                         "or 'fr' if you want to translate from English into French:\n")
    phrase = input("Type the word you want to translate:\n")
    print(f"You chose '{translate_to}' as the language to translate '{phrase}' to.")
    page_html = send_and_receive(phrase, translate_to)
    translate(page_html)


if __name__ == "__main__":
    main()

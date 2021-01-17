import requests
from bs4 import BeautifulSoup


def send_and_receive(phrase, to_lang):
    query = {"en": "french-english", "fr": "english-french"}
    headers = {"User-Agent": "Mozilla/5.0"}
    base_url = "https://context.reverso.net/translation/"
    url = base_url + f"{query[to_lang]}/{phrase}"
    r = requests.get(url, headers=headers)
    print(r.status_code, "OK" if r else "Fail")
    return r.content


def translate(page_content):
    translations = []
    sentences = []
    soup = BeautifulSoup(page_content, "html.parser")

    translation_tags = soup.find_all("a", class_="translation")
    for tr_tag in translation_tags:
        translations.append(tr_tag.text.strip())

    example_tags = soup.find_all("div", class_="ltr")
    for ex_tag in example_tags:
        sentences.append(ex_tag.text.strip())

    print(f"Translations\n{translations}\n{sentences}")


def main():
    translate_to = input("Type 'en' if you want to translate from French into English, "
                         "or 'fr' if you want to translate from English into French:\n")
    phrase = input("Type the word you want to translate:\n")
    print(f"You chose '{translate_to}' as the language to translate '{phrase}' to.'")
    page_html = send_and_receive(phrase, translate_to)
    translate(page_html)


if __name__ == "__main__":
    main()

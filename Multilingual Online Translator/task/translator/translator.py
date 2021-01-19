import requests
from bs4 import BeautifulSoup

languages = ["arabic", "german", "english", "spanish", "french", "hebrew", "japanese", "dutch", "polish",
             "portuguese", "romanian", "russian", "turkish"]


def send_and_receive(from_lang, to_lang, phrase):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    base_url = "https://context.reverso.net/translation/"
    url = base_url + f"{from_lang}-{to_lang}/{phrase}"
    r = requests.get(url, headers=headers)
    if not r:
        print(r.status_code)
    return r.content


def translate(page_content, to_lang):
    words = []
    sentences = []

    soup = BeautifulSoup(page_content, "html.parser")

    print(f"\n{to_lang.title()} Translations:")
    word_tags = soup.select("section#top-results > div#translations-content > a")
    for tag in word_tags:
        words.append(tag.text.strip())
    for word in words:
        print(word)

    print(f"\n{to_lang.title()} Examples:")
    example_tags = soup.select("section#examples-content > div > div > span.text")
    for ex_tag in example_tags:
        sentences.append(ex_tag.text.strip())
    sep_sentences = [j + ":" if not i % 2 else j + "\n" for i, j in enumerate(sentences)]
    for sentence in sep_sentences:
        print(sentence)


def main():
    print("Support for translation to and from the following languages:")
    for i, lang in enumerate(languages):
        print(f"{i + 1}. {lang.title()}")

    fr_num = int(input("Enter the number of your language you wish to translate from:"))
    to_num = int(input("Enter the number of the language you wish to translate to or "
                       "'0' to translate to all languages:"))
    phrase = input("Enter the word you wish to translate:")

    if to_num == 0:
        fr_lang = languages[fr_num - 1]
        del languages[fr_num - 1]  # avoids translating to same lang translating from
        print(languages)
        for lang in languages:
            lang_html = send_and_receive(fr_lang, lang, phrase)
            translate(lang_html, lang)

    else:
        page_html = send_and_receive(languages[fr_num - 1], languages[to_num - 1], phrase)
        translate(page_html, languages[to_num - 1])


if __name__ == "__main__":
    main()

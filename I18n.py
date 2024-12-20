import json

LANG = 0
# 0: Chinese Simplified, 1: Chinese Traditional, 2: English, 3: Japanese（翻译由 ChatGPT 提供）

STRINGS = {}
LANG_DICT = {
    0: 'zh_cn',
    1: 'zh_tr',
    2: 'en_us',
    3: 'jp_jp'
}


def set_language(lang: int):
    global LANG
    LANG = lang
    load_strings()


def load_strings():
    with open('./assets/lang/' + LANG_DICT[LANG] + '.json', 'r', encoding='utf-8') as file:
        global STRINGS
        STRINGS = json.load(file)


def text(string: str):
    return TranslatableText(string)


def literal(string: str):
    return Text(string)


class Text:

    def __init__(self, string):
        self.string = string

    def format(self, *args):
        return self.string.format(*args)

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

    def get(self):
        return self.string


class TranslatableText(Text):

    def __init__(self, key):
        super().__init__(key)

    def format(self, *args):
        return STRINGS[self.string].format(*args) if self.string in STRINGS else self.string

    def __str__(self):
        return STRINGS[self.string] if self.string in STRINGS else self.string

    def __repr__(self):
        return STRINGS[self.string] if self.string in STRINGS else self.string

    def get(self):
        return STRINGS[self.string] if self.string in STRINGS else self.string

import json

LANG = 0
# 0: Chinese Simplified, 1: Chinese Traditional, 2: English

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
    with open('assets/lang/' + LANG_DICT[LANG] + '.json', 'r', encoding='utf-8') as file:
        global STRINGS
        STRINGS = json.load(file)


def text(string: str):
    return STRINGS[string] or '?'

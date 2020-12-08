from random import choice
import time


def get_word(lang: str) -> str:
    file = open(f"{lang}.txt", "r", encoding="UTF-8")
    words = file.read()
    words = words.split()
    word = choice(words)
    word = word.replace("_", " ")
    return word


def set_in_game(in_game: bool, context) -> bool:
    try:
        context.chat_data["in_game"] = in_game
        return True
    except:
        return False


def in_game(context) -> bool:
    return context.chat_data.get("in_game", False)


def time_finished(context) -> bool:
    try:
        start_time = context.chat_data["start_time"]
        r = time.time() - start_time >= 300
        return r
    except:
        return False


def set_start_time(context) -> bool:
    try:
        context.chat_data["start_time"] = time.time()
        return True
    except:
        return False


def set_word(context, lang: str) -> bool:
    try:
        context.chat_data["word"] = get_word(lang)
        return True
    except:
        return False


def cr_word(context) -> str:
    return context.chat_data.get("word", "NONE")


def set_host(host: list, context) -> bool:
    try:
        context.chat_data["host"] = host
        return True
    except:
        return False


def cr_host(context):
    return context.chat_data.get("host", "NONE")


def eq(inp, rec):
    inp, rec = inp.lower(), rec.lower()
    inp, rec = inp.replace(" ", ""), rec.replace(" ", "")
    inp, rec = inp.replace("\n", ""), rec.replace("\n", "")

    char = """
    ü
    û
    ê
    î
    ş
    ç
    ı
    ك
    ھ
    ڵ
    وو
    ڕ
    """.split()

    repl = """
    u
    u
    e
    i
    s
    c
    i
    ک
    ه
    ل
    و
    ر
    """.split()

    for i in range(len(char)):
        rec, inp = rec.replace(char[i], repl[i]), inp.replace(char[i], repl[i])

    return rec in inp

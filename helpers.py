from random import choice
import time


def get_word(lang: str) -> str:
    file = open(f"{lang}.txt", "r", encoding="UTF-8")
    words = file.read()
    words = words.split()
    word = choice(words)
    word = word.replace("_", " ")
    return word


def new_game(usr, lang, context) -> bool:
    try:
        context.chat_data["in_game"] = True
        context.chat_data["start_time"] = time.time()
        context.chat_data["word"] = get_word(lang)
        context.chat_data["host"] = [usr.id, usr.full_name]
        return True
    except:
        return False

def stop_game(context):
    del context.chat_data["start_time"]
    del context.chat_data["word"]
    del context.chat_data["host"]
    context.chat_data["in_game"] = False
    

def in_game(context) -> bool:
    return context.chat_data.get("in_game", False)


def time_finished(context) -> bool:
    try:
        start_time = context.chat_data["start_time"]
        r = time.time() - start_time >= 300
        return r
    except:
        return False



def cr_word(context) -> str:
    return context.chat_data.get("word", "NONE")


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

from typing import Union

from . import database

collection = database.chats


def get_chat(chat_id: int) -> Union[dict, bool]:
    return collection.find_one(chat_id) or False


def update_chat(chat_id: int, title: str) -> bool:
    find = get_chat(chat_id)

    if not find:
        collection.insert_one(
            {
                "chat_id": chat_id,
                "title": title,
                "games": 1
            }
        )
        return True

    collection.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "title": title,
                "scores": find["games"] + 1
            }
        }
    )
    return True

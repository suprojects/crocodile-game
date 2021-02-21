from typing import Union

from . import database

collection = database.users


def get(user_id: int) -> Union[dict, bool]:
    return collection.find_one({"user_id": user_id}) or False


def update(chat_id: int, user_id: int, firstname: str, username: Union[str, None]) -> bool:
    find = get(user_id)

    if not find:
        collection.insert_one(
            {
                "user_id": user_id,
                "firstname": firstname,
                "username": username,
                "scores": {
                    chat_id:  1
                }
            }
        )
        return True

    scores = find["scores"]

    if chat_id not in scores:
        scores[chat_id] = 1
    else:
        scores[chat_id] += 1

    collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "firstname": firstname,
                "username": username,
                "scores": scores
            }
        }
    )
    return True


def total_scores(user_id: int) -> Union[int, bool]:
    user = get(user_id)

    if not user:
        return False
    elif "scores" not in user:
        return False

    return sum([user["scores"][chat_id] for chat_id in user["scores"]])


def scores_in_chat(chat_id: int, user_id: int) -> Union[int, bool]:
    user = get(user_id)

    if not user:
        return False
    elif "scores" not in user:
        return False
    elif chat_id not in user["scores"]:
        return False

    return user["scores"][chat_id]


def top_ten() -> Union[list, bool]:
    find = list(collection.find())

    if not find:
        return False

    all = []

    for item in find:
        all.append(
            {
                "user_id": item["user_id"],
                "firstname": item["firstname"],
                "username": item["username"],
                "scores": sum([item["scores"][chat_id] for chat_id in item["scores"]]),
            }
        )

    return sorted(all, key=lambda x: x["scores"])

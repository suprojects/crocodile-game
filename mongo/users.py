from typing import Union

from . import database

collection = database.users


def get_user(user_id: int) -> Union[dict, bool]:
    return collection.find_one({"user_id": user_id}) or False


def add_score(user_id: int, firstname: str, username: Union[str, None]) -> bool:
    find = get_user(user_id)

    if not find:
        collection.insert_one(
            {
                "user_id": user_id,
                "firstname": firstname,
                "username": username,
                "scores": 1
            }
        )
        return True

    collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "firstname": firstname,
                "username": username,
                "scores": find["scores"] + 1
            }
        }
    )
    return True

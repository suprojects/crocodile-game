from telegram.ext import CommandHandler

import sql.game_sql as sql


def leaderboard(update, context):
    cht, usr, msg = update.effective_chat, update.effective_user, update.effective_message

    all_scores = sql.all_scores()

    max = 1
    arr = []

    for score in all_scores:
        if int(score.scores) > max:
            max = int(score.scores)
            arr.append(score)
    msg.reply_text(
        "1st player:"
        "\nid: {}\nuname: {}\nscores: {}".format(
            arr[-1].user_id, arr[-1].username, arr[-1].scores)
    )


__handlers__ = [
    [
        CommandHandler(
            "leaderboard",
            leaderboard
        )
    ]
]

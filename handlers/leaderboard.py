from telegram.ext import CommandHandler

import sql.game_sql as sql


def leaderboard(update, context):
    cht, usr, msg = update.effective_chat, update.effective_user, update.effective_message

    all_scores = sql.all_scores()

    max = 1
    arr = []

    for score in all_socres:
        if score.scores > max:
            max = socre.scores
            arr.append(score)
    msg.reply_text("1st player:"
                   "\nid: {}".format(arr[-1].user_id)
                   "\nuname: {}".format(arr[-1].username)
                   "\nscores: {}".format(arr[-1].scores))


__handlers__ = [
    [
        CommandHandler(
            "leaderboard",
            leaderboard
        )
    ]
]

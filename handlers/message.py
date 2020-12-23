from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from sql.game_sql import add_score
from strings import _
from il import il
from helpers import eq, in_game, stop_game, time_finished, cr_word, cr_host


@il
def message(update, context, lang):
    usr, msg = update.effective_user, update.effective_message

    if in_game(context):
        if time_finished(context):
            stop_game(context)
            msg.reply_text(
                "The current game was aborted as no one said the correct word in 5 minutes."
            )
            return ""

        host = cr_host(context)
        word = cr_word(context)

        if type(host) != str:
            if eq(msg.text, word):
                if usr.id != host[0]:
                    add_score(update.effective_chat.id, usr.id, usr.username)
                    stop_game(context)
                    msg.reply_text(
                        _(lang, "guessed").format(
                            f'<a href="tg://user?id={usr.id}">{usr.full_name}</a>',
                            f'<b>{word}</b>'
                        ),
                        parse_mode="HTML",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        _(lang, "next_game"),
                                        callback_data="next_game")
                                ]
                            ]
                        )
                    )
                else:
                    stop_game(context)
                    msg.reply_text(
                        _(lang, "host").format(
                            f'<a href="tg://user?id={usr.id}">{usr.full_name}</a>',
                            f'<b>{word}</b>'
                        ),
                        parse_mode="HTML",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        _(lang, "next_game"),
                                        callback_data="next_game")
                                ]
                            ]
                        )
                    )


__handlers__ = [
    [MessageHandler(Filters.text & ~Filters.command & Filters.group, message)]
]

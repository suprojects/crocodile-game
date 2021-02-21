from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, CallbackContext, Filters

import mongo.chats as db
from helpers.game import new_game, get_game, next_word
from helpers.wrappers import nice_errors
from bot import SUDO_USERS


@nice_errors
def view(update: Update, context: CallbackContext):
    game = get_game(context)

    if game["host"].id == update.effective_user.id:
        update.callback_query.answer(
            game["word"],
            show_alert=True
        )
    else:
        update.callback_query.answer(
            "This is not for you.", show_alert=True
        )


@nice_errors
def next(update: Update, context: CallbackContext):
    game = get_game(context)

    if game["host"].id == update.effective_user.id:
        word = next_word(context)
        update.callback_query.answer(
            word,
            show_alert=True
        )
    else:
        update.callback_query.answer(
            "This is not for you.", show_alert=True
        )


@nice_errors
def host(update: Update, context: CallbackContext):
    new_game(update.effective_user, context)

    update.effective_message.reply_text(
        f"{update.effective_user.mention_html()} talks about a word.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "View",
                        callback_data="view")
                ],
                [
                    InlineKeyboardButton(
                        "Next",
                        callback_data="next")
                ]
            ]
        )
    )

    db.update(update.effective_chat.id, update.effective_chat.title)


__handlers__ = [
    [CallbackQueryHandler(view, pattern="view")],
    [CallbackQueryHandler(next, pattern="next")],
    [CallbackQueryHandler(host, pattern="host")]
]

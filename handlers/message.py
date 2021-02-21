from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, MessageHandler, Filters

import mongo.users as db
from helpers.game import get_game, is_true


def message(update: Update, context: CallbackContext):
    try:
        game = get_game(context)

        if game["host"].id != update.effective_user.id:
            if is_true(update.effective_message.text, context):
                update.effective_message.reply_text(
                    f"{update.effective_user.mention_html()} guessed the correct word, {game['word']}.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "I want to be the host",
                                    callback_data="host")
                            ]
                        ]
                    )
                )

                db.update(
                    update.effective_chat.id,
                    update.effective_user.id,
                    update.effective_user.first_name,
                    update.effective_user.username
                )
    except:
        pass


__handlers__ = [
    [
        MessageHandler(
            Filters.text & ~Filters.command & Filters.chat_type.groups,
            message
        )
    ]
]

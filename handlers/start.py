from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, Filters

import mongo.chats as db
from helpers.game import new_game
from helpers.wrappers import nice_errors


@nice_errors
def start(update: Update, context: CallbackContext):
    if "frompvt" in update.effective_message.text:
        update.effective_message.reply_text(
            """
<b>Thanks for adding me!</b>

You can <b>visit my news channel to get tuned about any update and my discussion group to get help or report a bug</b>.
            """.format(context.bot.username),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="News", url="http://t.me/su_Bots"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="Discussion", url="https://t.me/su_Chats"
                        )
                    ]
                ]
            )
        )
    else:
        new_game(update.effective_user, context)

        update.effective_message.reply_text(
            f"{update.effective_user.mention_html()} talks about a word.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "View",
                            callback_data="view"
                        )
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


def _start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(".")


__handlers__ = [
    [CommandHandler("start", start, filters=Filters.chat_type.groups)],
    [CommandHandler("start", _start, filters=Filters.chat_type.private)]
]

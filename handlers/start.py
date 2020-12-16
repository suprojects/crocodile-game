from telegram.ext import CommandHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from strings import _
from il import il
from helpers import in_game, new_game
from threading import Timer


@il
def start_pvt(update, context, lang):
    update.effective_message.reply_text(
        _(lang, "add_to_chat").format(context.bot.username), "HTML", True, reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Join our Channel 🔈", url="http://t.me/su_Bots"),
                    InlineKeyboardButton(
                        text="Discussion Group 💬", url="https://t.me/su_BotsChat"),
                ]
            ]
        ))


@il
def start_game(update, context, lang):
    usr, msg, cht = update.effective_user, update.effective_message, update.effective_chat

    if in_game(context):
        msg.reply_text(_(lang, "game_is_running").format(context.bot.username))
    else:
        if "frompvt" not in msg.text:
            new_game(usr, lang, context)
            msg.reply_text(
                _(lang, "presenter")
                .format(f'<a href="tg://user?id={usr.id}">{usr.full_name}</a>'),
                quote=False,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                _(lang, "view_word"),
                                callback_data="view_word")],
                        [
                            InlineKeyboardButton(
                                _(lang, "next_word"),
                                callback_data="next_word")
                        ]
                    ]
                )
            )
            

__handlers__ = [
    [CommandHandler("start", start_pvt, filters=Filters.private)],
    [CommandHandler("start", start_game, filters=Filters.group)]
]

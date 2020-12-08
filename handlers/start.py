from telegram.ext import CommandHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from strings import _
from il import il
from helpers import *


@il
def start_pvt(update, context, lang):
    update.effective_message.reply_text(
        _(lang, "add_to_chat").format(context.bot.username), parse_mode="HTML")


@il
def start_game(update, context, lang):
    usr, msg = update.effective_user, update.effective_message

    if in_game(context):
        msg.reply_text(_(lang, "game_is_running").format(context.bot.username))
    else:
        if "frompvt" not in msg.text:
            set_in_game(True, context)
            set_start_time(context)
            set_host([usr.id, usr.full_name], context)
            set_word(context, lang)
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

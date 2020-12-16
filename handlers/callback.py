from telegram.ext import CallbackQueryHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from strings import _
from il import il
from helpers import cr_host, cr_word, in_game, new_game
from bot import SUDO_USERS


@il
def callback(update, context, lang):
    usr, query = update.effective_user, update.callback_query

    if query.data == "view_word":
        host = cr_host(context)
        if type(host) != str:
            if usr.id == host[0]:
                query.answer(cr_word(context), show_alert=True)
            else:
                query.answer(_(lang, "not_your_word"), show_alert=True)

    if query.data == "next_word":
        host = cr_host(context)
        if type(host) != str:
            if usr.id == host[0]:
                new_game(usr, lang, context)
                query.answer(cr_word(context), show_alert=True)
            else:
                query.answer(_(lang, "not_your_word"), show_alert=True)

    if query.data == "next_game":
        query.edit_message_reply_markup(None)

        if not in_game(context):
            new_game(usr, lang, context)
            query.message.reply_text(
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

    if query.data.startswith("chatlang"):
        if query.message.chat.type != "private":
            if query.message.chat.get_member(query.from_user.id).status not in ("creator", "administrator"):
                if query.from_user.id not in SUDO_USERS:
                    query.answer(_(lang, "not_admin"),
                                 show_alert=True)
                    return

        data = query.data.split("_")
        selected_lang = data[1]
        context.chat_data["lang"] = selected_lang
        query.edit_message_text(_(selected_lang, "languagec"))


__handlers__ = [
    [CallbackQueryHandler(callback)]
]

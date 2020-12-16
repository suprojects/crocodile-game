from telegram.ext import CommandHandler
from strings import _
from il import il
from helpers import stop_game
from bot import SUDO_USERS


@il
def abort(update, context, lang):
    cht, usr, msg = update.effective_chat, update.effective_user, update.effective_message

    if cht.get_member(usr.id).status not in ("creator", "administrator"):
        if usr.id not in SUDO_USERS:
            msg.reply_text(_(lang, "not_admin"))
            return ""
    stop_game(context)
    msg.reply_text(
        _(lang, "game_stopped").format(
            f'<a href="tg://user?id={usr.id}">{usr.full_name}</a>'
        ), "HTML")


__handlers__ = [
    [CommandHandler("abort", abort)]
]

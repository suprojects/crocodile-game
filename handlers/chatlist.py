from telegram.ext import CommandHandler, Filters
from bot import SUDO_USERS
from sql import get_chats
from strings import _
from il import il


@il
def chatlist(update, context, lang):
    update.effective_message.reply_document(
        open(
            get_chats(),
            "rb"
        )
    )


__handlers__ = [
    [CommandHandler("chatlist", chatlist, filters=Filters.user(SUDO_USERS))]
]

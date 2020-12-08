from telegram.ext import CommandHandler
from strings import _
from il import il


@il
def rules(update, context, lang):
    update.effective_message.reply_text(
        _(lang, "rules"),
        parse_mode="HTML"
    )


__handlers__ = [
    [CommandHandler("rules", rules)]
]

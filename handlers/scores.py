from telegram.ext import CommandHandler
from sql.game_sql import get_scores
from strings import _
from il import il


@il
def scores(update, context, lang):
    update.effective_message.reply_text(
        _(lang, "scores").format(
            get_scores(
                update.effective_user.id
            )
        ),
        parse_mode="HTML"
    )


__handlers__ = [
    [CommandHandler("scores", scores)]
]

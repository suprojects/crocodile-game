from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from helpers.wrappers import admin_only
from helpers.game import end_game


@admin_only
def abort(update: Update, context: CallbackContext):
    try:
        end_game(context)
        update.effective_message.reply_text(
            f"{update.effective_user.mention_html()} aborted the game."
        )
    except Exception as e:
        update.effective_message.reply_text(f"Error: {e}")


__handlers__ = [
    [CommandHandler("abort", abort)]
]

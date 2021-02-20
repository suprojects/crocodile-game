from telegram.ext import Updater, Defaults

from config import BOT_TOKEN, SUDO_USERS

updater = Updater(
    token=BOT_TOKEN,
    defaults=Defaults(
        parse_mode="HTML",
        disable_web_page_preview=True,
        quote=False
    )
)

dp = updater.dispatcher


if __name__ == "__main__":
    import os
    import sys
    from threading import Thread

    from telegram import Update
    from telegram.ext import CallbackContext, CommandHandler

    from handlers import all_handlers
    from helpers.filters import sudo_only

    if "-r" in sys.argv:
        for user in SUDO_USERS:
            updater.bot.send_message(user, "Restarted.")

    def stop_and_restart(chat, msg):
        os.system("git pull")
        updater.stop()
        os.execl(
            sys.executable,
            sys.executable,
            *sys.argv,
            "-r",
            f"{chat}_{msg}"
        )

    def restart(update: Update, context: CallbackContext):
        update.effective_message.reply_text("Restarting...")
        Thread(
            target=stop_and_restart, args=(
                update.effective_chat.id,
                update.effective_message.message_id,
            )
        ).start()

    for handler in all_handlers:
        if len(handler) == 2:
            if handler[1] == "error":
                dp.add_error_handler(handler[0])
            else:
                dp.add_handler(handler[0], handler[1])
        else:
            dp.add_handler(handler[0])

    dp.add_handler(
        CommandHandler("r", restart, filters=sudo_only)
    )

    updater.start_polling(clean=True)
    updater.idle()

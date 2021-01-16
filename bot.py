from telegram.ext import Updater, PicklePersistence
from os import environ


TOKEN = "1408658862:AAF0vifsXB2r2OgqndKcDei8alWCNAqKvFg"
DB_URI = environ.get("DATABASE_URL", "postgres://hwemieye:TXCzli-eCW3gvkUzwK5A3B-i0P4hhe0p@hattie.db.elephantsql.com:5432/hwemieye")
SUDO_USERS = [
    951435494
]

updater = Updater(
    TOKEN,
    use_context=True,
    persistence=PicklePersistence(filename="data")
)
dp = updater.dispatcher


def main():
    import sys
    import os
    from threading import Thread
    from telegram.ext import CommandHandler, Filters
    from handlers import all_handlers

    if "-r" in sys.argv:
        for SUDO_USER in SUDO_USERS:
            updater.bot.send_message(SUDO_USER, "Bot restarted successfully.")

    def stop_and_restart():
        os.system("git pull")
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv, "-r")

    def restart(update, context):
        update.message.reply_text("Bot is restarting...")
        Thread(target=stop_and_restart).start()

    for handler in all_handlers:
        if len(handler) == 2:
            dp.add_handler(
                handler[0],
                handler[1]
            )
        else:
            dp.add_handler(
                handler[0]
            )

    dp.add_handler(
        CommandHandler(
            "r",
            restart,
            filters=Filters.user(SUDO_USERS)
        )
    )

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == "__main__":
    main()

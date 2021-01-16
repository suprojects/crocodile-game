from io import BytesIO
from time import sleep
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.error import BadRequest, RetryAfter

from bot import SUDO_USERS
import sql.users_sql as sql
from sql.users_helper import chats as cs


def cleandb(update, context):
    chats = cs()
    count = 0

    msg = update.message.reply_text(
        "Cleaning..."
    )

    for chat in chats:
        try:
            context.bot.get_chat(chat)
        except BadRequest as excp:
            if "not found" in excp.message:
                try:
                    sql.del_chat(chat)
                    count += 1
                except:
                    pass
        except RetryAfter as excp:
            msg.edit_text(
                "Stopped. RetryAfter: {}".format(
                    excp.message
                )
            )
            break

    update.message.reply_text(
        "Database cleaning finished.\n"
        f"Removed {count} chat(s) from database."
    )


def broadcast(update, context):
    msg = update.effective_message

    to_broadcast = msg.text.replace(
        "/broadcast ",
        ""
    )

    if len(to_broadcast) == 0:
        msg.reply_text(
            "Give me some text to broadcast."
        )
        return

    chats = cs()
    sent = 0
    failed = 0

    for chat in chats:
        try:
            context.bot.send_message(
                int(chat.chat_id),
                to_broadcast
            )
            sleep(0.5)
            sent += 1
        except:
            failed += 1

    msg.reply_text(
        "Broadcast complete.\n"
        f"Sent the message to {sent} chat(s).\n"
        f"Failed to send the message to {failed} chat(s)."
    )


def chatlist(update, context):
    all_chats = cs(True)
    chatfile = "List of chat(s).\n"

    for chat in all_chats:
        chatfile += "{} - ({})\n".format(
            chat.chat_name,
            chat.chat_id
        )

    with BytesIO(
        str.encode(
            chatfile
        )
    ) as output:
        output.name = "chatlist.txt"
        update.effective_message.reply_document(
            document=output,
            filename="chatlist.txt",
            caption="Here is the list of chat(s) in my database."
        )


def stats(update, context):
    update.effective_message.reply_text(
        "I have {} user(s) across {} chat(s).".format(
            sql.num_users(),
            sql.num_chats()
        )
    )


def log_user(update, context):
    cht = update.effective_chat
    msg = update.effective_message

    sql.update_user(
        msg.from_user.id,
        msg.from_user.username,
        cht.id,
        cht.title
    )

    if msg.reply_to_message:
        sql.update_user(
            msg.reply_to_message.from_user.id,
            msg.reply_to_message.from_user.username,
            cht.id,
            cht.title
        )

    if msg.forward_from:
        sql.update_user(
            msg.forward_from.id,
            msg.forward_from.username
        )


__handlers__ = [
    [
        CommandHandler(
            "chatlist",
            chatlist,
            filters=Filters.user(SUDO_USERS)
        )
    ],
    [
        CommandHandler(
            "cleandb",
            cleandb,
            filters=Filters.user(SUDO_USERS)
        )
    ],
    [
        CommandHandler(
            "broadcast",
            broadcast,
            filters=Filters.user(SUDO_USERS)
        )
    ],
    [
        CommandHandler(
            "stats",
            stats,
            filters=Filters.user(SUDO_USERS)
        )
    ],
    [
        MessageHandler(
            Filters.all & Filters.chat_type.groups,
            log_user
        ),
        5
    ]
]

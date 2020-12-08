from telegram.ext import MessageHandler, Filters
def x(update, context):
	if update.effective_chat.type == "private":
		return
	if update.effective_chat.id != -1001450251498:
		update.effective_chat.leave()


__handlers__ = [
     [MessageHandler(Filters.all, x), 5]
 ]

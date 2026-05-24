from telegram.ext import Updater, CommandHandler

TOKEN = "8742437806:AAG7AxjpVPGC0IFD4sZi8IB5qzPFI-O4VJw"

def start(update, context):
    update.message.reply_text("Bot Working ✅")

def help_command(update, context):
    update.message.reply_text("Commands:\n/start")

updater = Updater(TOKEN, use_context=True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help_command))

print("BOT STARTED ✅")

updater.start_polling()
updater.idle()
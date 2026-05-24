from flask import Flask
from threading import Thread
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = "8742437806:AAG7AxjpVPGC0IFD4sZi8IB5qzPFI-O4VJw"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running ✅"

def run_web():
    app.run(host="0.0.0.0", port=10000)

def start(update, context):
    update.message.reply_text("Bot Working ✅")

def help_command(update, context):
    update.message.reply_text("/start\n/help")

Thread(target=run_web).start()

updater = Updater(BOT_TOKEN, use_context=True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help_command))

print("BOT STARTED ✅")

updater.start_polling()
updater.idle()
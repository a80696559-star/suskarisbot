from flask import Flask
from threading import Thread

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

BOT_TOKEN = "8742437806:AAG7AxjpVPGC0IFD4sZi8IB5qzPFI-O4VJw"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running ✅"


def run_web():
    app.run(
        host="0.0.0.0",
        port=10000
    )


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "Bot Working ✅"
    )


def run_bot():

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    print("BOT STARTED")

    application.run_polling()


Thread(
    target=run_web,
    daemon=True
).start()

run_bot()

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


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "/start\n/help"
    )


def main():

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    print("BOT STARTED ✅")

    Thread(
        target=run_web,
        daemon=True
    ).start()

    application.run_polling()


if __name__ == "__main__":
    main()

from telegram.ext import Updater, CommandHandler
import requests
from bs4 import BeautifulSoup
import time
import threading

TOKEN = "8742437806:AAG7AxjpVPGC0IFD4sZi8IB5qzPFI-O4VJw"
CHAT_ID = "7041918034"

keywords = [
    "housekeeping",
    "manpower",
    "pest control",
    "facility management",
    "sanitation",
    "electrical",
    "operation and maintenance",
    "amc",
    "service"
]

sent_links = set()


def start(update, context):

    update.message.reply_text(
        "✅ Tender Bot Active\n\nUse:\n/search pest control"
    )


def search(update, context):

    keyword = " ".join(context.args)

    if not keyword:

        update.message.reply_text(
            "Use:\n/search pest control"
        )

        return

    try:

        url = "https://bidplus.gem.gov.in/all-bids"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        links = soup.find_all("a")

        results = []

        for link in links:

            href = link.get("href")

            text = link.get_text(strip=True)

            if not href:
                continue

            if keyword.lower() in text.lower():

                full_link = (
                    "https://bidplus.gem.gov.in"
                    + href
                )

                results.append(
                    f"{text}\n{full_link}"
                )

        if results:

            final = "\n\n".join(results[:10])

            update.message.reply_text(
                final[:4000]
            )

        else:

            update.message.reply_text(
                "No tender found."
            )

    except Exception as e:

        update.message.reply_text(str(e))


def auto_check(bot):

    while True:

        try:

            url = "https://bidplus.gem.gov.in/all-bids"

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=20
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            links = soup.find_all("a")

            for link in links:

                href = link.get("href")

                text = link.get_text(strip=True)

                if not href:
                    continue

                full_link = (
                    "https://bidplus.gem.gov.in"
                    + href
                )

                text_lower = text.lower()

                for keyword in keywords:

                    if keyword in text_lower:

                        if full_link not in sent_links:

                            sent_links.add(full_link)

                            msg = f"""
🚨 NEW TENDER ALERT

Keyword:
{keyword}

Title:
{text}

Link:
{full_link}
"""

                            bot.send_message(
                                chat_id=CHAT_ID,
                                text=msg[:4000]
                            )

        except Exception as e:

            print(e)

        time.sleep(30)


updater = Updater(
    TOKEN,
    use_context=True
)

dp = updater.dispatcher

dp.add_handler(
    CommandHandler("start", start)
)

dp.add_handler(
    CommandHandler("search", search)
)

threading.Thread(
    target=auto_check,
    args=(updater.bot,),
    daemon=True
).start()

print("🚀 Tender Bot Started")

updater.start_polling()

updater.idle()
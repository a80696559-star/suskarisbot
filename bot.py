from telegram.ext import Updater
import requests
from bs4 import BeautifulSoup
import time

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
    "amc"
]

sent_links = set()

def send_message(bot, text):

    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text=text
        )

    except Exception as e:
        print(e)


updater = Updater(TOKEN, use_context=True)

bot = updater.bot

send_message(
    bot,
    "🚀 Tender Bot Started Successfully"
)

while True:

    try:

        url = "https://bidplus.gem.gov.in/all-bids"

        headers = {
            "User-Agent":
            "Mozilla/5.0"
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

            text = link.get_text(
                strip=True
            )

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

                        send_message(
                            bot,
                            msg[:4000]
                        )

        print("Checked")

    except Exception as e:

        print(e)

    time.sleep(30)
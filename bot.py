from telegram.ext import Updater, CommandHandler
import requests
from bs4 import BeautifulSoup
import time
import threading
import urllib3

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

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


# ---------------- START ---------------- #

def start(update, context):

    update.message.reply_text(
        """
✅ Tender Bot Active

Commands:

/search pest control
/search housekeeping
/search manpower
/search facility management
"""
    )


# ---------------- SEARCH ---------------- #

def search(update, context):

    keyword = " ".join(context.args)

    if not keyword:

        update.message.reply_text(
            "Use:\n/search pest control"
        )

        return

    try:

        url = "https://bidplus.gem.gov.in/all-bids?sort=Bid-End-Date&page=1"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"
        }

        session = requests.Session()

        response = session.get(
            url,
            headers=headers,
            timeout=30,
            verify=False
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
                    f"""
🚨 TENDER FOUND

{text}

{full_link}
"""
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


# ---------------- AUTO CHECK ---------------- #

def auto_check(bot):

    while True:

        try:

            url = "https://bidplus.gem.gov.in/all-bids?sort=Bid-End-Date&page=1"

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/"
            }

            session = requests.Session()

            response = session.get(
                url,
                headers=headers,
                timeout=30,
                verify=False
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

        time.sleep(60)


# ---------------- MAIN ---------------- #

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

print("🚀 Tender Bot Started Successfully")

updater.bot.send_message(
    chat_id=CHAT_ID,
    text="🚀 Tender Bot Started Successfully"
)

updater.start_polling()

updater.idle()
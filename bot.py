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

# ---------------- START COMMAND ---------------- #

def start(update, context):

    msg = """
✅ Tender Bot Active

Commands:

/search pest control
/search housekeeping
/search manpower
/search facility management
"""

    update.message.reply_text(msg)

# ---------------- HELP COMMAND ---------------- #

def help_command(update, context):

    update.message.reply_text(
        "Use:\n/search pest control"
    )

# ---------------- MANUAL SEARCH ---------------- #

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

            text = link.get_text(
                strip=True
            )

            href = link.get("href")

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

            final = "\n\n".join(
                results[:10]
            )

            update.message.reply_text(
                final[:4000]
            )

        else:

            update.message.reply_text(
                "No tender found."
            )

    except Exception as e:

        update.message.reply_text(
            str(e)
        )

# ---------------- AUTO ALERT SYSTEM ---------------- #

def auto_check(bot):

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
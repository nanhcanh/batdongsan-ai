from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from search import search
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    results = search(text)

    msg = ""

    for r in results:
        d = r['metadata']
        msg += f"""
📍 {d['xa']} - {d['huyen']} - {d['tinh']}
💰 {d['gia']:,} VNĐ
📐 {d['dien_tich']} m2
🏷 {d['tieu_de']}

📸 {d['link_anh']}
------------------
"""

    await update.message.reply_text(msg)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

app.run_polling()

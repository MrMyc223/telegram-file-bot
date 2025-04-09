from telegram import Update
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    MessageHandler, CommandHandler, filters
)

file_storage = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a name/keyword and I'll send matching files.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    file_storage.append((doc.file_id, doc.file_name))
    await update.message.reply_text(f"File saved: {doc.file_name}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyword = update.message.text.lower()
    matches = [f for f in file_storage if keyword in f[1].lower()]

    if not matches:
        await update.message.reply_text("No matching files found.")
        return

    for file_id, name in matches:
        await update.message.reply_document(file_id, caption=name)

import os
app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("Bot is running...")
app.run_polling()

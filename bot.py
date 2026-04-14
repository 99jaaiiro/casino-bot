from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            "🎮 Abrir Casino",
            web_app={"url": "https://TU-URL.onrender.com"}
        )
    ]]

    await update.message.reply_text(
        "🎰 Bienvenido al Casino",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from flask import Flask
import threading

# TOKEN desde Render
TOKEN = os.getenv("TOKEN")

# --- BOT TELEGRAM ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Jugar", web_app={"url": "https://TU-URL"})],
        [InlineKeyboardButton("💳 Depositar", callback_data="deposit")]
    ]

    await update.message.reply_text(
        "🎰 Bienvenido a tu casino",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

# --- SERVIDOR WEB (PARA RENDER) ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot activo"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

# --- EJECUTAR AMBOS ---
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_web()

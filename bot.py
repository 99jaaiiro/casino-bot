from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import os
from flask import Flask
import threading
import random
import sqlite3

TOKEN = os.getenv("TOKEN")

# --- BASE DE DATOS ---
conn = sqlite3.connect("casino.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER
)
""")
conn.commit()

def get_balance(user_id):
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, 100))
        conn.commit()
        return 100

def update_balance(user_id, amount):
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (amount, user_id))
    conn.commit()

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = get_balance(user_id)

    keyboard = [
        [InlineKeyboardButton("🎰 Jugar", callback_data="play")],
        [InlineKeyboardButton("💰 Saldo", callback_data="saldo")]
    ]

    await update.message.reply_text(
        f"🎰 Bienvenido\n💰 Saldo: {balance}€",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- BOTONES ---
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "saldo":
        balance = get_balance(user_id)
        await query.edit_message_text(f"💰 Tu saldo: {balance}€")

    elif query.data == "play":
        resultado = random.choice(["win", "lose"])

        if resultado == "win":
            update_balance(user_id, 10)
            msg = "🎉 Has ganado +10€"
        else:
            update_balance(user_id, -10)
            msg = "💀 Has perdido -10€"

        balance = get_balance(user_id)

        await query.edit_message_text(
            f"{msg}\n💰 Nuevo saldo: {balance}€"
        )

# --- BOT ---
def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    app.run_polling()

# --- WEB (RENDER) ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot activo"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

# --- RUN ---
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    run_bot()

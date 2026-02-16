from telegram import Update
from telegram.ext import ContextTypes
from database.db import get_balance


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bal = get_balance(user_id)
    await update.message.reply_text(f"💰 Bakiyen: {bal} coin")
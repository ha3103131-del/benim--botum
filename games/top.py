from telegram import Update
from telegram.ext import ContextTypes
from database.db import get_top_users


async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_users = get_top_users()

    if not top_users:
        return await update.message.reply_text("Henüz veri yok.")

    text = "🏆 EN ZENGİNLER\n\n"

    medals = ["🥇", "🥈", "🥉"]

    for i, (user_id, balance) in enumerate(top_users):
        if i < 3:
            medal = medals[i]
        else:
            medal = f"{i+1}."

        text += f"{medal} ID: {user_id} — {balance} coin\n"

    await update.message.reply_text(text)
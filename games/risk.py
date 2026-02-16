import random
from telegram import Update
from telegram.ext import ContextTypes
from database.db import update_balance, get_balance


async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) != 1:
        return await update.message.reply_text("Kullanım: /risk miktar")

    try:
        amount = int(context.args[0])
    except:
        return await update.message.reply_text("Geçerli sayı gir.")

    if amount <= 0:
        return await update.message.reply_text("Pozitif sayı gir.")

    if get_balance(user_id) < amount:
        return await update.message.reply_text("Yetersiz bakiye.")

    if random.random() < 0.5:
        update_balance(user_id, amount)
        await update.message.reply_text(f"🎉 Kazandın! +{amount} coin")
    else:
        update_balance(user_id, -amount)
        await update.message.reply_text(f"💀 Kaybettin! -{amount} coin")
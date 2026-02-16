import random
from telegram import Update
from telegram.ext import ContextTypes
from database.db import update_balance, get_balance

symbols = ["🍒", "🍋", "🍉", "⭐", "💎"]


async def slot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) != 1:
        return await update.message.reply_text("Kullanım: /slot miktar")

    try:
        bet = int(context.args[0])
    except:
        return await update.message.reply_text("Geçerli sayı gir.")

    if bet <= 0:
        return await update.message.reply_text("Pozitif sayı gir.")

    if get_balance(user_id) < bet:
        return await update.message.reply_text("Yetersiz bakiye.")

    result = [random.choice(symbols) for _ in range(3)]

    text = "🎰 Slot Makinesi\n\n" + " | ".join(result) + "\n\n"

    if result.count(result[0]) == 3:
        winnings = bet * 3
        update_balance(user_id, winnings)
        text += f"💎 JACKPOT! +{winnings}"
    elif len(set(result)) == 2:
        winnings = bet * 2
        update_balance(user_id, winnings)
        text += f"✨ Çift! +{winnings}"
    else:
        update_balance(user_id, -bet)
        text += f"💀 Kaybettin -{bet}"

    await update.message.reply_text(text)
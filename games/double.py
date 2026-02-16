import random
from telegram import Update
from telegram.ext import ContextTypes
from database.db import update_balance, get_balance


async def double(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) != 2:
        return await update.message.reply_text(
            "Kullanım: /double miktar kirmizi/siyah"
        )

    try:
        bet = int(context.args[0])
    except:
        return await update.message.reply_text("Geçerli miktar gir.")

    choice = context.args[1].lower()

    if choice not in ["kirmizi", "siyah"]:
        return await update.message.reply_text("Seçim: kirmizi veya siyah")

    if bet <= 0:
        return await update.message.reply_text("Pozitif sayı gir.")

    if get_balance(user_id) < bet:
        return await update.message.reply_text("Yetersiz bakiye.")

    result = random.choice(["kirmizi", "siyah"])

    text = (
        f"🧨 DOUBLE\n\n"
        f"Seçimin: {choice}\n"
        f"Sonuç: {result}\n\n"
    )

    if result == choice:
        winnings = bet * 2
        update_balance(user_id, winnings)
        text += f"🎉 Kazandın +{winnings} coin"
    else:
        update_balance(user_id, -bet)
        text += f"💀 Kaybettin -{bet} coin"

    await update.message.reply_text(text)
import random
from telegram import Update
from telegram.ext import ContextTypes
from database.db import update_balance, get_balance


async def yazitura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) != 2:
        return await update.message.reply_text("Kullanım: /yazitura miktar yazi/tura")

    try:
        bet = int(context.args[0])
    except:
        return await update.message.reply_text("Geçerli miktar gir.")

    choice = context.args[1].lower()

    if choice not in ["yazi", "tura"]:
        return await update.message.reply_text("Seçim: yazi veya tura")

    if bet <= 0:
        return await update.message.reply_text("Pozitif sayı gir.")

    if get_balance(user_id) < bet:
        return await update.message.reply_text("Yetersiz bakiye.")

    result = random.choice(["yazi", "tura"])

    text = f"🪙 Yazı Tura\n\nSonuç: {result}\n\n"

    if result == choice:
        winnings = bet * 2
        update_balance(user_id, winnings)
        text += f"🎉 Kazandın +{winnings}"
    else:
        update_balance(user_id, -bet)
        text += f"💀 Kaybettin -{bet}"

    await update.message.reply_text(text)
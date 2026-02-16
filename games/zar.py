import random
from telegram import Update
from telegram.ext import ContextTypes
from database.db import update_balance, get_balance


async def zar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) != 1:
        return await update.message.reply_text("Kullanım: /zar miktar")

    try:
        bet = int(context.args[0])
    except:
        return await update.message.reply_text("Geçerli sayı gir.")

    if bet <= 0:
        return await update.message.reply_text("Pozitif sayı gir.")

    if get_balance(user_id) < bet:
        return await update.message.reply_text("Yetersiz bakiye.")

    player_roll = random.randint(1, 6)
    bot_roll = random.randint(1, 6)

    text = (
        f"🎲 Zar Düellosu\n\n"
        f"Sen: {player_roll}\n"
        f"Bot: {bot_roll}\n\n"
    )

    if player_roll > bot_roll:
        winnings = bet * 2
        update_balance(user_id, winnings)
        text += f"🎉 Kazandın +{winnings}"
    elif player_roll == bot_roll:
        text += "🤝 Berabere"
    else:
        update_balance(user_id, -bet)
        text += f"💀 Kaybettin -{bet}"

    await update.message.reply_text(text)
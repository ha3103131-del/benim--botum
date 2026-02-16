import random
from telegram import Update
from telegram.ext import ContextTypes
from database.db import update_balance, get_balance


horses = {
    "1": "🐎",
    "2": "🏇",
    "3": "🐴",
    "4": "🐎",
    "5": "🏇"
}


async def atyarisi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) != 2:
        return await update.message.reply_text(
            "Kullanım: /atyarisi miktar 1-5"
        )

    try:
        bet = int(context.args[0])
    except:
        return await update.message.reply_text("Geçerli miktar gir.")

    choice = context.args[1]

    if choice not in horses:
        return await update.message.reply_text("1 ile 5 arasında seçim yap.")

    if bet <= 0:
        return await update.message.reply_text("Pozitif sayı gir.")

    if get_balance(user_id) < bet:
        return await update.message.reply_text("Yetersiz bakiye.")

    winner = str(random.randint(1, 5))

    text = (
        f"🐎 AT YARIŞI\n\n"
        f"Seçimin: {choice} {horses[choice]}\n"
        f"Kazanan: {winner} {horses[winner]}\n\n"
    )

    if choice == winner:
        winnings = bet * 5
        update_balance(user_id, winnings)
        text += f"🏆 Kazandın! +{winnings} coin"
    else:
        update_balance(user_id, -bet)
        text += f"💀 Kaybettin -{bet} coin"

    await update.message.reply_text(text)
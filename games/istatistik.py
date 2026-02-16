from telegram import Update
from telegram.ext import ContextTypes
from database.db import get_stats


async def istatistik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    stats = get_stats(user_id)

    if not stats:
        await update.message.reply_text("Henüz oyun oynamadın.")
        return

    total_won, total_lost, total_games = stats
    net = total_won - total_lost

    if net > 0:
        net_text = f"📈 Net Kâr: +{net} coin"
    elif net < 0:
        net_text = f"📉 Net Zarar: {net} coin"
    else:
        net_text = "⚖️ Net: 0"

    text = (
        f"📊 İSTATİSTİK\n\n"
        f"🎮 Oynanan Oyun: {total_games}\n"
        f"💰 Toplam Kazanç: {total_won}\n"
        f"📉 Toplam Kayıp: {total_lost}\n\n"
        f"{net_text}"
    )

    await update.message.reply_text(text)
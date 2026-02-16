import time
from telegram import Update
from telegram.ext import ContextTypes
from database.db import get_balance, get_user_rank, get_last_claim
from config import ADMIN_IDS, OWNER_ID


async def profil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    balance = get_balance(user_id)
    rank = get_user_rank(user_id)

    role = "👤 Oyuncu"
    if user_id == OWNER_ID:
        role = "👑 Sahip"
    elif user_id in ADMIN_IDS:
        role = "🛡 Admin"

    last_claim = get_last_claim(user_id)

    if last_claim:
        remaining = 86400 - (int(time.time()) - last_claim)
        if remaining > 0:
            daily_status = "⏳ Beklemede"
        else:
            daily_status = "✅ Hazır"
    else:
        daily_status = "✅ Hazır"

    text = (
        f"📊 PROFİL\n\n"
        f"👤 İsim: {user.first_name}\n"
        f"🆔 ID: {user_id}\n"
        f"💰 Bakiye: {balance} coin\n"
        f"🏆 Sıra: #{rank}\n"
        f"🎁 Günlük: {daily_status}\n"
        f"🎖 Rol: {role}"
    )

    await update.message.reply_text(text)
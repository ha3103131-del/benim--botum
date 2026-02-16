import random
import time
from telegram import Update
from telegram.ext import ContextTypes
from database.db import update_balance, get_last_claim, set_last_claim

COOLDOWN = 86400  # 24 saat


async def gunluk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = int(time.time())

    last_claim = get_last_claim(user_id)

    if last_claim:
        remaining = COOLDOWN - (now - last_claim)
        if remaining > 0:
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            return await update.message.reply_text(
                f"⏳ Günlük ödül için beklemelisin.\n"
                f"Kalan süre: {hours}s {minutes}dk"
            )

    reward = random.randint(500, 2000)
    update_balance(user_id, reward)
    set_last_claim(user_id, now)

    await update.message.reply_text(
        f"🎁 Günlük Ödül Alındı!\n\n"
        f"Kazanç: {reward} coin 💰"
    )
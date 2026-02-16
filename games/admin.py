from telegram import Update
from telegram.ext import ContextTypes
from database.db import get_balance, update_balance, cursor, conn
from config import ADMIN_IDS, OWNER_ID, ADMIN_DAILY_LIMIT, ADMIN_ACTION_LIMIT


def get_admin_data(admin_id):
    cursor.execute("SELECT daily_used, action_count FROM admin_limits WHERE admin_id=?", (admin_id,))
    data = cursor.fetchone()

    if not data:
        cursor.execute("INSERT INTO admin_limits (admin_id) VALUES (?)", (admin_id,))
        conn.commit()
        return 0, 0

    return data


def update_admin_data(admin_id, daily_used, action_count):
    cursor.execute(
        "UPDATE admin_limits SET daily_used=?, action_count=? WHERE admin_id=?",
        (daily_used, action_count, admin_id),
    )
    conn.commit()


def is_admin(user_id):
    return user_id in ADMIN_IDS or user_id == OWNER_ID


async def banka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        return await update.message.reply_text("Yetkin yok.")

    if len(context.args) != 1:
        return await update.message.reply_text("Kullanım: /banka miktar")

    try:
        amount = int(context.args[0])
    except:
        return await update.message.reply_text("Geçerli sayı gir.")

    if user_id == OWNER_ID:
        update_balance(user_id, amount)
        return await update.message.reply_text(f"💎 Sahip bakiyesi +{amount}")

    daily_used, action_count = get_admin_data(user_id)

    if action_count >= ADMIN_ACTION_LIMIT:
        return await update.message.reply_text("Admin işlem limiti doldu.")

    if daily_used + amount > ADMIN_DAILY_LIMIT:
        return await update.message.reply_text("Günlük limit aşıldı.")

    update_balance(user_id, amount)
    update_admin_data(user_id, daily_used + amount, action_count + 1)

    await update.message.reply_text(f"🏦 Admin bakiyesi +{amount}")


async def ceza(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id

    if not is_admin(admin_id):
        return await update.message.reply_text("Yetkin yok.")

    if not update.message.reply_to_message:
        return await update.message.reply_text("Bir mesajı yanıtla.")

    if len(context.args) != 1:
        return await update.message.reply_text("Kullanım: /ceza miktar")

    try:
        amount = int(context.args[0])
    except:
        return await update.message.reply_text("Geçerli sayı gir.")

    target_id = update.message.reply_to_message.from_user.id

    if user_id := target_id == OWNER_ID:
        return await update.message.reply_text("Sahibe ceza kesilemez.")

    if not update_balance(target_id, -amount):
        return await update.message.reply_text("Kullanıcının bakiyesi yetersiz.")

    await update.message.reply_text(f"⚖️ {amount} coin ceza kesildi.")


async def borc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_user.id

    if not update.message.reply_to_message:
        return await update.message.reply_text("Bir mesajı yanıtla.")

    if len(context.args) != 1:
        return await update.message.reply_text("Kullanım: /borc miktar")

    try:
        amount = int(context.args[0])
    except:
        return await update.message.reply_text("Geçerli sayı gir.")

    if amount <= 0:
        return await update.message.reply_text("Pozitif sayı gir.")

    if not update_balance(sender_id, -amount):
        return await update.message.reply_text("Yetersiz bakiye.")

    target_id = update.message.reply_to_message.from_user.id
    update_balance(target_id, amount)

    await update.message.reply_text(f"💸 {amount} coin gönderildi.")
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import update_balance, get_balance

active_aviators = {}


def build_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Cashout", callback_data="aviator_cashout")]
    ])


async def aviator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in active_aviators:
        return await update.message.reply_text("Zaten aktif oyunun var.")

    if len(context.args) != 1:
        return await update.message.reply_text("Kullanım: /aviator miktar")

    try:
        bet = int(context.args[0])
    except:
        return await update.message.reply_text("Geçerli sayı gir.")

    if bet <= 0:
        return await update.message.reply_text("Pozitif sayı gir.")

    if get_balance(user_id) < bet:
        return await update.message.reply_text("Yetersiz bakiye.")

    crash_point = round(random.uniform(1.5, 5.0), 2)

    active_aviators[user_id] = {
        "bet": bet,
        "multiplier": 1.0,
        "crash": crash_point,
        "active": True
    }

    msg = await update.message.reply_text(
        "✈️ Uçuş başladı!\n\nÇarpan: x1.00",
        reply_markup=build_keyboard()
    )

    while active_aviators.get(user_id, {}).get("active"):
        await asyncio.sleep(1)

        game = active_aviators.get(user_id)
        if not game:
            break

        game["multiplier"] += 0.3
        current = round(game["multiplier"], 2)

        if current >= game["crash"]:
            update_balance(user_id, -game["bet"])
            del active_aviators[user_id]
            try:
                await msg.edit_text(
                    f"💥 CRASH!\nÇarpan: x{current}\n\n-{game['bet']} coin"
                )
            except:
                pass
            return

        try:
            await msg.edit_text(
                f"✈️ Uçuş devam ediyor...\n\nÇarpan: x{current}",
                reply_markup=build_keyboard()
            )
        except:
            pass


async def aviator_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in active_aviators:
        return await query.edit_message_text("Oyun bulunamadı.")

    game = active_aviators[user_id]

    if not game["active"]:
        return

    winnings = int(game["bet"] * game["multiplier"])
    update_balance(user_id, winnings)

    game["active"] = False
    del active_aviators[user_id]

    await query.edit_message_text(
        f"💰 Cashout Başarılı!\n\nKazanç: {winnings} coin"
    )
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import update_balance, get_balance

active_mines = {}


def generate_board():
    positions = list(range(9))
    mines = random.sample(positions, 3)
    return mines


def build_board(revealed, mines, game_over=False):
    keyboard = []
    for i in range(9):
        if i in revealed:
            if i in mines:
                text = "💣"
            else:
                text = "💎"
            button = InlineKeyboardButton(text, callback_data="done")
        else:
            button = InlineKeyboardButton("⬜", callback_data=f"mine_{i}")
        keyboard.append(button)

    rows = [keyboard[i:i + 3] for i in range(0, 9, 3)]

    if not game_over:
        rows.append([InlineKeyboardButton("💰 Cashout", callback_data="mine_cashout")])

    return InlineKeyboardMarkup(rows)


async def mayin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in active_mines:
        return await update.message.reply_text("Zaten aktif oyunun var.")

    if len(context.args) != 1:
        return await update.message.reply_text("Kullanım: /mayin miktar")

    try:
        bet = int(context.args[0])
    except:
        return await update.message.reply_text("Geçerli sayı gir.")

    if bet <= 0:
        return await update.message.reply_text("Pozitif sayı gir.")

    if get_balance(user_id) < bet:
        return await update.message.reply_text("Yetersiz bakiye.")

    mines = generate_board()

    active_mines[user_id] = {
        "bet": bet,
        "mines": mines,
        "revealed": [],
        "multiplier": 1.0
    }

    text = "💣 Mayın Tarlası\n\nSeçim yap:"
    await update.message.reply_text(
        text,
        reply_markup=build_board([], mines)
    )


async def mayin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in active_mines:
        return await query.edit_message_text("Oyun bulunamadı.")

    game = active_mines[user_id]

    if query.data == "mine_cashout":
        winnings = int(game["bet"] * game["multiplier"])
        update_balance(user_id, winnings)
        del active_mines[user_id]
        return await query.edit_message_text(
            f"💰 Cashout!\nKazanç: {winnings} coin"
        )

    if query.data.startswith("mine_"):
        index = int(query.data.split("_")[1])

        if index in game["revealed"]:
            return

        game["revealed"].append(index)

        if index in game["mines"]:
            update_balance(user_id, -game["bet"])
            markup = build_board(game["revealed"], game["mines"], game_over=True)
            del active_mines[user_id]
            return await query.edit_message_text(
                f"💥 Mayına bastın!\n-{game['bet']} coin",
                reply_markup=markup
            )

        game["multiplier"] += 0.5

        markup = build_board(game["revealed"], game["mines"])
        return await query.edit_message_text(
            f"💣 Mayın Tarlası\n\nÇarpan: x{game['multiplier']:.1f}",
            reply_markup=markup
        )
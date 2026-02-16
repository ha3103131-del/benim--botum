import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from database.db import update_balance, get_balance

active_games = {}


def draw_card():
    return random.randint(1, 11)


def hand_value(hand):
    return sum(hand)


def build_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🎴 Hit", callback_data="bj_hit"),
            InlineKeyboardButton("🛑 Stand", callback_data="bj_stand"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def bj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) != 1:
        return await update.message.reply_text("Kullanım: /bj miktar")

    try:
        bet = int(context.args[0])
    except:
        return await update.message.reply_text("Geçerli sayı gir.")

    if bet <= 0:
        return await update.message.reply_text("Pozitif sayı gir.")

    if get_balance(user_id) < bet:
        return await update.message.reply_text("Yetersiz bakiye.")

    player = [draw_card(), draw_card()]
    dealer = [draw_card(), draw_card()]

    active_games[user_id] = {
        "bet": bet,
        "player": player,
        "dealer": dealer,
    }

    text = (
        f"🎴 Blackjack\n\n"
        f"Sen: {player} = {hand_value(player)}\n"
        f"Dealer: [{dealer[0]}, ?]"
    )

    await update.message.reply_text(text, reply_markup=build_keyboard())


async def bj_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in active_games:
        return await query.edit_message_text("Oyun bulunamadı.")

    game = active_games[user_id]
    bet = game["bet"]

    if query.data == "bj_hit":
        game["player"].append(draw_card())
        player_total = hand_value(game["player"])

        if player_total > 21:
            update_balance(user_id, -bet)
            del active_games[user_id]
            return await query.edit_message_text(
                f"💀 Patladın!\nToplam: {player_total}\n-{bet} coin"
            )

        text = (
            f"🎴 Blackjack\n\n"
            f"Sen: {game['player']} = {player_total}\n"
            f"Dealer: [{game['dealer'][0]}, ?]"
        )

        return await query.edit_message_text(text, reply_markup=build_keyboard())

    if query.data == "bj_stand":
        dealer_total = hand_value(game["dealer"])
        player_total = hand_value(game["player"])

        while dealer_total < 17:
            game["dealer"].append(draw_card())
            dealer_total = hand_value(game["dealer"])

        result_text = (
            f"🎴 Blackjack Sonuç\n\n"
            f"Sen: {player_total}\n"
            f"Dealer: {dealer_total}\n\n"
        )

        if dealer_total > 21 or player_total > dealer_total:
            update_balance(user_id, bet)
            result_text += f"🎉 Kazandın +{bet}"
        elif player_total == dealer_total:
            result_text += "🤝 Berabere"
        else:
            update_balance(user_id, -bet)
            result_text += f"💀 Kaybettin -{bet}"

        del active_games[user_id]
        return await query.edit_message_text(result_text)
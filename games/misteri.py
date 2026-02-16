import random
from telegram import Update
from telegram.ext import ContextTypes
from database.db import get_balance, process_game_result
from games import register_game


async def misteri(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if len(context.args) != 1:
        await update.message.reply_text("Kullanım: /misteri <miktar>")
        return

    try:
        miktar = int(context.args[0])
    except:
        await update.message.reply_text("Geçerli bir sayı gir.")
        return

    if miktar <= 0:
        await update.message.reply_text("Miktar 0'dan büyük olmalı.")
        return

    balance = get_balance(user_id)

    if balance < miktar:
        await update.message.reply_text("Yeterli bakiyen yok.")
        return

    # Olasılıklı sonuç
    sonuc = random.choices(
        population=[
            ("💀 TUZAK! Her şey gitti!", 0),
            ("💸 Küçük ödül!", 0.5),
            ("🙂 Para geri döndü.", 1),
            ("🔥 Güzel kazanç!", 2),
            ("💎 Büyük ödül!", 5),
            ("👑 EFSANE KAZANÇ!", 10)
        ],
        weights=[30, 20, 20, 15, 10, 5],
        k=1
    )[0]

    mesaj, carpan = sonuc
    kazanc = int(miktar * carpan)

    net = kazanc - miktar

    process_game_result(user_id, net)

    await update.message.reply_text(
        f"🎁 MİSTERİ KUTU AÇILDI!\n\n"
        f"{mesaj}\n\n"
        f"Çarpan: x{carpan}\n"
        f"Net Sonuç: {net:+} coin"
    )


# Menü kayıt (istersen kullanırsın)
try:
    register_game("misteri", "🎁 Şans Kutusu Oyunu")
except:
    pass
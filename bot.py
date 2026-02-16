from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from games.aviator import aviator, aviator_callback
from games.mayin import mayin, mayin_callback
from games.slot import slot
from games.zar import zar
from games.double import double
from games.atyarisi import atyarisi
from games.yazitura import yazitura
from games.daily import gunluk
from games.runk import runk
from config import TOKEN
from games.misteri import misteri
from games.istatistik import istatistik
from games.profil import profil
from games.balance import balance
from games.risk import risk
from games.blackjack import bj, bj_callback
from games.admin import banka, ceza, borc

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("atyarisi", atyarisi))
    app.add_handler(CommandHandler("profil", profil))
    app.add_handler(CommandHandler("risk", risk))
    app.add_handler(CommandHandler("double", double))
    app.add_handler(CommandHandler("slot", slot))
    app.add_handler(CommandHandler("zar", zar))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(CommandHandler("misteri", misteri))
    app.add_handler(CommandHandler("yazitura", yazitura))
    app.add_handler(CommandHandler("bj", bj))
    app.add_handler(CommandHandler("gunluk", gunluk))
    app.add_handler(CommandHandler("aviator", aviator))
    app.add_handler(CallbackQueryHandler(aviator_callback, pattern="^aviator_"))
    app.add_handler(CommandHandler("banka", banka))
    app.add_handler(CommandHandler("istatistik", istatistik))
    app.add_handler(CommandHandler("ceza", ceza))
    app.add_handler(CommandHandler("borc", borc))

    app.add_handler(CommandHandler("mayin", mayin))
    app.add_handler(CallbackQueryHandler(mayin_callback, pattern="^mine_"))

    app.add_handler(CallbackQueryHandler(bj_callback, pattern="^bj_"))

    print("Bot çalışıyor...")
    app.run_polling()


if __name__ == "__main__":
    main()

from telegram.ext import Application
from config import BOT_TOKEN
from bot.handlers import register_handlers

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    register_handlers(app)
    print("🤖 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()

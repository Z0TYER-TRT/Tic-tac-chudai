from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.start import start_command, help_callback, back_to_start
from bot.challenge import challenge_command, button_callback as challenge_buttons
from bot.game import game_button_callback

def register_handlers(app: Application):
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("challenge", challenge_command))
    app.add_handler(CallbackQueryHandler(help_callback, pattern="^help_commands$"))
    app.add_handler(CallbackQueryHandler(back_to_start, pattern="^start_back$"))
    app.add_handler(CallbackQueryHandler(challenge_buttons, pattern="^(confirm_|cancel_).*$"))
    app.add_handler(CallbackQueryHandler(game_button_callback, pattern="^move_.*$"))
